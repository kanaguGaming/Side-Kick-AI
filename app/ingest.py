import fitz  # PyMuPDF
from app.db import lab_knowledge

def process_pdf(file_path: str):
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        clean_text = " ".join(text.split())
        lab_knowledge.insert_one({"text": clean_text, "source": file_path})
    return "Lab manual ingested successfully!"