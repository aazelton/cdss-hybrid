# CDSS Voice Client - Clinical Decision Support System

Voice-activated medical decision support system for austere environments. Uses Raspberry Pi 3 edge device with cloud-based AI processing.

## 🎯 Features

- 🎤 **Voice Input** - Hands-free medical queries via USB microphone
- 🔊 **Natural Speech Output** - OpenAI TTS with human-like voice
- ☁️ **Cloud Processing** - GPT-4 powered protocol retrieval
- 📚 **JTS Protocol Database** - 7,186 indexed medical documents
- 🏥 **Field-Optimized Responses** - Action-focused AUSTERE-CDS format
- ⚡ **6-13 Second Response Time** - Fast enough for field use

## 🛠️ Hardware Requirements

- **Raspberry Pi 3** (or newer)
- **USB Microphone** (tested with Audio-Technica iTalk-02)
- **Speakers or HDMI audio output**
- **Internet connection** (WiFi or Ethernet)

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/aazelton/cdss-hybrid.git
cd cdss-hybrid/cdss-client
```

### 2. System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv mpg123 alsa-utils
```

### 3. Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

Required configuration:
- `CLOUD_API_URL` - Your cloud VM endpoint
- `OPENAI_API_KEY` - OpenAI API key for TTS

### 5. Test Microphone
```bash
# List audio devices
arecord -l

# Test recording (speak for 3 seconds)
arecord -D hw:0,0 -d 3 test.wav
aplay test.wav
```

## 🚀 Usage

### Start Voice Client
```bash
source venv/bin/activate
python voice_complete.py
```

### Voice Mode

1. Type `v` for voice mode
2. Speak your medical query clearly (5 seconds)
3. Confirm the transcription
4. Receive protocol-based guidance
5. Optional: Hear response spoken aloud

### Text Mode

1. Type `t` for text mode
2. Type your medical query
3. Receive protocol-based guidance

### Example Queries

- "Treatment for tension pneumothorax"
- "RSI protocol for burn patient 100 kilograms"
- "Tourniquet application steps"
- "TXA dosing for 80kg patient"

## 🎤 Voice Settings

OpenAI TTS voices available:
- `nova` - Warm professional female (default, recommended)
- `alloy` - Neutral balanced
- `echo` - Authoritative male
- `onyx` - Deep male
- `shimmer` - Soft gentle female
- `fable` - British expressive

Change in `voice_complete.py`:
```python
speak_with_openai(response_text, voice="echo")
```

## 🏗️ System Architecture
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Raspberry Pi 3 │      │   Google Cloud   │      │   OpenAI API    │
│                 │      │       VM         │      │                 │
│  • USB Mic      │─────▶│  • FastAPI       │─────▶│  • GPT-4        │
│  • Voice Input  │      │  • ChromaDB      │      │  • TTS (nova)   │
│  • Audio Output │◀─────│  • 7,186 docs    │◀─────│                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
     Edge Device           Cloud Backend            AI Services
```

## 📁 Project Structure
```
cdss-client/
├── voice_complete.py    # Main voice client
├── .env                 # Configuration (gitignored)
├── .env.example         # Configuration template
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git exclusions
```

## 🔒 Security Notes

- **Never commit .env files** - Contains API keys
- **Use .env.example** - For sharing configuration structure
- **Rotate API keys** - If accidentally exposed
- **Firewall rules** - Restrict cloud VM access to your IP

## 🐛 Troubleshooting

### Microphone Not Detected
```bash
# Check USB devices
lsusb | grep -i audio

# List ALSA devices
arecord -l

# Update device index in code if needed
```

### Voice Recognition Fails

- Speak more slowly and clearly
- Reduce background noise
- Check internet connection (Google Speech API)
- Try simpler medical terminology

### No Audio Output
```bash
# Test speakers
speaker-test -t wav -c 2

# Check audio devices
aplay -l

# Verify mpg123 installed
which mpg123
```

### API Connection Errors

- Verify VM is running
- Check firewall rules
- Confirm correct IP in .env
- Test with: `curl http://YOUR_VM_IP:8000/health`

## 📊 Performance Metrics

- **Voice Recognition**: 90%+ accuracy with clear speech
- **Response Time**: 6-13 seconds end-to-end
- **Protocol Coverage**: 89 JTS Clinical Practice Guidelines
- **Database Size**: 7,186 indexed document chunks
- **Confidence Scoring**: 30-50% typical for relevant protocols

## 🔧 Development

### Requirements File

Create `requirements.txt`:
```
requests
SpeechRecognition
pyaudio
gTTS
python-dotenv
openai
```

### Contributing

This is a research/educational project. For improvements:
1. Fork the repository
2. Create feature branch
3. Submit pull request

## 📜 License

Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)

**Non-commercial use only.** This is a research prototype, not for clinical deployment.

## ⚠️ Medical Disclaimer

**NOT FOR CLINICAL USE**

This system is a research prototype for studying AI-assisted medical decision support. It is:
- Not FDA approved
- Not validated for clinical accuracy
- Not a substitute for medical training
- For educational and research purposes only

Always follow established medical protocols and consult qualified medical professionals.

## 👤 Author

Andrew Azelton (aazelton)
- GitHub: https://github.com/aazelton
- Project: AI in Austere Medicine Research

## 🙏 Acknowledgments

- Joint Trauma System (JTS) for clinical practice guidelines
- OpenAI for GPT-4 and TTS APIs
- Anthropic Claude for development assistance

## 📞 Support

For issues or questions:
- Open GitHub issue
- Review troubleshooting section
- Check cloud VM logs

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Status**: Research Prototype - Voice-Activated CDSS Operational
