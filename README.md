# LegalCaseExtractor


LegalCaseExtractor/
├── app.py
├── extractor.py
├── utils.py
├── requirements.txt
├── .env.example
├── README.md
└── temp_files/   # optional, will be auto-created by app.py



# ⚖️ Legal Case Extractor - For & Against Points

A Python-based Streamlit web application to extract and analyze **legal case PDFs**. The app summarizes text, extracts metadata, entities, keywords, questions, and generates **For & Against points** from case sections using AI.

---

## Features

- Upload legal case PDFs and extract clean text.
- Automatically split the text into manageable sections.
- Extract metadata per section:
  - Title
  - Summary
  - Keywords
  - Questions
  - Named Entities
- Generate **For & Against points** from each section.
- Interactive Streamlit interface for preview and exploration.

---

## Screenshots

*(Add screenshots here if available)*

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/LegalCaseExtractor.git
cd LegalCaseExtractor



2.Create a virtual environment and activate it:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

3.Install dependencies:

pip install -r requirements.txt


4.Setup environment variables:

Create a .env file in the project root.

Add your Gemini API key:

GEMINI_API_KEY=your_api_key_here


Usage

Run the Streamlit app:

streamlit run app.py


Open the link in your browser (usually http://localhost:8501).

Upload a PDF to extract metadata and for/against points.

Dependencies

Python 3.11

Streamlit

pdfplumber

spaCy

llama_index

google-generativeai


After installing spaCy, don’t forget to run:

```bash
python -m spacy download en_core_web_sm
.env.example
ini
Copy code
# Copy this file to .env and add your Gemini API key
GEMINI_API_KEY=your_api_key_here
