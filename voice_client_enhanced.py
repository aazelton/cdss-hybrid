#!/usr/bin/env python3
"""
Enhanced CDSS Voice Client
- OpenAI Whisper API for speech recognition (better medical terminology)
- OpenAI TTS API for audio output
- Voice-optimized response formatting
- HDMI audio output support
"""

import os
import sys
import time
import requests
import pyaudio
import wave
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import subprocess

# Load environment variables
load_dotenv()

# Configuration
CLOUD_API_URL = os.getenv("CLOUD_API_URL", "http://xxxxxxx")
DEVICE_ID = os.getenv("DEVICE_ID", "pi-zero-2w-001")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio settings
MICROPHONE_INDEX = 0  # iTalk USB microphone
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
CHANNELS = 1
RECORD_SECONDS = 15  # Max recording time

# Voice settings
VOICE_MODE = "brief"  # "brief" or "detailed"
TTS_VOICE = "echo"  # Options: alloy, echo, fable, onyx, nova, shimmer

# Initialize OpenAI client
if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file")
    sys.exit(1)

openai_client = OpenAI(api_key=OPENAI_API_KEY)


class AudioRecorder:
    """Handle audio recording from USB microphone"""
    
    def __init__(self, device_index=MICROPHONE_INDEX):
        self.device_index = device_index
        self.audio = pyaudio.PyAudio()
        
    def record(self, duration=RECORD_SECONDS):
        """Record audio and return filename"""
        print(f"🎤 Recording for up to {duration} seconds... (speak now)")
        
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=CHUNK_SIZE
        )
        
        frames = []
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                frames.append(data)
        except KeyboardInterrupt:
            print("\n⏹️  Recording stopped by user")
        
        stream.stop_stream()
        stream.close()
        
        # Save to temporary file
        filename = f"/tmp/recording_{int(time.time())}.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"✅ Recording saved: {filename}")
        return filename
    
    def cleanup(self):
        """Clean up audio resources"""
        self.audio.terminate()


def transcribe_audio(audio_file):
    """Transcribe audio using OpenAI Whisper API"""
    print("🔄 Transcribing with Whisper API...")
    
    try:
        with open(audio_file, "rb") as f:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="en"
            )
        
        text = transcript.text.strip()
        print(f"📝 Transcribed: {text}")
        return text
    
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return None


def query_cdss(medical_query):
    """Send query to CDSS cloud API"""
    print(f"📤 Querying CDSS: {medical_query}")
    
    payload = {
        "query": medical_query,
        "device_id": DEVICE_ID,
        "timestamp": datetime.now().isoformat(),
        "voice_mode": VOICE_MODE  # Signal that response should be brief
    }
    
    try:
        response = requests.post(
            f"{CLOUD_API_URL}/query",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API error: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Query error: {e}")
        return None


def format_for_voice(response_data):
    """Extract and format response for voice output (condensed)"""
    if not response_data:
        return "No response received from the system."
    
    response_text = response_data.get("response", "")
    
    # Extract just the essential action items for voice
    lines = response_text.split('\n')
    voice_response = []
    
    # Find "WHAT TO DO NOW" section
    in_action_section = False
    in_dose_section = False
    
    for line in lines:
        if "WHAT TO DO NOW" in line:
            in_action_section = True
            continue
        elif "DOSE & VOLUME" in line:
            in_action_section = False
            in_dose_section = True
            continue
        elif "CONTRAINDICATIONS" in line or "MONITOR" in line:
            break
        
        # Only include action items
        if in_action_section and line.strip().startswith('-'):
            # Remove leading dash and clean up
            action = line.strip()[1:].strip()
            voice_response.append(action)
        
        if in_dose_section and line.strip().startswith('-'):
            dose = line.strip()[1:].strip()
            voice_response.append(dose)
    
    if voice_response:
        # Create concise spoken response
        result = ". ".join(voice_response[:4])  # Limit to first 4 items
        return result
    else:
        return "Unable to parse guidance. Please check the display."


def speak_response(text, voice=TTS_VOICE):
    """Convert text to speech and play through HDMI"""
    print(f"🔊 Generating speech (voice: {voice})...")
    
    try:
        # Generate speech with OpenAI TTS
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=1.0
        )
        
        # Save to file
        speech_file = f"/tmp/response_{int(time.time())}.mp3"
        response.stream_to_file(speech_file)
        
        print("▶️  Playing audio...")
        
        # Play through HDMI using mpg123 (lightweight, reliable)
        # Install with: sudo apt-get install mpg123
        result = subprocess.run(
            ["mpg123", "-q", speech_file],  # -q for quiet mode
            capture_output=True
        )
        
        if result.returncode != 0:
            print(f"⚠️  Audio playback warning: {result.stderr.decode()}")
            # Try alternative player
            subprocess.run(["aplay", "-q", speech_file], capture_output=True)
        
        # Cleanup
        try:
            os.remove(speech_file)
        except:
            pass
        
        print("✅ Audio playback complete")
        
    except Exception as e:
        print(f"❌ TTS error: {e}")
        print(f"📄 Text response: {text}")


def display_full_response(response_data):
    """Display full response on screen while voice plays condensed version"""
    if not response_data:
        return
    
    print("\n" + "="*60)
    print("📋 FULL MEDICAL GUIDANCE (SCREEN DISPLAY):")
    print("="*60)
    print(response_data.get("response", ""))
    print("="*60)
    
    # Show sources
    sources = response_data.get("sources", [])
    if sources:
        print("\n📚 SOURCES:")
        for i, source in enumerate(sources[:3], 1):
            title = source.get("title", "Unknown")
            conf = source.get("confidence", 0)
            print(f"  {i}. {title} ({conf:.0%})")
    
    # Processing time
    proc_time = response_data.get("processing_time_ms", 0)
    print(f"\n⏱️  Processing time: {proc_time}ms")
    print("="*60 + "\n")


def main():
    """Main voice client loop"""
    print("\n" + "="*60)
    print("🎙️  ENHANCED CDSS VOICE CLIENT")
    print("="*60)
    print(f"📡 Cloud API: {CLOUD_API_URL}")
    print(f"🎤 Microphone: iTalk USB (index {MICROPHONE_INDEX})")
    print(f"🔊 Audio Output: HDMI Monitor")
    print(f"🎯 Voice Mode: {VOICE_MODE.upper()}")
    print(f"🗣️  TTS Voice: {TTS_VOICE}")
    print("="*60)
    
    # Test audio output
    print("\n🔊 Testing audio output...")
    speak_response("CDSS voice system ready. Press V to start voice mode, T for text mode, or Q to quit.")
    
    recorder = AudioRecorder()
    
    try:
        while True:
            print("\n" + "-"*60)
            mode = input("Mode [v=voice | t=text | q=quit]: ").lower().strip()
            
            if mode == 'q':
                print("👋 Goodbye!")
                break
            
            elif mode == 'v':
                # Voice input mode
                print("\n🎙️  VOICE INPUT MODE")
                print("Press ENTER when ready to speak...")
                input()
                
                # Record audio
                audio_file = recorder.record()
                
                # Transcribe
                query_text = transcribe_audio(audio_file)
                
                # Cleanup audio file
                try:
                    os.remove(audio_file)
                except:
                    pass
                
                if not query_text:
                    print("❌ Could not understand audio. Please try again.")
                    continue
                
                # Confirm transcription
                print(f"\n✅ Heard: '{query_text}'")
                confirm = input("Is this correct? [y/n]: ").lower().strip()
                
                if confirm != 'y':
                    print("❌ Query cancelled. Please try again.")
                    continue
                
                # Query CDSS
                response_data = query_cdss(query_text)
                
                if response_data:
                    # Show full response on screen
                    display_full_response(response_data)
                    
                    # Speak condensed version
                    voice_text = format_for_voice(response_data)
                    speak_response(voice_text)
            
            elif mode == 't':
                # Text input mode
                print("\n⌨️  TEXT INPUT MODE")
                query_text = input("Medical query: ").strip()
                
                if not query_text:
                    continue
                
                # Query CDSS
                response_data = query_cdss(query_text)
                
                if response_data:
                    # Show full response on screen
                    display_full_response(response_data)
                    
                    # Option to speak response
                    speak_opt = input("Speak response? [y/n]: ").lower().strip()
                    if speak_opt == 'y':
                        voice_text = format_for_voice(response_data)
                        speak_response(voice_text)
            
            else:
                print("❌ Invalid option. Use 'v' for voice, 't' for text, or 'q' to quit.")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
    
    finally:
        recorder.cleanup()
        print("\n✅ Voice client stopped")


if __name__ == "__main__":
    main()
