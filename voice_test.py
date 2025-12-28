#!/usr/bin/env python3
import speech_recognition as sr
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

r = sr.Recognizer()
r.energy_threshold = 100  # Lower = more sensitive
r.dynamic_energy_threshold = False

m = sr.Microphone(device_index=1)

print("\n=== MICROPHONE TEST ===\n")

# Calibrate
print("Calibrating (be quiet)...")
with m as source:
    r.adjust_for_ambient_noise(source, duration=1)
print(f"Energy threshold: {r.energy_threshold}")

# Listen
print("\nNow SPEAK LOUDLY and CLEARLY:")
print("Say: 'Hello testing one two three'\n")

with m as source:
    print(">>> LISTENING NOW <<<")
    audio = r.listen(source, timeout=10, phrase_time_limit=10)
    print(">>> Got audio! Processing...")

# Try to recognize
try:
    text = r.recognize_google(audio, language='en-US', show_all=True)
    print(f"\n✅ SUCCESS!")
    print(f"Result: {text}")
except sr.UnknownValueError:
    print("\n❌ FAILED: Could not understand audio")
    print("Try speaking LOUDER and more clearly")
except sr.RequestError as e:
    print(f"\n❌ API ERROR: {e}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
