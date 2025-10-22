import re
import pdfplumber
from tqdm import tqdm
import spacy
import json

from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import (
    TitleExtractor,
    SummaryExtractor,
    KeywordExtractor,
    QuestionsAnsweredExtractor
)
from llama_index.core.schema import TextNode  # ✅ Correct node type

from utils import get_gemini_llm

# Load spaCy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in tqdm(pdf.pages, desc="Extracting PDF"):
            text += page.extract_text() or ""
    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,;:?!\s]', '', text)
    return text.strip()

def build_nodes(text):
    splitter = SentenceSplitter(chunk_size=512)
    chunks = splitter.split_text(text)
    # ✅ Use TextNode instead of Document
    return [TextNode(text=chunk, metadata={"source": "pdf"}) for chunk in chunks]

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def extract_metadata(nodes):
    try:
        gemini_llm = get_gemini_llm()
        Settings.llm = gemini_llm
        llm_available = True
    except Exception as e:
        print("⚠️ Gemini unavailable, using fallback summarizer:", e)
        gemini_llm = None
        llm_available = False

    title_extractor = TitleExtractor(llm=gemini_llm) if llm_available else None
    summary_extractor = SummaryExtractor(llm=gemini_llm) if llm_available else None
    keyword_extractor = KeywordExtractor(llm=gemini_llm) if llm_available else None
    question_extractor = QuestionsAnsweredExtractor(llm=gemini_llm) if llm_available else None

    results = []

    for node in tqdm(nodes, desc="Extracting metadata"):
        clean_node_text = clean_text(node.text)
        entities = extract_entities(clean_node_text)

        try:
            # Basic metadata
            metadata = {
                "title": title_extractor.extract([node])[0] if title_extractor else "Untitled",
                "summary": summary_extractor.extract([node])[0] if summary_extractor else clean_node_text[:250] + "...",
                "keywords": keyword_extractor.extract([node])[0] if keyword_extractor else [],
                "questions": question_extractor.extract([node])[0] if question_extractor else [],
                "entities": entities,
            }

            # ✅ Extract For & Against points
            if llm_available:
                prompt = f"""
                Read this legal case section:
                ---
                {clean_node_text}
                ---
                Identify key points FOR (supporting arguments) and AGAINST (opposing arguments).
                Return JSON like:
                {{
                  "for_points": ["point1", "point2"],
                  "against_points": ["point1", "point2"]
                }}
                """
                response = gemini_llm.complete(prompt).text
                try:
                    parsed = json.loads(response)
                    metadata["for_points"] = parsed.get("for_points", [])
                    metadata["against_points"] = parsed.get("against_points", [])
                except Exception:
                    metadata["for_points"] = []
                    metadata["against_points"] = []
            else:
                # Fallback heuristic
                metadata["for_points"] = [sent for sent in clean_node_text.split('.') if 'support' in sent.lower() or 'agree' in sent.lower()]
                metadata["against_points"] = [sent for sent in clean_node_text.split('.') if 'oppose' in sent.lower() or 'disagree' in sent.lower()]

        except Exception as e:
            metadata = {
                "title": "Untitled",
                "summary": clean_node_text[:250] + "...",
                "keywords": [],
                "questions": [],
                "entities": entities,
                "for_points": [],
                "against_points": [],
                "error": str(e)
            }

        results.append({"text": clean_node_text, "metadata": metadata})

    return results
