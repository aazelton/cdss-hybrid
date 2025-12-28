#!/usr/bin/env python3
"""
Test connection to CDSS Cloud API
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLOUD_API_URL = os.getenv('CLOUD_API_URL', 'http://localhost:8000')

print("Testing CDSS Cloud API Connection")
print("="*50)
print(f"API URL: {CLOUD_API_URL}")
print("="*50)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
try:
    response = requests.get(f"{CLOUD_API_URL}/", timeout=5)
    if response.status_code == 200:
        print("✅ Root endpoint OK")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Root endpoint failed: {response.status_code}")
except Exception as e:
    print(f"❌ Root endpoint failed: {e}")

# Test 2: Health endpoint
print("\n2. Testing health endpoint...")
try:
    response = requests.get(f"{CLOUD_API_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print("✅ Health endpoint OK")
        print(f"   Status: {data.get('status')}")
        print(f"   ChromaDB: {data.get('chromadb')}")
        print(f"   OpenAI: {data.get('openai_api')}")
        print(f"   Documents: {data.get('documents_indexed')}")
    else:
        print(f"❌ Health endpoint failed: {response.status_code}")
except Exception as e:
    print(f"❌ Health endpoint failed: {e}")

# Test 3: Query endpoint
print("\n3. Testing query endpoint...")
try:
    response = requests.post(
        f"{CLOUD_API_URL}/query",
        json={
            "query": "What is the treatment for tension pneumothorax?",
            "device_id": "test-device",
            "timestamp": "2024-12-15T12:00:00"
        },
        timeout=30
    )
    if response.status_code == 200:
        data = response.json()
        print("✅ Query endpoint OK")
        print(f"   Response length: {len(data.get('response', ''))} chars")
        print(f"   Sources found: {len(data.get('sources', []))}")
        print(f"   Processing time: {data.get('processing_time_ms')}ms")
    else:
        print(f"❌ Query endpoint failed: {response.status_code}")
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"❌ Query endpoint failed: {e}")

print("\n" + "="*50)
print("Connection test complete!")
print("="*50)
