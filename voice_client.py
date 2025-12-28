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
r.pause_threshold = 1.0

m = sr.Microphone(device_index=0)

print("\n" + "="*70)
print("  CDSS VOICE CLIENT - Pi 3")
print("="*70)
print(f"Cloud API: {CLOUD_API_URL}")
print(f"Microphone: iTalk-02")
print("="*70 + "\n")

while True:
    mode = input("[v=voice | t=text | q=quit]: ").strip().lower()
    
    if mode in ['q', 'quit']:
        break
    
    if mode == 't':
        query = input("Query: ").strip()
    else:
        print("\nSpeak now:")
        try:
            with m as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10, phrase_time_limit=10)
            print("Processing...")
            query = r.recognize_google(audio)
            print(f"Heard: '{query}'")
            if input("Send? [y/n]: ").lower() not in ['y', 'yes', '']:
                continue
        except:
            print("Failed")
            continue
    
    if not query:
        continue
    
    print("Sending...")
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
    except Exception as e:
        print(f"Error: {e}")

print("Done")
