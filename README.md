
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
## 🎧 Bluetooth Headset Support

The system supports Bluetooth headsets with both microphone and speaker capabilities for hands-free operation in field environments.

### Bluetooth Requirements

**Supported Profiles:**
- A2DP (Advanced Audio Distribution Profile) - for high-quality audio playback
- HSP/HFP (Headset/Hands-Free Profile) - for microphone input

**Tested Devices:**
- ✅ Shokz OpenRun Pro (bone conduction headset)
- ✅ Any Bluetooth headset supporting both A2DP and HSP/HFP profiles

**NOT Supported:**
- BLE-only devices without A2DP audio profile
- Fitness trackers with Bluetooth alerts only

### Bluetooth Setup (Raspberry Pi 3/4)
```bash
# Install Bluetooth audio support
sudo apt-get install -y pulseaudio pulseaudio-module-bluetooth bluez-tools

# Start PulseAudio
pulseaudio --start

# Pair headset
bluetoothctl
> power on
> agent on
> scan on
# Wait for device to appear
> pair XX:XX:XX:XX:XX:XX
> trust XX:XX:XX:XX:XX:XX
> connect XX:XX:XX:XX:XX:XX

# Switch to headset profile (enables microphone)
pactl set-card-profile bluez_card.XX_XX_XX_XX_XX_XX handsfree_head_unit

# Verify devices
pactl list sources short  # Should show Bluetooth mic
pactl list sinks short    # Should show Bluetooth speaker
```

### Known Issues

**Raspberry Pi 3/Zero 2W Bluetooth Audio:**
- PyAudio + PulseAudio + Bluetooth can be unreliable on Pi 3/Zero 2W
- Recommend Raspberry Pi 4 or newer for better Bluetooth audio stack
- Alternative: Use USB microphone + Bluetooth speakers
- Or use text interface (fully functional, no audio issues)

**Workaround for Pi 3:**
Text mode provides 100% reliable operation:
```bash
python cdss_final.py
```
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
=======
# CDSS Hybrid - Clinical Decision Support System
### AI-Powered Medical Protocol Assistant for Austere Environments

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: Research](https://img.shields.io/badge/status-research%20proof%20of%20concept-orange.svg)]()

---

## ⚠️ IMPORTANT MEDICAL DISCLAIMER

**THIS IS A RESEARCH PROOF OF CONCEPT - NOT FOR CLINICAL USE**

- ❌ NOT intended for actual patient care decisions
- ❌ NOT FDA approved or clinically validated  
- ❌ NOT a replacement for qualified medical professionals
- ✅ FOR research, education, and demonstration purposes ONLY

**Always consult qualified healthcare professionals for patient care.**

---

## Overview

CDSS Hybrid is an open-source clinical decision support system demonstrating AI-assisted medical protocols for austere environments. Built with a hybrid cloud-edge architecture, it provides instant access to medical protocols while maintaining offline capability.

This proof-of-concept uses Joint Trauma System (JTS) clinical practice guidelines as example, but **works with ANY medical protocols** - simply replace the PDFs with your organization's guidelines.

### Key Features

🎤 **Voice-Activated Interface** - Hands-free operation for field use  
☁️ **Hybrid Architecture** - Cloud AI + edge computing for resilience  
📴 **Offline Capable** - Critical protocols cached locally  
🔄 **Protocol-Agnostic** - Works with any PDF-based guidelines  
🤖 **AI-Powered** - OpenAI GPT-4 or any compatible LLM API  
🧠 **Self-Optimizing** - Learns usage patterns to improve caching  
🌐 **Web Demo** - Test without installation  
🔓 **Open Source** - CC BY-NC 4.0 License (non-commercial use)

---

## Quick Start

### Prerequisites
- Cloud VM (Google Cloud, AWS, Azure, DigitalOcean)
- OpenAI API key
- Python 3.10+

### Installation
```bash
# Clone repository
git clone https://github.com/aazelton/cdss-hybrid.git
cd cdss-hybrid

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Ingest your protocol PDFs
python scripts/ingest_pdfs.py

# Run the server
python app/main.py
```

> **Note:** Detailed deployment guide coming soon.

---

## Architecture
```
Cloud VM (AI Backend)          Edge Device (Voice Interface)
├── ChromaDB Vector DB    ←→   ├── Speech Recognition
├── OpenAI GPT-4                ├── Text-to-Speech  
├── REST API                    ├── Local Cache
└── Protocol Management         └── Offline Fallback
```

---

## Use Your Own Protocols

**This system is protocol-agnostic!** Replace PDFs with ANY medical guidelines:
- Hospital protocols
- EMS guidelines  
- Wilderness medicine
- Nursing protocols
- Veterinary medicine
- **Any PDF-based knowledge base**

Simply place PDFs in `data/protocols/` and run ingestion script.

---

## Example Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Management of tension pneumothorax in field settings", "device_id": "test"}'
```

**Response:**
AI-generated medical guidance with source citations from your protocol database.

---

## Technology Stack

- **Backend:** FastAPI (Python)
- **Vector DB:** ChromaDB
- **AI/LLM:** OpenAI GPT-4 (swappable - use Claude, Gemini, local models, etc.)
- **PDF Processing:** pypdf
- **Voice:** SpeechRecognition + pyttsx3

**Works with any LLM API** - easily swap OpenAI for Anthropic Claude, Google Gemini, or local models.

---

## Documentation

- **Quick Start** - See installation section above
- **Hardware Setup** - See deployment options below
- **API Documentation** - REST API reference (coming soon)
- **Contributing** - See contributing section below

---

## Use Cases

- **Austere Medical Environments** - Remote clinics, disaster response, wilderness medicine
- **Research** - Study AI integration in clinical workflows
- **Education** - Medical training simulations, protocol familiarization
- **Field Medicine** - Combat/tactical medicine, mobile medical units

---

## Deployment Options

### Cloud Only ($30-50/month)
Access via web browser or API

### Cloud + Raspberry Pi ($50-100 one-time + $30-50/month)
Voice-activated field device with offline capability

> **Note:** Complete hardware setup guide coming soon. For now, you'll need a Raspberry Pi with microphone input and network connectivity to your cloud VM.

---

## License

**CC BY-NC 4.0** - Creative Commons Attribution-NonCommercial 4.0 International

✅ **Free for non-commercial use** - research, education, personal projects  
✅ **Can modify and share** with attribution  
❌ **NO commercial use** without written permission  

**For commercial licensing:** Contact @aazelton

See [LICENSE](LICENSE) for full terms.

---

## Medical & Legal Disclaimer

This software is provided **"AS IS"** for research and educational purposes only.

- **NOT** a medical device
- **NOT** FDA approved
- **NOT** clinically validated  
- **NOT** for patient care decisions

Users assume **ALL risk**. Always consult qualified healthcare professionals for patient care.

---

## Contributing

We welcome contributions! This project benefits the medical and research communities.

### How to Contribute
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

We welcome contributions! Please ensure your code follows the project's style and includes appropriate tests.

---

## Acknowledgments

- **Joint Trauma System** - Clinical practice guidelines
- **OpenAI** - GPT-4 API
- **Open source community**
- **Medical professionals** providing feedback

---

## Contact

**Creator:** Andrew Azelton  azelton@proton.me
**GitHub:** [@aazelton](https://github.com/aazelton)  
**Project:** https://github.com/aazelton/cdss-hybrid

💬 [Discussions](https://github.com/aazelton/cdss-hybrid/discussions) | 🐛 [Issues](https://github.com/aazelton/cdss-hybrid/issues)

---

⭐ **Star this repo** if you find it useful!  
🔄 **Share** with medical and tech communities  
🤝 **Contribute** to advance the project

**Built for the medical, emergency services, and research communities**

**Remember: Research tool only. Always consult qualified healthcare professionals for patient care.**
>>>>>>> 3c1a495caeaede076de1a5e4fc36e70dc629bfde
