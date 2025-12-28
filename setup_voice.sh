#!/bin/bash
# Setup script for Enhanced CDSS Voice Client
# Run on Raspberry Pi

echo "======================================================"
echo "🎙️  CDSS Enhanced Voice Client Setup"
echo "======================================================"

# Check if running on Pi
if [ ! -d ~/cdss-client ]; then
    echo "❌ Error: ~/cdss-client directory not found"
    echo "Please run this script on your Raspberry Pi"
    exit 1
fi

cd ~/cdss-client

echo ""
echo "Step 1: Installing system dependencies..."
echo "------------------------------------------------------"
sudo apt-get update
sudo apt-get install -y mpg123 alsa-utils

echo ""
echo "Step 2: Testing HDMI audio output..."
echo "------------------------------------------------------"
# Set HDMI as default audio output
amixer cset numid=3 2  # 2 = HDMI, 1 = headphone jack

# Test audio
speaker-test -t wav -c 2 -l 1 2>/dev/null

echo ""
echo "Step 3: Checking Python environment..."
echo "------------------------------------------------------"
source venv/bin/activate

# Install/upgrade required packages
pip install --upgrade openai requests pyaudio python-dotenv

echo ""
echo "Step 4: Configuring environment..."
echo "------------------------------------------------------"

# Check if OPENAI_API_KEY exists in .env
if grep -q "OPENAI_API_KEY" .env; then
    echo "✅ OPENAI_API_KEY found in .env"
else
    echo ""
    echo "⚠️  OPENAI_API_KEY not found in .env file"
    echo "You need to add your OpenAI API key to use Whisper and TTS"
    echo ""
    read -p "Enter your OpenAI API key (or press Enter to skip): " api_key
    
    if [ ! -z "$api_key" ]; then
        echo "OPENAI_API_KEY=$api_key" >> .env
        echo "✅ Added OPENAI_API_KEY to .env"
    else
        echo "⚠️  Skipped - you'll need to add this manually later"
    fi
fi

echo ""
echo "Step 5: Testing microphone..."
echo "------------------------------------------------------"
python3 << EOF
import pyaudio
import sys

try:
    audio = pyaudio.PyAudio()
    print("\nAvailable audio devices:")
    print("-" * 60)
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"  [{i}] {info['name']}")
            if 'italk' in info['name'].lower() or 'usb' in info['name'].lower():
                print(f"      ✅ This looks like your USB microphone!")
    print("-" * 60)
    audio.terminate()
except Exception as e:
    print(f"❌ Error checking audio devices: {e}")
    sys.exit(1)
EOF

echo ""
echo "======================================================"
echo "✅ Setup Complete!"
echo "======================================================"
echo ""
echo "Next steps:"
echo "1. Copy the new voice client:"
echo "   scp voice_client_enhanced.py admin@raspberrypi:~/cdss-client/"
echo ""
echo "2. Update the VM server files (from your Mac/local machine):"
echo "   scp main_enhanced.py akaclinicalco@35.202.102.233:~/cdss-cloud/app/main.py"
echo "   scp openai_client_enhanced.py akaclinicalco@35.202.102.233:~/cdss-cloud/app/openai_client.py"
echo ""
echo "3. Restart the VM server:"
echo "   ssh akaclinicalco@35.202.102.233"
echo "   cd ~/cdss-cloud/app"
echo "   source ~/cdss-cloud/venv/bin/activate"
echo "   python main.py"
echo ""
echo "4. Test the enhanced voice client:"
echo "   cd ~/cdss-client"
echo "   source venv/bin/activate"
echo "   python voice_client_enhanced.py"
echo ""
echo "======================================================"
echo "For voice configuration, check .env file:"
echo "  - TTS_VOICE options: alloy, echo, fable, onyx, nova, shimmer"
echo "  - VOICE_MODE: brief (default) or detailed"
echo "======================================================"
