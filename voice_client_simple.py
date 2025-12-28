#!/usr/bin/env python3
import os
import sys
import time
import requests
import speech_recognition as sr
from datetime import datetime
from dotenv import load_dotenv

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

load_dotenv()

CLOUD_API_URL = os.getenv('CLOUD_API_URL', 'http://localhost:8000')
DEVICE_ID = os.getenv('DEVICE_ID', 'pi-zero-2w-001')

recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=1)

print("\n" + "="*60)
print("🎙️  CDSS VOICE CLIENT - TEXT MODE")
print("="*60)
print(f"📡 Cloud API: {CLOUD_API_URL}")
print(f"🎤 Microphone: iTalk USB (index 1)")
print("="*60)

def get_voice_query():
    """Capture voice input"""
    print("\n🎤 LISTENING... Speak now!")
    print("   (Timeout: 10 seconds)")
    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        print("🔄 Processing speech...")
        query = recognizer.recognize_google(audio)
        return query
    except sr.WaitTimeoutError:
        print("❌ No speech detected (timeout)")
        return None
    except sr.UnknownValueError:
        print("❌ Could not understand speech")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def send_query_to_cloud(query):
    """Send query to API"""
    print(f"\n📤 Sending: '{query}'")
    try:
        r = requests.post(
            f"{CLOUD_API_URL}/query",
            json={
                "query": query,
                "device_id": DEVICE_ID,
                "timestamp": datetime.now().isoformat()
            },
            timeout=30
        )
        
        if r.status_code == 200:
            return r.json()
        else:
            print(f"❌ Server error: {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

# Main loop
while True:
    print("\n" + "-"*60)
    mode = input("Mode [v=voice | t=text | q=quit]: ").strip().lower()
    
    if mode in ['q', 'quit']:
        print("👋 Goodbye!")
        break
    
    # Get query
    query = None
    if mode in ['t', 'text']:
        query = input("Medical query: ").strip()
    else:
        # Voice mode
        query = get_voice_query()
        if query:
            print(f"✅ Transcribed: '{query}'")
            confirm = input("Send this? [y/n]: ").strip().lower()
            if confirm not in ['y', 'yes', '']:
                print("Cancelled")
                continue
    
    if not query:
        continue
    
    # Send to cloud and display response
    result = send_query_to_cloud(query)
    
    if result:
        response = result.get('response', 'No response')
        sources = result.get('sources', [])
        proc_time = result.get('processing_time_ms', 0)
        
        print("\n" + "="*60)
        print("📋 MEDICAL GUIDANCE:")
        print("="*60)
        print(response)
        print("="*60)
        
        if sources:
            print("\n📚 SOURCES:")
            for i, src in enumerate(sources, 1):
                conf = src.get('confidence', 0)
                title = src.get('title', 'Unknown')
                print(f"  {i}. {title} ({conf:.0%})")
        
        print(f"\n⏱️  Processing time: {proc_time}ms")
        print("="*60)

print("\n✅ Done\n")
