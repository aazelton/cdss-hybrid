import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from embeddings import ChromaDBClient
from dotenv import load_dotenv

load_dotenv()

def ingest_text_file(file_path, source_name):
    """Ingest a text file into ChromaDB"""
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split into chunks (simple split by paragraphs for now)
    chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
    
    # Initialize ChromaDB client
    client = ChromaDBClient()
    
    # Prepare documents, metadatas, and ids
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({
            'source': source_name,
            'chunk_id': i,
            'total_chunks': len(chunks)
        })
        ids.append(f"{source_name.replace(' ', '_')}_{i}")
    
    # Add to ChromaDB
    print(f"Adding {len(documents)} chunks from {source_name}...")
    client.add_documents(documents, metadatas, ids)
    print(f"✅ Successfully ingested {source_name}")
    print(f"Total documents in collection: {client.get_collection_count()}")

if __name__ == "__main__":
    # Test with our sample protocol
    test_file = "data/jts_protocols/test_protocol.txt"
    
    if os.path.exists(test_file):
        ingest_text_file(test_file, "Chest Pain Protocol")
    else:
        print(f"Error: {test_file} not found")
