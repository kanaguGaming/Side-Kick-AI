import os
import docx
import fitz  # PyMuPDF for PDF processing
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
chunks = []

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def load_manual_to_memory():
    global index, chunks
    data_dir = './data/' 
    all_text = ""
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        return

    # Process both .docx and .pdf files
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.endswith(".docx"):
            print(f"📖 Processing DOCX: {filename}...")
            all_text += extract_text_from_docx(file_path) + "\n\n"
        elif filename.endswith(".pdf"):
            print(f"📖 Processing PDF: {filename}...")
            all_text += extract_text_from_pdf(file_path) + "\n\n"

    if not all_text:
        print("⚠️ No lab manual files found in /data!")
        return

    # Improved text splitting for code-heavy manuals
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\nEx.No:", "\nAIM:", "\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(all_text)
    
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    print(f"✅ RAG Ready: Indexed {len(chunks)} sections.")

def get_context(query: str):
    if index is None or not chunks:
        return "No lab manual context available."
    
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding).astype('float32'), k=3)
    
    return "\n---\n".join([chunks[i] for i in I[0]])

# Initial load
load_manual_to_memory()

def get_context(query: str):
    if index is None or not chunks:
        return "No lab manual context available."
    
    # We search for the top 3 most relevant matches
    query_vector = model.encode([query]).astype('float32')
    distances, indices = index.search(query_vector, k=3)
    
    context_text = ""
    for idx in indices[0]:
        if idx < len(chunks):
            context_text += chunks[idx] + "\n---\n"
    
    return context_text