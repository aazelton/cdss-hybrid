from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from embeddings import ChromaDBClient
from openai_client import OpenAIClient

load_dotenv()

app = FastAPI(title="CDSS Cloud API", version="1.0.0")

try:
    chroma_client = ChromaDBClient()
    openai_client = OpenAIClient()
    print("✅ ChromaDB and OpenAI clients initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not initialize clients: {e}")
    chroma_client = None
    openai_client = None

class QueryRequest(BaseModel):
    query: str
    device_id: str
    timestamp: Optional[str] = None

class Source(BaseModel):
    title: str
    page: Optional[int] = None
    confidence: float

class QueryResponse(BaseModel):
    response: str
    sources: List[Source]
    query_type: str
    processing_time_ms: int

@app.get("/")
async def root():
    return {"message": "CDSS Cloud API", "status": "running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    chromadb_status = "connected" if chroma_client else "not_initialized"
    openai_status = "connected" if openai_client else "not_initialized"
    
    doc_count = 0
    if chroma_client:
        try:
            doc_count = chroma_client.get_collection_count()
        except:
            pass
    
    return {
        "status": "healthy",
        "chromadb": chromadb_status,
        "openai_api": openai_status,
        "documents_indexed": doc_count,
        "version": "1.0.0"
    }

@app.post("/query")
async def process_query(request: QueryRequest):
    if not chroma_client or not openai_client:
        raise HTTPException(status_code=503, detail="Services not fully initialized")
    
    try:
        results = chroma_client.query(request.query, n_results=3)
        
        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []
        distances = results["distances"][0] if results["distances"] else []
        
        if not documents:
            return {
                "response": "No relevant protocols found in the database.",
                "sources": [],
                "query_type": "no_results",
                "processing_time_ms": 0
            }
        
        response_text, processing_time = openai_client.generate_response(request.query, documents)
        
        sources = []
        for i, (metadata, distance) in enumerate(zip(metadatas, distances)):
            confidence = max(0.0, 1.0 - distance)
            sources.append({
                "title": metadata.get("source", f"Protocol {i+1}"),
                "page": metadata.get("page"),
                "confidence": round(confidence, 2)
            })
        
        return {
            "response": response_text,
            "sources": sources,
            "query_type": "chromadb",
            "processing_time_ms": processing_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
