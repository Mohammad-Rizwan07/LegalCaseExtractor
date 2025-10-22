
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

## Installation

1. *Clone this repository*:

```bash
git clone https://github.com/yourusername/LegalCaseExtractor.git
cd LegalCaseExtractor
```



2. *Create a virtual environment and activate it*:
```bash
python -m venv venv
```
# Windows
```bash
venv\Scripts\activate
```
# Linux / macOS
```bash
source venv/bin/activate
```

3. *Install dependencies*:
```bash
pip install -r requirements.txt
```

4. *Setup environment variables*:

Create a .env file in the project root.

Add your Gemini API key:
```bash

GEMINI_API_KEY=your_api_key_here
```

# Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

It opens the link in your browser (usually http://localhost:8501).

Upload a PDF to extract metadata and for/against points.

# Dependencies

Python 3.11

Streamlit

pdfplumber

spaCy

llama_index

google-generativeai


After installing spaCy, don’t forget to run:

```bash
python -m spacy download en_core_web_sm
```

# Project Structure 

```bash
LegalCaseExtractor/
├── app.py
├── extractor.py
├── utils.py
├── requirements.txt
├── .env.example
├── README.md
└── temp_files/   # optional, will be auto-created by app.py
```
