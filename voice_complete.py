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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # We'll add this to .env

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

print("\n" + "="*70)
print("  CDSS VOICE CLIENT - OPENAI TTS")
print("="*70)
print(f"Cloud: {CLOUD_API_URL}")
print("="*70 + "\n")

def speak_with_openai(text, voice="nova"):
    """
    Generate natural speech with OpenAI TTS
    Voices: alloy, echo, fable, onyx, nova, shimmer
    nova = warm female voice (recommended for medical)
    """
    print(f"🔊 Generating speech (OpenAI {voice})...")
    
    try:
        response = openai_client.audio.speech.create(
            model="tts-1",  # or "tts-1-hd" for higher quality
            voice=voice,
            input=text,
            speed=1.0  # 0.25 to 4.0 (1.0 is normal)
        )
        
        # Save to file
        response.stream_to_file("response.mp3")
        
        # Play through speakers
        subprocess.run(['mpg123', '-q', 'response.mp3'])
        
        # Cleanup
        os.remove('response.mp3')
        print("✅ Playback complete")
        
    except Exception as e:
        print(f"❌ TTS Error: {e}")

while True:
    mode = input("[v=voice | t=text | q=quit]: ").strip().lower()
    
    if mode in ['q', 'quit']:
        break
    
    if mode == 't':
        query = input("Query: ").strip()
    else:
        # Record voice
        print("\n🎤 RECORDING 5 SECONDS - SPEAK NOW!")
        result = subprocess.run(
            ['arecord', '-D', 'hw:0,0', '-d', '5', 
             '-f', 'S16_LE', '-r', '44100', '-c', '1', 'voice.wav'],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print("❌ Recording failed")
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
            response_text = data['response']
            
            # Display on screen
            print("\n" + "="*70)
            print(response_text)
            print("="*70)
            
            if data.get('sources'):
                print("\nSOURCES:")
                for i, s in enumerate(data['sources'], 1):
                    print(f"  {i}. {s['title']} ({s['confidence']:.0%})")
            print()
            
            # Speak the response with OpenAI TTS
            speak = input("🔊 Speak response? [y/n]: ").strip().lower()
            if speak in ['y', 'yes', '']:
                speak_with_openai(response_text, voice="nova")
            
        else:
            print(f"❌ Error: {resp.status_code}")
    except Exception as e:
        print(f"❌ {e}")

print("\nDone\n")
