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

**Creator:** Andrew Zelton  
**GitHub:** [@aazelton](https://github.com/aazelton)  
**Project:** https://github.com/aazelton/cdss-hybrid

💬 [Discussions](https://github.com/aazelton/cdss-hybrid/discussions) | 🐛 [Issues](https://github.com/aazelton/cdss-hybrid/issues)

---

⭐ **Star this repo** if you find it useful!  
🔄 **Share** with medical and tech communities  
🤝 **Contribute** to advance the project

**Built for the medical, emergency services, and research communities**

**Remember: Research tool only. Always consult qualified healthcare professionals for patient care.**
