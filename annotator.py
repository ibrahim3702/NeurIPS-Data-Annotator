import os
import time
import csv
import google.generativeai as genai
from PyPDF2 import PdfReader
from datetime import datetime
import itertools
import signal  
import sys     

# --- Configuration ---
PDF_FOLDER_PATH = r'D:\scrapped-pdf'
LABELS = [
    "Machine Learning",
    "Deep Learning",
    "Computer Vision",
    "Natural Language Processing",
    "Reinforcement Learning",
    "Optimization",
    "Theory",
    "Applications",
    "Algorithms",
    "Datasets"
]
GENERIC_LABELS_PROMPT = ", ".join(LABELS)
GEMINI_API_KEYS = [
    os.getenv("GOOGLE_API_KEY"),
    os.getenv("GOOGLE_API_KEY2"),
    os.getenv("GOOGLE_API_KEY3")
    # ... add more keys as needed
]
MODEL_NAME = "gemini-1.5-flash"
CSV_OUTPUT_FILE = r'D:\Data annotator\pdf_output.csv'
API_TIMEOUT_SECONDS = 90


GEMINI_API_KEYS = [key for key in GEMINI_API_KEYS if key]

if not GEMINI_API_KEYS:
    print("Error: No Gemini API keys found in environment variables (GEMINI_API_KEY, GEMINI_API_KEY2, etc.).")
    print("Please set up at least one API key.")
    exit()

print(f"DEBUG: Loaded {len(GEMINI_API_KEYS)} Gemini API keys.")

api_key_cycle = itertools.cycle(GEMINI_API_KEYS)  # Create an iterator that cycles through keys

pdf_categories_global = {} # Global dictionary to store categories
csv_header_written = False # Flag to track if CSV header has been written

def extract_text_from_pdf(pdf_path):
    """Extracts text content from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return None
    return text


def categorize_pdf_with_gemini(pdf_text, labels_prompt=GENERIC_LABELS_PROMPT):
    """Categorizes PDF text using Gemini API with retry logic and API key rotation."""

    if not pdf_text:
        return "No Text Extracted"

    prompt_content = f"""
    Instructions: Carefully read the research paper excerpt provided below.
    Identify the MOST relevant category from the following list of categories.
    You MUST ONLY respond with the name of ONE category from the list, or with the word "Other" if none of the categories are suitable.
    Do NOT provide any explanations, full sentences, or conversational text. ONLY output the CATEGORY NAME or "Other".

    Categories: [{labels_prompt}]

    Research Paper Excerpt:
    ---
    {pdf_text}
    ---

    Category:  (Respond with category name or "Other" ONLY)
    """

    max_retries_per_key = 3
    api_error_delay = 60
    api_timeout_seconds = API_TIMEOUT_SECONDS

    api_keys_tried_count = 0
    keys_exhausted_delay_occurred = False

    while api_keys_tried_count < len(GEMINI_API_KEYS) * max_retries_per_key:
        try:
            current_api_key = next(api_key_cycle)
            genai.configure(api_key=current_api_key)
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt_content) # Removed timeout for compatibility
            gemini_output = response.text.strip()

            if gemini_output.lower() not in [label.lower() for label in LABELS + ["Other"]]:
                print(f"Warning: Gemini returned unexpected label: '{gemini_output}'. Review prompt/labels.")
                return "Uncategorized"
            return gemini_output

        except Exception as e:
            if "429" in str(e):
                delay = api_error_delay
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                key_index = GEMINI_API_KEYS.index(current_api_key) if current_api_key in GEMINI_API_KEYS else 'N/A'
                print(
                    f"{timestamp} - Gemini API error (Key rotation): 429 Rate Limit Exceeded (Key index: {key_index}, Attempt {api_keys_tried_count % max_retries_per_key + 1}/{max_retries_per_key}, Total Attempts Across Keys: {api_keys_tried_count + 1}/{len(GEMINI_API_KEYS) * max_retries_per_key})."
                )
                api_keys_tried_count += 1
                if api_keys_tried_count >= len(GEMINI_API_KEYS) * max_retries_per_key and not keys_exhausted_delay_occurred:
                    print(
                        f"{timestamp} - All API keys attempted and possibly rate limited. Waiting for {delay} seconds before retrying key cycle..."
                    )
                    time.sleep(delay)
                    keys_exhausted_delay_occurred = True
                continue

            elif "deadline" in str(e.args[0].lower()) if hasattr(e, 'args') and e.args else "deadline" in str(e):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                key_index = GEMINI_API_KEYS.index(current_api_key) if current_api_key in GEMINI_API_KEYS else 'N/A'
                print(f"{timestamp} - Gemini API Timeout (Key index: {key_index}, Attempt ...).") # ... (rest of timeout message)
                api_keys_tried_count += 1
                continue

            else:
                print(f"Gemini API error (non-429/non-timeout): {e}")
                return "API Error"

    timestamp_fail = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp_fail} - Max API key rotation retries reached. Gemini API categorization failed.")
    return "API Error (Rate Limit/Rotation Exhausted/Timeout)"


def process_pdfs_in_folder(folder_path, labels_list=GENERIC_LABELS_PROMPT):
    global pdf_categories_global, csv_header_written # Access global variables

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            pdf_text = extract_text_from_pdf(pdf_path)
            if pdf_text:
                category = categorize_pdf_with_gemini(pdf_text, labels_list)
                pdf_categories_global[filename] = category # Update GLOBAL dictionary directly
                print(f"  - Category: {category}")
            else:
                pdf_categories_global[filename] = "Text Extraction Failed" # Update GLOBAL dictionary directly
                print(f"  - Category: Text Extraction Failed")

            save_category_to_csv_append(filename, pdf_categories_global[filename], CSV_OUTPUT_FILE, not csv_header_written) # Save immediately, append mode
            if not csv_header_written:
                csv_header_written = True # Mark header as written after the first PDF

            delay_seconds = 1
            print(f"  - Waiting for {delay_seconds} seconds after processing...")
            time.sleep(delay_seconds)
        else:
            print(f"Skipping non-PDF file: {filename}")
    return pdf_categories_global # Return the global dictionary (though it's also updated throughout)


def save_category_to_csv_append(pdf_name, category, csv_filename=CSV_OUTPUT_FILE, write_header=False):
    """Saves a single PDF category to CSV file, appending to the file. Writes header only if write_header is True."""
    file_exists = os.path.exists(csv_filename)

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        if write_header or not file_exists:
            print(f"DEBUG: Writing CSV header...") # DEBUG PRINT - HEADER WRITE CONDITION
            csv_writer.writerow(['PDF Name', 'Category'])
        print(f"DEBUG: Writing data row: PDF Name='{pdf_name}', Category='{category}'") # DEBUG PRINT - DATA WRITE
        csv_writer.writerow([pdf_name, category])

    print(f"  - Saved category for '{pdf_name}' to {csv_filename}")
    
def signal_handler(sig, frame):
    """Handles interrupt signals (like Ctrl+C) - No save needed here as save happens on each PDF."""
    print("\nScript interrupted by user. Exiting...")
    sys.exit(0)


print("Starting PDF Categorization with Gemini...")

signal.signal(signal.SIGINT, signal_handler) # Register signal handler for Ctrl+C

pdf_categories_global = process_pdfs_in_folder(PDF_FOLDER_PATH, GENERIC_LABELS_PROMPT) # Process and save incrementally

print("\n--- Categorization Results (Console Output - Final) ---") # Indicate final output
for pdf_name, category in pdf_categories_global.items(): # Use global dictionary for final output
    print(f"{pdf_name}: {category}")

print("\n--- Done ---")
