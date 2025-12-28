#!/usr/bin/env python3
from embeddings import ChromaDBClient

client = ChromaDBClient()

print("="*60)
print(f"Documents in ChromaDB: {client.get_collection_count()}")
print("="*60)

# Test query
query = "RSI intubation for burn patient"
print(f"\nTest Query: {query}")
print("-"*60)

results = client.query(query, n_results=3)

if results['documents'][0]:
    print(f"Found {len(results['documents'][0])} results\n")
    
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"\nResult {i}:")
        print(f"Source: {metadata['source']}")
        print(f"Preview: {doc[:300]}...")
        print("-"*60)
else:
    print("No results found")
