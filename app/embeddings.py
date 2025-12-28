import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict

class ChromaDBClient:
    def __init__(self):
        db_path = os.getenv("CHROMADB_PATH", "./cache/chromadb")
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Create or get collection for JTS protocols
        self.collection = self.client.get_or_create_collection(
            name="jts_protocols",
            metadata={"description": "Joint Trauma System Clinical Practice Guidelines"}
        )
    
    def add_documents(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Add documents to the vector database"""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """Query the vector database"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
    
    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()
