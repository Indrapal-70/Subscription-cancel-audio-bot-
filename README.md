# Hebrew Customer Service AI (Offline)

A complete offline Hebrew customer service system with text-to-speech, speech-to-text, and intelligent conversation handling. No OpenAI required - runs entirely on local models.

## 🚀 Features

### Core Capabilities
- **Hebrew Text Processing**: Adds Nikud (diacritics) using local ONNX model
- **Phoneme Generation**: Converts Hebrew text to IPA phonemes
- **Text-to-Speech**: Converts Hebrew text to audio (gTTS fallback)
- **Speech-to-Text**: Transcribes Hebrew audio using Vosk
- **Smart Conversation**: Handles customer service scenarios with rule-based responses
- **Web Interface**: Streamlit app for easy interaction

### Special Commands
- **Admin Override**: `admin@123 123` → "subscription cancelled"
- **Cancel Refusal**: Phrases like "don't want to cancel" → polite refusal response
- **Offline Fallback**: Works without Ollama (uses default Hebrew responses)

## 📁 Project Structure

```
cancel_subscription/
├── agents/
│   ├── nikud_agent.py          # Hebrew diacritics & phonemes
│   ├── tts_agent.py            # Text-to-speech (gTTS)
│   ├── stt_agent.py            # Speech-to-text (Vosk)
│   ├── customer_service_agent.py # Main conversation logic
│   ├── client_agent.py         # Client simulation
│   └── transcript_agent.py     # Conversation logging
├── crew_flow.py                # Agent orchestration
├── main.py                     # Console entry point
├── app.py                      # Streamlit web interface
├── requirements.txt            # Dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- Windows PowerShell
- Optional: GPU for faster processing

### Setup

1. **Clone and navigate to project**:
   ```bash
   cd cancel_subscription
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv crewai_env
   crewai_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Phonikud model**:
   - Download `phonikud-1.0.int8.onnx` from the official source
   - Place it in the project root directory
   - Or specify custom path: `NikudAgent(model_path="path/to/model.onnx")`

5. **Optional: Setup Ollama for LLM responses**:
   ```bash
   winget install ollama
   ollama serve
   ollama pull mistral
   ```

6. **Optional: Setup Vosk for STT**:
   - Download Hebrew Vosk model
   - Set environment variable: `VOSK_MODEL_PATH=C:/path/to/vosk-model-he`
   - Or pass to STTAgent: `STTAgent(model_path="C:/path/to/vosk-model-he")`

## 🎯 Usage

### Console Interface
```bash
python main.py
```

### Web Interface (Recommended)
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

### Web Interface Features

#### Text Input Tab
1. Enter Hebrew text in the text area
2. Click "Send" to process
3. View Nikud, phonemes, and agent response
4. Listen to generated audio

#### Audio Upload Tab
1. Upload a WAV file (mono, 16kHz recommended)
2. Click "Transcribe & Respond"
3. View transcription, Nikud, and response
4. Listen to generated audio

## 🔧 Configuration

### Model Paths
```python
# Custom Phonikud model
nikud_agent = NikudAgent(model_path="C:/path/to/phonikud-1.0.int8.onnx")

# Custom Vosk model
stt_agent = STTAgent(model_path="C:/path/to/vosk-model-he")
```

### Environment Variables
```bash
# Vosk model path
VOSK_MODEL_PATH=C:/path/to/vosk-model-he

# Disable HuggingFace symlink warning
HF_HUB_DISABLE_SYMLINKS_WARNING=1
```

## 🎛️ Custom Commands

### Admin Commands
- `admin@123 123` → Immediately cancels subscription

### Negative Intent Detection
The system recognizes these phrases and responds appropriately:
- English: "don't want to cancel", "cancel later", "not cancel"
- Hebrew: "לא רוצה לבטל", "לא לבטל", "לא מעוניין לבטל"

### Adding New Commands
Edit `agents/customer_service_agent.py` in the `handle_call` method:

```python
normalized = (client_text or "").strip().lower()
if normalized == "your_command":
    reply = "your_response"
    # ... rest of handling
```

## 🔍 Troubleshooting

### Common Issues

**TTS fails with "Language not supported"**:
- gTTS falls back to `iw` (Hebrew) if `he` doesn't work
- Install ffmpeg for better audio support

**STT fails with "lang he does not exist"**:
- Download Hebrew Vosk model
- Set `VOSK_MODEL_PATH` environment variable

**LLM responses not working**:
- Start Ollama: `ollama serve`
- Pull model: `ollama pull mistral`
- System uses offline fallback if Ollama unavailable

**Nikud model not found**:
- Ensure `phonikud-1.0.int8.onnx` is in project root
- Or specify custom path in `NikudAgent(model_path="...")`

### Performance Tips
- Use GPU for faster TTS (if available)
- Place models on SSD for faster loading
- Close unused applications to free memory

## 📝 Output Files

- `transcript.txt` - Conversation log
- `voices/output.wav` - Generated audio files
- Streamlit logs in terminal


## 🙏 Acknowledgments

- Phonikud for Hebrew diacritics
- Vosk for speech recognition
- gTTS for text-to-speech
- Streamlit for web interface
- CrewAI for agent orchestration