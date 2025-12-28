import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from embeddings import ChromaDBClient
from dotenv import load_dotenv
import pypdf
from pathlib import Path

load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks

def ingest_pdf_directory(directory_path):
    """Ingest all PDFs in a directory"""
    
    client = ChromaDBClient()
    pdf_files = list(Path(directory_path).glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files")
    
    total_chunks = 0
    
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        # Chunk the text
        chunks = chunk_text(text)
        print(f"  Created {len(chunks)} chunks")
        
        # Prepare for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for j, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                'source': pdf_path.name,
                'chunk_id': j,
                'total_chunks': len(chunks)
            })
            ids.append(f"{pdf_path.stem}_{j}")
        
        # Add to ChromaDB
        try:
            client.add_documents(documents, metadatas, ids)
            total_chunks += len(chunks)
            print(f"  ✅ Successfully added to database")
        except Exception as e:
            print(f"  ❌ Error adding to database: {e}")
    
    print(f"\n{'='*60}")
    print(f"Ingestion complete!")
    print(f"Total documents in collection: {client.get_collection_count()}")
    print(f"Total chunks added: {total_chunks}")
    print(f"{'='*60}")

if __name__ == "__main__":
    pdf_dir = "data/jts_protocols"
    if os.path.exists(pdf_dir):
        ingest_pdf_directory(pdf_dir)
    else:
        print(f"Error: Directory {pdf_dir} not found")
