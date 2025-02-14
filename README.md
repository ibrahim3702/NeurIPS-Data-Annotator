# 📂 NeurIPS Paper Sorter: ✨ Intelligent Categorization with Gemini AI ✨

[![Project Status: Active - Feature-Rich & Maintained](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/your-github-username/your-repo-name)
[![License: MIT - Open Source & Permissive](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version: 3.12+ - Modern & Optimized](https://img.shields.io/badge/Python-3.12+-yellow.svg)](https://www.python.org/)

<p align="center">
  <img src="https://github.com/ibrahim3702/NeurIPS-Data-Annotator/blob/main/images.png" alt="NeurIPS Paper Sorter Logo" width="300">
</p>

**Organize your research library like never before!** 🚀 This Python tool, powered by Google Gemini AI, intelligently categorizes PDF research papers from NeurIPS and beyond, transforming your chaotic PDF collection into a structured, searchable knowledge base. 📚

---

## 🚀 Project Overview

Navigating the vast ocean of academic research, especially in dynamic fields like AI, demands efficient organization. Conferences like **NeurIPS (Neural Information Processing Systems)** are pivotal, generating a constant stream of groundbreaking publications.  **NeurIPS Paper Sorter** directly tackles the challenge of managing this information overload.

This Python program is your intelligent research assistant, using the power of Google's Gemini AI to automatically sort your PDF research papers.  Think of it as a smart "sorting hat" for your academic library.  It seamlessly:

1.  **Ingests PDF Research Papers:** Processes entire folders of PDFs, ideal for organizing papers downloaded from platforms like NeurIPS.
2.  **Intelligent Content Analysis:** Extracts text and utilizes the advanced natural language understanding of Google's **`gemini-1.5-flash`** model to analyze paper content.
3.  **Automated Category Assignment:**  Intelligently assigns each paper to the *most relevant* category from your pre-defined list of research domains (e.g., Machine Learning, Computer Vision, NLP, etc.).
4.  **Generates Structured CSV Output:**  Neatly saves categorization results into a `pdf_output.csv` file, ready for import into spreadsheets, databases, or research management tools.
5.  **Ensures Robust & Reliable Operation:**  Features built-in mechanisms for API key rotation, intelligent retries, and graceful error handling to overcome API rate limits, timeouts, and network hiccups.

**✨ Key Benefits ✨**

*   ✅ **Save Countless Hours:** Automate the time-consuming task of manual PDF sorting.
*   🧠 **Leverage AI-Powered Intelligence:** Benefit from Gemini AI's nuanced understanding of research content for superior categorization accuracy.
*   📈 **Boost Research Productivity:** Transform a disorganized PDF collection into a structured, searchable, and readily accessible knowledge repository.
*   🛡️ **Reliable and Resilient:**  Built to handle real-world API limitations and potential interruptions, ensuring consistent performance and data integrity.

---

## ✨ Core Features: Powering Your Research Workflow ✨

*   **🤖 Gemini AI Categorization Engine:** Employs Google's cutting-edge `gemini-1.5-flash` model for accurate and contextually relevant text classification.
*   **🏷️ Customizable Categories:** Define and tailor research categories to perfectly match your specific field and organizational needs.
*   **🔄 Robust API Interaction with Key Rotation:**  Intelligently manages API usage with automatic key cycling and retry logic, effectively mitigating rate limits and network issues.
*   **🔧 Resilient String-Based Error Handling:**  Adaptable error detection ensures compatibility across varying versions of the `google-generativeai` library, prioritizing functionality and stability.
*   **📊 Real-time & Persistent CSV Output:**  Results are saved incrementally to `pdf_output.csv` *as you process*, guaranteeing data safety and allowing you to monitor progress live.
*   ✍️ **Append-Mode CSV & Smart Header Management:** New results are seamlessly added to your CSV on each run, intelligently handling header writing to prevent duplication and maintain file integrity.
*   🛑 **Graceful Interrupt Handling:** Stop the script at any time (Ctrl+C) and rest assured your categorized data up to that point is safely saved.
*   🗣️ **Informative Console Feedback:** Stay informed with clear, real-time console messages detailing processing progress, API interactions, and any warnings or errors.
*   ⚙️ **Simple Configuration:**  All key settings – from API keys to PDF paths and category labels – are easily configurable at the script's beginning.

---

## 🛠️ Challenges Overcome: Engineering for Resilience 🛠️

Developing **NeurIPS Paper Sorter** wasn't just about calling an AI API. It involved tackling real-world software engineering challenges and crafting robust solutions:

*   **🚧 The Library Version Maze:**  Initial development stumbled upon frustrating `TypeError` and `AttributeError` exceptions, stemming from inconsistencies in `google-generativeai` library versions.
    *   **💡 The Solution:**  A move to **string-based error handling** proved to be the key. By detecting errors based on keywords within exception messages (like `"429"` for rate limits and `"deadline"` for timeouts), the program became remarkably resilient to library version variations, prioritizing functionality over strict version dependencies.

*   **🚦 Taming the API Rate Limit Beast:**  Working with cloud APIs inevitably means confronting rate limits.  Unmanaged, these can halt processing and make the tool unusable.
    *   **🔑 The Solution:**  Implementing **API key rotation** and **intelligent retry logic** was crucial.  By cycling through multiple API keys and retrying requests with backoff delays, the program effectively navigates rate limits, ensuring smooth and continuous operation.

*   **💾 Ensuring Data Persistence & Real-Time Progress:**  Losing categorization progress due to interruptions or system crashes was unacceptable.  And waiting until the very end for results was inefficient.
    *   **🚀 The Solution:**  Adopting **immediate CSV saving with append mode** and incorporating **signal handling** revolutionized data management.  Results are now written to `pdf_output.csv` *after each PDF is processed*, providing real-time progress visibility and complete data safety, even if you abruptly stop the script.

**Dive Deeper:** For a detailed technical walkthrough of these challenges and their code-level solutions, read the companion blog post: [**[Link to your Detailed Blog Post Here - Coming Soon!]**] (Or: [**[Link to your Detailed Blog Post Here - Detailed Blog Post Available Here!]**])

---

## 🚀 Get Started - Categorize Your Research Today! 🚀

Ready to organize your research library with the power of Gemini AI? Follow these simple steps:

### ✅ Prerequisites

*   **🐍 Python 3.12 or Later:** Ensure you have Python 3.12+ installed. [Download Python](https://www.python.org/)
*   **📦 pip Package Installer:** `pip` is essential for installing Python packages and is typically included with Python installations.

### 🛠️ Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [Your Repository Link Here]
    cd [Your Repository Directory Name]
    ```

2.  **Highly Recommended: Create a Virtual Environment:**  Isolate project dependencies and avoid system-wide conflicts.
    ```bash
    python3.12 -m venv venv  # Create the virtual environment
    # Activate the environment:
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Required Python Packages:**
    ```bash
    pip install -r requirements.txt  # (If you have a requirements.txt file)
    # OR, if no requirements.txt:
    pip install google-generativeai PyPDF2
    ```

4.  **🔑 Set up your Gemini API Keys:**
    *   Obtain API keys from [Google AI Studio](https://makersuite.google.com/app/apikey).
    *   Configure environment variables: `GOOGLE_API_KEY`, `GOOGLE_API_KEY2`, `GOOGLE_API_KEY3` (and more if needed).
        *   **Windows:** System Environment Variables or `setx` command.
        *   **macOS/Linux:** `.bashrc`, `.zshrc`, or `export` command in your terminal.

### ⚡️ Run the NeurIPS Paper Sorter

1.  **Prepare Your PDF Folder:**  Place all the research PDFs you want to categorize into a designated folder. **Remember to update the `PDF_FOLDER_PATH` variable in `annotator.py`** to point to this folder's location on your system.

2.  **Execute the Script:**
    Open your Command Prompt/Terminal, navigate to the project directory, and run:
    ```bash
    python annotator.py
    ```

3.  **Review Categorized Results:**
    Watch the console for progress updates!  Categorization results will be saved in real-time to `pdf_output.csv` within the `D:\Data annotator\` directory (or your configured `CSV_OUTPUT_FILE` path).

4.  **Interrupt & Resume:** Feel free to stop the script with `Ctrl+C` at any point – your progress is automatically saved!

---

## ⚙️ Configuration: Tailor it to Your Needs ⚙️

Customize these variables at the top of `annotator.py` to adapt the script to your specific research domain and preferences:

```python
# --- Configuration ---
PDF_FOLDER_PATH = r'D:\scrapped-pdf'  # 📂 ⚠️ **Update this to your PDF folder!** ⚠️
LABELS = [  # 🏷️ Define your research categories here:
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
GENERIC_LABELS_PROMPT = ", ".join(LABELS) #  🤖 Gemini Prompt Label String (auto-generated from LABELS)
GEMINI_API_KEYS = [  # 🔑 Your Google Gemini API Keys (set as environment variables!)
    os.getenv("GOOGLE_API_KEY"),
    os.getenv("GOOGLE_API_KEY2"),
    os.getenv("GOOGLE_API_KEY3")
    # ... Add more keys as needed ...
]
MODEL_NAME = "gemini-1.5-flash"  # 🧠 Gemini AI Model (adjust if needed)
CSV_OUTPUT_FILE = r'D:\Data annotator\pdf_output.csv' # 📊 Path and filename for the CSV output
API_TIMEOUT_SECONDS = 90 # ⏳ API Timeout (Configuration - currently not directly used in `generate_content`)
```
⚠️ Error Handling & API Limits: Built for Resilience ⚠️
NeurIPS Paper Sorter is engineered to handle common challenges:

🚦 API Rate Limits (429 Errors): Automatic key rotation and retry mechanisms kick in to smoothly manage rate limits.
⏳ API Timeouts: Timeout errors are detected, triggering retries to ensure robust operation even with temporary API delays.
❌ PDF Reading Issues: Basic error handling is in place to gracefully manage potential problems with individual PDF files.
⏭️ Future Enhancements: The Road Ahead ⏭️
🚀 Performance Boost: Multi-threading/Asynchronous Processing: Parallel PDF processing for significantly faster categorization.
🎨 Interactive User Interface: A GUI for easier setup, real-time progress visualization, and interactive category refinement.
🔗 Seamless NeurIPS Scrapper Integration: Directly embed the categorization into the NeurIPS scraping workflow for a fully automated research pipeline.
🌳 Hierarchical & Dynamic Categories: Explore more advanced category structures and dynamic category suggestions based on paper content.
📜 License
This project is open-source and licensed under the MIT License. See the LICENSE file for full details.

✍️ Author

ibrahim3702

