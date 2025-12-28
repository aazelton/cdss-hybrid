#!/usr/bin/env python3
import os
import subprocess
import requests
import speech_recognition as sr
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLOUD_API_URL = os.getenv('CLOUD_API_URL')
DEVICE_ID = os.getenv('DEVICE_ID')

print("\n🎙️  CDSS Voice Client - arecord Method")
print("="*60)

while True:
    mode = input("\n[v=voice | t=text | q=quit]: ").strip().lower()
    
    if mode in ['q', 'quit']:
        break
    
    if mode == 't':
        query = input("Query: ").strip()
    else:
        # Record with arecord (we know this works!)
        print("\n🎤 Recording 5 seconds... SPEAK NOW!")
        result = subprocess.run([
            'arecord', '-D', 'plughw:1,0', '-d', '5', 
            '-f', 'S16_LE', '-r', '16000', '-c', '1',
            'voice_query.wav'
        ], capture_output=True)
        
        if result.returncode != 0:
            print("❌ Recording failed")
            continue
        
        print("🔄 Converting speech to text...")
        
        # Use speech_recognition to convert the WAV file
        r = sr.Recognizer()
        try:
            with sr.AudioFile('voice_query.wav') as source:
                audio = r.record(source)
            query = r.recognize_google(audio)
            print(f"✅ Heard: '{query}'")
            
            confirm = input("Send this? [y/n]: ").strip().lower()
            if confirm not in ['y', 'yes', '']:
                continue
        except:
            print("❌ Could not understand speech")
            continue
    
    if not query:
        continue
    
    # Send to cloud
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
            print("📋 RESPONSE:")
            print("="*60)
            print(data['response'])
            print("="*60)
            
            if data.get('sources'):
                print("\n📚 SOURCES:")
                for i, src in enumerate(data['sources'], 1):
                    print(f"  {i}. {src['title']} ({src['confidence']:.0%})")
        else:
            print(f"❌ Error: {resp.status_code}")
    except Exception as e:
        print(f"❌ {e}")

print("\n👋 Done\n")
