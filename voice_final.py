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

print("\n" + "="*70)
print("  CDSS VOICE CLIENT")
print("="*70)
print(f"Cloud: {CLOUD_API_URL}")
print("="*70 + "\n")

while True:
    mode = input("[v=voice | t=text | q=quit]: ").strip().lower()
    
    if mode in ['q', 'quit']:
        break
    
    if mode == 't':
        query = input("Query: ").strip()
    else:
        # Record MONO at 16kHz (what the mic actually supports)
        print("\n🎤 RECORDING 5 SECONDS - SPEAK NOW!")
        result = subprocess.run(
            ['arecord', '-D', 'hw:0,0', '-d', '5', 
             '-f', 'S16_LE', '-r', '44100', '-c', '1', 'voice.wav'],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Recording failed")
            continue
        
        print("🔄 Converting to text...")
        
        r = sr.Recognizer()
        try:
            with sr.AudioFile('voice.wav') as source:
                audio = r.record(source)
            query = r.recognize_google(audio)
            print(f"✅ Heard: '{query}'")
            
            if input("Send? [y/n]: ").lower() not in ['y', 'yes', '']:
                continue
        except sr.UnknownValueError:
            print("❌ Could not understand")
            continue
        except Exception as e:
            print(f"❌ Error: {e}")
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
            print("\n" + "="*70)
            print(data['response'])
            print("="*70)
            if data.get('sources'):
                print("\nSOURCES:")
                for i, s in enumerate(data['sources'], 1):
                    print(f"  {i}. {s['title']} ({s['confidence']:.0%})")
            print()
        else:
            print(f"❌ Error: {resp.status_code}")
    except Exception as e:
        print(f"❌ {e}")

print("\nDone\n")
