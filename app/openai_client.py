from openai import OpenAI
import os
from typing import List, Dict
import time

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=api_key)
    
    def generate_response(self, query: str, context_documents: List[str]) -> str:
        """Generate a response using GPT-4 with retrieved context"""
        
        # Build context from retrieved documents
        context = "\n\n".join([f"Protocol excerpt:\n{doc}" for doc in context_documents])
        
        system_prompt = """You are a medical AI assistant providing clinical decision support 
for emergency medical services and trauma care. You have access to Joint Trauma System 
clinical practice guidelines. Provide clear, evidence-based guidance while emphasizing 
that this is educational information and not a replacement for clinical judgment.

CRITICAL: Always include appropriate medical disclaimers and emphasize consulting 
qualified healthcare professionals for actual patient care."""

        user_prompt = f"""Based on the following medical protocols, answer this query:

Query: {query}

Available Protocols:
{context}

Provide a clear, structured response with:
1. Direct answer to the query
2. Key protocol points
3. Important considerations or contraindications
4. Source references when applicable

Remember: This is educational information only."""

        start_time = time.time()
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent medical info
            max_tokens=1000
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return response.choices[0].message.content, processing_time
