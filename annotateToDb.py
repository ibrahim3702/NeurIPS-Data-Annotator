import fitz  # PyMuPDF for reading PDFs
import mysql.connector
import google.generativeai as genai
import json
import os
import time
import re

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Change if needed
    "password": "",  # Change if needed
    "database": "neurips_papers"
}

# Google Gemini API Configuration
GENAI_API_KEY = "GENAI_API_KEY" #your api key here

# Set up Google Gemini API
genai.configure(api_key=GENAI_API_KEY)

# Folder where PDFs are stored
PDF_BASE_PATH = r'D:\scrapped-pdf' #Change if needed

def create_papers_table_if_not_exists():
    """Creates the 'papers' table in the database if it doesn't exist."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS papers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        pdf_path VARCHAR(200) UNIQUE,
        labels JSON,
        author VARCHAR(255),
        publication_date VARCHAR(50)
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def extract_metadata_from_pdf(pdf_path):
    """Extract metadata (title, author, publication date) from a PDF."""
    full_path = os.path.join(PDF_BASE_PATH, pdf_path)

    if not os.path.exists(full_path):
        print(f"❌ PDF not found: {full_path}")
        return None

    try:
        doc = fitz.open(full_path)
        metadata = doc.metadata
        title = metadata.get("title", "Unknown Title")
        author = metadata.get("author", "Unknown Author")
        creation_date = metadata.get("creationDate", "Unknown Date")
        doc.close()
        return {"title": title, "author": author, "publication_date": creation_date}
    except Exception as e:
        print(f"❌ Error extracting metadata from {pdf_path}: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """Extract text content from a given PDF"""
    full_path = os.path.join(PDF_BASE_PATH, pdf_path)

    if not os.path.exists(full_path):
        print(f"❌ PDF not found: {full_path}")
        return None

    doc = fitz.open(full_path)
    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return text if text.strip() else None

def call_gemini_api(text):
    """Send extracted text to Google Gemini API and get three labels."""
    prompt = f"""
    Read the following research paper text and generate exactly three relevant category labels:
    -----
    {text[:4000]}  # Limit to 4000 characters to avoid API token issues
    -----
    Return only a JSON list of three labels. Example:
    ["Deep Learning", "Computer Vision", "Interpretability"]
    """

    model = genai.GenerativeModel("gemini-2.0-flash")

    for attempt in range(5):  # Retry up to 5 times
        try:
            response = model.generate_content(prompt)

            # Check if response exists and contains valid text
            if not response or not hasattr(response, "text") or not response.text.strip():
                print("⚠️ Empty API response. Retrying...")
                time.sleep(10)
                continue

            # Clean response text (remove ```json and any extra code formatting)
            cleaned_text = re.sub(r"```json|```", "", response.text).strip()

            # Parse JSON safely
            try:
                labels = json.loads(cleaned_text)
                if isinstance(labels, list) and len(labels) == 3:
                    return labels
                else:
                    print(f"⚠️ Invalid label format: {labels}")
            except json.JSONDecodeError:
                print(f"⚠️ JSON decoding failed: {cleaned_text}")

        except Exception as e:
            error_message = str(e)
            if "429" in error_message:
                print("⚠️ API quota exceeded! Retrying after 60 seconds...")
                time.sleep(60)  # Wait before retrying
                continue
            elif "finish_reason is 3" in error_message or "safety_ratings" in error_message:
                print("⚠️ Gemini API blocked this paper due to safety concerns.")
                return None
            else:
                print(f"❌ API Error: {e}")
                break  # Exit loop on non-retryable errors

    print(f"⚠️ Unexpected API Response: {response.text if response else 'No Response'}")
    return None

def insert_paper_into_db(pdf_path, title, author, publication_date, labels):
    """Insert paper metadata and labels into the database."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    labels_str = json.dumps(labels) if labels else None

    query = """
    INSERT INTO papers (title, pdf_path, labels, author, publication_date)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE labels = %s;
    """
    cursor.execute(query, (title, pdf_path, labels_str, author, publication_date, labels_str))
    conn.commit()
    cursor.close()
    conn.close()

def process_pdfs_in_folder():
    """Process all PDFs in the specified folder, labelizing them and storing metadata."""
    create_papers_table_if_not_exists()
    for filename in os.listdir(PDF_BASE_PATH):
        if filename.lower().endswith(".pdf"):
            pdf_path = filename
            print(f"🔍 Processing: {pdf_path}")

            metadata = extract_metadata_from_pdf(pdf_path)
            if not metadata:
                print(f"⚠️ Skipping {pdf_path} due to metadata extraction failure.")
                continue

            pdf_text = extract_text_from_pdf(pdf_path)
            if not pdf_text:
                print(f"⚠️ Skipping {pdf_path} due to empty PDF content.")
                continue

            labels = call_gemini_api(pdf_text)
            if labels:
                print(f"✅ Labels Generated: {labels}")
            else:
                print("❌ Failed to generate labels.")

            insert_paper_into_db(pdf_path, metadata["title"], metadata["author"], metadata["publication_date"], labels)

            # Delay to avoid hitting API rate limits
            time.sleep(2)

    print("🎉 Annotation process fully completed.")

if __name__ == "__main__":
    process_pdfs_in_folder()
