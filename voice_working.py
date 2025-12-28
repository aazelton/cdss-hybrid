#!/usr/bin/env python3
import os
import requests
import speech_recognition as sr
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLOUD_API_URL = os.getenv('CLOUD_API_URL')
DEVICE_ID = os.getenv('DEVICE_ID')

r = sr.Recognizer()
r.energy_threshold = 300

# Use device 0 (iTalk is now card 0!)
m = sr.Microphone(device_index=0)

print("\n🎙️  CDSS Voice Client")
print(f"📡 {CLOUD_API_URL}\n")

while True:
    mode = input("[v=voice | t=text | q=quit]: ").strip().lower()
    
    if mode in ['q', 'quit']:
        break
    
    if mode == 't':
        query = input("Query: ").strip()
    else:
        print("\n🎤 Speak clearly now:")
        try:
            with m as source:
                audio = r.listen(source, timeout=10, phrase_time_limit=8)
            print("🔄 Processing...")
            query = r.recognize_google(audio)
            print(f"✅ Heard: '{query}'")
            if input("Send? [y/n]: ").lower() not in ['y', 'yes', '']:
                continue
        except Exception as e:
            print(f"❌ Failed: {e}")
            continue
    
    if not query:
        continue
    
    print("📤 Sending...")
    try:
        resp = requests.post(
            f"{CLOUD_API_URL}/query",
            json={"query": query, "device_id": DEVICE_ID, 
                  "timestamp": datetime.now().isoformat()},
            timeout=30
        )
        
        if resp.status_code == 200:
            data = resp.json()
            print("\n" + "="*60)
            print(data['response'])
            print("="*60)
            if data.get('sources'):
                print("\n📚 SOURCES:")
                for i, s in enumerate(data['sources'], 1):
                    print(f"  {i}. {s['title']} ({s['confidence']:.0%})")
            print()
    except Exception as e:
        print(f"❌ {e}")

print("\n👋 Done\n")
