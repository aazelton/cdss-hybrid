# Changelog

## [1.1.0] - 2024-12-28

### Added
- Bluetooth headset support for hands-free operation
- Wake word detection ("HEY MEDIC" or "MEDIC")
- OpenAI TTS integration for natural voice responses (nova voice)
- PulseAudio integration for Bluetooth audio
- Support for HSP/HFP headset profiles (microphone + speaker)
- Tested with Shokz OpenRun Pro bone conduction headset

### Changed
- Updated system prompt for ultra-concise field responses (15-30 sec spoken)
- Responses now use medic-to-medic radio traffic style
- Medication doses provided as exact mL volumes (no calculations required)
- Reduced response verbosity for voice playback

### Fixed
- Bluetooth device profile switching for microphone access
- PulseAudio source/sink detection

### Known Issues
- PyAudio + Bluetooth unreliable on Raspberry Pi 3/Zero 2W
- Recommend Pi 4+ for Bluetooth audio
- Text mode fully functional as alternative

## [1.0.0] - 2024-12-27

### Added
- Initial hybrid cloud-edge CDSS architecture
- Voice recognition using Google Speech API
- ChromaDB vector database with 7,186 JTS protocol chunks
- GPT-4 integration for medical decision support
- FastAPI cloud backend on Google Cloud VM
- Raspberry Pi edge client
- Text and voice query modes
- AUSTERE-CDS response formatting
- 89 Joint Trauma System (JTS) Clinical Practice Guidelines

### Technical Stack
- Cloud: Google Cloud e2-custom VM (4 vCPU, 17.5GB RAM)
- Database: ChromaDB vector store
- AI: OpenAI GPT-4
- Edge: Raspberry Pi 3
- Protocols: Joint Trauma System CPGs
