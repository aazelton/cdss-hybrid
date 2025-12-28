#!/usr/bin/env python3
import os
import subprocess
import requests
import speech_recognition as sr
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CLOUD_API_URL = os.getenv('CLOUD_API_URL')
DEVICE_ID = os.getenv('DEVICE_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai_client = OpenAI(api_key=OPENAI_API_KEY)

print("\n" + "="*70)
print("  CDSS VOICE CLIENT - BLUETOOTH")
print("="*70)
print(f"Cloud: {CLOUD_API_URL}")
print("Bluetooth: OpenRun Pro by Shokz")
print("="*70 + "\n")

def listen_for_wake_word():
    """Listen for wake word using Bluetooth mic via PulseAudio"""
    print("🎤 Listening for wake word...")
    print("Say: 'HEY MEDIC' or 'MEDIC'\n")
    
    r = sr.Recognizer()
    
    while True:
        try:
            # Use default PulseAudio input (Bluetooth mic)
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=None, phrase_time_limit=3)
            
            text = r.recognize_google(audio).lower()
            
            if 'medic' in text:
                print(f"✅ Wake word: '{text}'\n")
                return True
                
        except KeyboardInterrupt:
            return False
        except:
            continue

def listen_for_query():
    """Listen for medical query"""
    print("🎤 LISTENING FOR QUERY (10 sec)...")
    print("Speak your medical question:\n")
    
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
        
        query = r.recognize_google(audio)
        print(f"✅ Query: '{query}'\n")
        return query
        
    except:
        print("❌ Could not understand\n")
        return None

def speak_response(text, voice="nova"):
    """Speak response with OpenAI TTS via Bluetooth"""
    print("🔊 Generating speech...")
    
    try:
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=1.0
        )
        
        response.stream_to_file("response.mp3")
        
        print("🔊 Playing via Bluetooth...")
        # Use paplay for PulseAudio (Bluetooth)
        subprocess.run(['paplay', 'response.mp3'])
        
        os.remove('response.mp3')
        print("✅ Done\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")

# Main loop
try:
    while True:
        # Wait for wake word
        if not listen_for_wake_word():
            break
        
        # Get query
        query = listen_for_query()
        
        if not query:
            continue
        
        # Query cloud
        print("📤 Querying protocols...")
        
        try:
            resp = requests.post(
                f"{CLOUD_API_URL}/query",
                json={"query": query, "device_id": DEVICE_ID,
                      "timestamp": datetime.now().isoformat()},
                timeout=30
            )
            
            if resp.status_code == 200:
                data = resp.json()
                response_text = data['response']
                
                # Display
                print("\n" + "="*70)
                print(response_text)
                print("="*70 + "\n")
                
                # Speak via Bluetooth
                speak_response(response_text)
                
        except Exception as e:
            print(f"❌ {e}\n")

except KeyboardInterrupt:
    print("\n\n👋 Done\n")
