#!/usr/bin/env python3
"""
Text Client for CDSS - Keyboard input testing
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLOUD_API_URL = os.getenv('CLOUD_API_URL', 'http://localhost:8000')
DEVICE_ID = os.getenv('DEVICE_ID', 'pi-zero-2w-001')

def send_query(query_text):
    """Send query to cloud API"""
    try:
        response = requests.post(
            f"{CLOUD_API_URL}/query",
            json={
                "query": query_text,
                "device_id": DEVICE_ID,
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return None

def main():
    print("="*60)
    print("CDSS Text Client")
    print(f"Cloud API: {CLOUD_API_URL}")
    print(f"Device ID: {DEVICE_ID}")
    print("="*60)
    print("\nType your queries below. Type 'quit' to exit.\n")
    
    while True:
        query = input("\n🔍 Query: ")
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not query.strip():
            continue
        
        print("\n📤 Sending query...")
        result = send_query(query)
        
        if result:
            print("\n" + "="*60)
            print("📋 RESPONSE:")
            print("-"*60)
            print(result.get('response', 'No response'))
            print("-"*60)
            
            sources = result.get('sources', [])
            if sources:
                print("\n📚 SOURCES:")
                for i, source in enumerate(sources, 1):
                    title = source.get('title', 'Unknown')
                    confidence = source.get('confidence', 0)
                    page = source.get('page')
                    page_str = f" (page {page})" if page else ""
                    print(f"  {i}. {title}{page_str} - {confidence:.0%} confidence")
            
            processing_time = result.get('processing_time_ms', 0)
            print(f"\n⏱️  Processing time: {processing_time}ms")
            print("="*60)

if __name__ == "__main__":
    main()
