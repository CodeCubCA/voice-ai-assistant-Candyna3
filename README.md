---
title: Voice AI Assistant
emoji: 💬
colorFrom: pink
colorTo: green
sdk: streamlit
sdk_version: "1.31.0"
app_file: app.py
pinned: false
---

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Mbf-Zm77)

# Voice AI Assistant

An intelligent AI chatbot with voice input and output capabilities, powered by Google Gemini. This application provides a seamless conversational experience with support for multiple languages and AI personalities.

## 🚀 Live Deployments

Try the live application on:
- **Hugging Face Spaces**: https://huggingface.co/spaces/Candyna/Voice-ai-assistant

## Features

- **Voice Input** - Record your voice using the built-in microphone recorder with Web Speech API integration
- **Voice Output** - Listen to AI responses with natural-sounding text-to-speech using Google Text-to-Speech (gTTS)
- **AI Conversation** - Intelligent responses powered by Google Gemini 2.5 Flash
- **Multiple Personalities** - Choose from different AI personalities:
  - General Assistant - A versatile AI helper for all your questions
  - Study Buddy - Your patient learning companion
  - Fitness Coach - Your motivating fitness partner
  - Gaming Helper - Your gaming strategy advisor
- **Multi-Language Support** - Speak and receive responses in multiple languages:
  - English
  - Spanish
  - French
  - Chinese (Mandarin)
  - Japanese
- **Polished User Interface** - Beautiful, colorful design with gradient backgrounds and smooth animations

## Technologies Used

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Google Gemini API** - AI language model for intelligent responses
- **Web Speech API** - Speech recognition for voice input
- **Google Text-to-Speech (gTTS)** - Text-to-speech conversion
- **Edge TTS** - Microsoft neural voices for natural speech output
- **SpeechRecognition** - Python library for speech-to-text

## Requirements

- Python 3.8 or higher
- Google Gemini API key
- Internet connection (for API calls and speech services)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd voice-ai-assistant
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```
GEMINI_API_KEY=your_api_key_here
```

To get your Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage Guide

### Voice Input
1. Click the microphone button to start recording
2. Speak your message clearly
3. The recording will automatically stop when you're done
4. Review the transcribed text
5. Click "Send Voice Message" to send your message to the AI

### Text Input
- Simply type your message in the chat input box at the bottom of the screen
- Press Enter to send

### Changing AI Personality
- Use the dropdown menu in the sidebar to select a different AI personality
- Each personality has a unique communication style

### Changing Language
- Select your preferred language from the sidebar
- Voice input will recognize speech in the selected language
- AI responses will be in the selected language
- Voice output will use a native speaker voice

### Clearing Chat History
- Click the "Clear Chat History" button in the sidebar to start a fresh conversation

## Project Structure

```
voice-ai-assistant/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .env.example       # Example environment file
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Dependencies

```
streamlit>=1.31.0
google-generativeai>=0.3.2
python-dotenv>=1.0.0
audio-recorder-streamlit>=0.0.8
SpeechRecognition>=3.10.0
pydub>=0.25.1
edge-tts>=6.1.0
```

## License

This project is for educational purposes.

## Acknowledgments

- Google Gemini for AI capabilities
- Streamlit for the web framework
- Microsoft Edge TTS for natural voice synthesis
