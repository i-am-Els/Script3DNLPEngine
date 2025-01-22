import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

def clean_text(text):
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Preserve paragraph breaks
    # Merge lines that end with a word (not punctuation) followed by a single newline
    text = re.sub(r'(?<![.!?])\n(?!\n)', ' ', text)
    return text.strip()