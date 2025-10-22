import os
from dotenv import load_dotenv
import google.generativeai as genai
from llama_index.llms.gemini import Gemini

load_dotenv()

def get_gemini_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("⚠️ Please set GEMINI_API_KEY in your .env file")

    genai.configure(api_key=api_key)
    gemini_llm = Gemini(
        model="gemini-2.5-pro",
        temperature=0.2,
        max_output_tokens=512
    )
    return gemini_llm
