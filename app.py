import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
import tempfile
import edge_tts
import asyncio

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Language configurations
LANGUAGES = {
    "English": {
        "code": "en",
        "stt_code": "en-US",
        "tts_voice": "en-US-JennyNeural",
        "flag": "🇺🇸",
        "ai_instruction": "Respond in English."
    },
    "Spanish": {
        "code": "es",
        "stt_code": "es-ES",
        "tts_voice": "es-ES-ElviraNeural",
        "flag": "🇪🇸",
        "ai_instruction": "Responde en español. (Respond in Spanish.)"
    },
    "French": {
        "code": "fr",
        "stt_code": "fr-FR",
        "tts_voice": "fr-FR-DeniseNeural",
        "flag": "🇫🇷",
        "ai_instruction": "Réponds en français. (Respond in French.)"
    },
    "Chinese (Mandarin)": {
        "code": "zh",
        "stt_code": "zh-CN",
        "tts_voice": "zh-CN-XiaoxiaoNeural",
        "flag": "🇨🇳",
        "ai_instruction": "用中文回复。(Respond in Mandarin Chinese.)"
    },
    "Japanese": {
        "code": "ja",
        "stt_code": "ja-JP",
        "tts_voice": "ja-JP-NanamiNeural",
        "flag": "🇯🇵",
        "ai_instruction": "日本語で返答してください。(Respond in Japanese.)"
    }
}

# Personality prompts
PERSONALITIES = {
    "General Assistant": {
        "name": "General Assistant",
        "prompt": "You are a helpful and friendly AI assistant. Provide clear, accurate, and helpful responses to any questions or tasks.",
        "icon": "🤖",
        "description": "A versatile AI helper for all your questions"
    },
    "Study Buddy": {
        "name": "Study Buddy",
        "prompt": "You are a patient and encouraging study companion. Help users learn by explaining concepts clearly, providing examples, and asking questions to check understanding. Break down complex topics into digestible parts.",
        "icon": "📚",
        "description": "Your patient learning companion"
    },
    "Fitness Coach": {
        "name": "Fitness Coach",
        "prompt": "You are an enthusiastic and motivating fitness coach. Provide workout advice, nutrition tips, and encouragement. Focus on health, safety, and sustainable fitness habits. Always remind users to consult healthcare professionals for medical concerns.",
        "icon": "💪",
        "description": "Your motivating fitness partner"
    },
    "Gaming Helper": {
        "name": "Gaming Helper",
        "prompt": "You are an experienced gaming enthusiast. Help with game strategies, tips, walkthroughs, and recommendations. Be excited about gaming while providing practical advice.",
        "icon": "🎮",
        "description": "Your gaming strategy advisor"
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot with Gemini",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for fun colorful styling
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #f0f8ff 50%, #f0fff0 100%);
    }

    /* Sidebar styling - pink theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffb6c1 0%, #ffc0cb 50%, #ffe4e1 100%);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #8b008b;
    }

    /* User message bubble - light blue */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #87ceeb 0%, #add8e6 100%);
        border-radius: 20px;
        padding: 10px;
        margin: 10px 0;
        border: 2px solid #4169e1;
    }

    /* Assistant message bubble - lime green */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: linear-gradient(135deg, #98fb98 0%, #90ee90 100%);
        border-radius: 20px;
        padding: 10px;
        margin: 10px 0;
        border: 2px solid #32cd32;
    }

    /* Chat input styling - pink border */
    [data-testid="stChatInput"] {
        border: 3px solid #ff69b4 !important;
        border-radius: 25px !important;
    }

    [data-testid="stChatInput"] textarea {
        border-radius: 20px !important;
    }

    /* Button styling - gradient pink */
    .stButton > button {
        background: linear-gradient(90deg, #ff69b4, #ff1493);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #ff1493, #ff69b4);
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.4);
    }

    /* Primary button - lime green gradient */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #32cd32, #7cfc00);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #7cfc00, #32cd32);
        box-shadow: 0 5px 15px rgba(50, 205, 50, 0.4);
    }

    /* Audio player styling */
    audio {
        border-radius: 25px;
        width: 100%;
    }

    /* Title styling */
    h1 {
        background: linear-gradient(90deg, #ff69b4, #87ceeb, #98fb98);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Info boxes */
    [data-testid="stAlert"] {
        border-radius: 15px;
        border-left: 5px solid #ff69b4;
    }

    /* Success message - lime green */
    .stSuccess {
        background-color: #98fb98 !important;
        border-left: 5px solid #32cd32 !important;
    }

    /* Selectbox styling */
    [data-testid="stSelectbox"] {
        border-radius: 15px;
    }

    /* Microphone button area */
    .stColumn {
        padding: 5px;
    }

    /* Footer text */
    .stMarkdown div[style*="text-align: center"] {
        background: linear-gradient(90deg, #ffb6c1, #87ceeb, #98fb98);
        padding: 10px;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "language" not in st.session_state:
    st.session_state.language = "English"

if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# TTS session state variables
if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}  # Store generated audio by message index

if "processing" not in st.session_state:
    st.session_state.processing = False

if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None

if "last_transcription" not in st.session_state:
    st.session_state.last_transcription = None

# Function to transcribe audio
def transcribe_audio(audio_bytes, language_code="en-US"):
    """Convert audio bytes to text using speech recognition"""
    if audio_bytes is None:
        return None

    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()

        # The audio_recorder returns WAV format audio
        # We need to use AudioFile to properly read it
        audio_file = io.BytesIO(audio_bytes)

        with sr.AudioFile(audio_file) as source:
            # Read the audio data from the file
            audio_data = recognizer.record(source)

        # Recognize speech using Google Speech Recognition with specified language
        text = recognizer.recognize_google(audio_data, language=language_code)
        return text
    except sr.UnknownValueError:
        return None  # Return None so we can show a better message
    except sr.RequestError as e:
        return f"Speech service error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate TTS audio using Edge TTS (natural human-like voices)
async def generate_tts_async(text, output_file, voice="en-US-JennyNeural"):
    """Async function to generate TTS using Edge TTS"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def generate_tts_audio(text, voice="en-US-JennyNeural"):
    """Convert text to speech using Edge TTS and return audio bytes"""
    try:
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            tmp_filename = tmp_file.name

        # Run the async TTS generation with the specified voice
        asyncio.run(generate_tts_async(text, tmp_filename, voice))

        # Read the audio file
        with open(tmp_filename, 'rb') as f:
            audio_data = f.read()

        # Clean up temp file
        os.unlink(tmp_filename)

        return audio_data
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.markdown("---")

    # Personality selector
    st.subheader("Choose AI Personality")
    selected_personality = st.selectbox(
        "Select a personality:",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality),
        key="personality_selector"
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history on personality change
        st.session_state.tts_audio = {}  # Clear TTS audio cache
        st.rerun()

    # Display current personality info
    current = PERSONALITIES[st.session_state.personality]
    st.info(f"{current['icon']} **{current['name']}**\n\n{current['description']}")

    st.markdown("---")

    # Language selector
    st.subheader("Choose Language")
    language_options = list(LANGUAGES.keys())
    selected_language = st.selectbox(
        "Select a language:",
        options=language_options,
        index=language_options.index(st.session_state.language),
        format_func=lambda x: f"{LANGUAGES[x]['flag']} {x}",
        key="language_selector"
    )

    # Update language if changed
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.session_state.messages = []  # Clear chat history on language change
        st.session_state.tts_audio = {}  # Clear TTS audio cache
        st.rerun()

    # Display current language info
    current_lang = LANGUAGES[st.session_state.language]
    st.info(f"{current_lang['flag']} **{st.session_state.language}**\n\nVoice input and output will use this language.")

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.tts_audio = {}  # Clear TTS audio cache
        st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.markdown("Powered by Google Gemini 2.5 Flash")
    st.markdown("Built with Streamlit")

# Main chat interface
st.title(f"{PERSONALITIES[st.session_state.personality]['icon']} {st.session_state.personality}")
st.markdown("Ask me anything! I'm here to help.")

# Voice input section
st.markdown("### 🎤 Voice Input")
col1, col2 = st.columns([1, 4])

with col1:
    audio_bytes = audio_recorder(
        text="Click to record",
        recording_color="#ff1493",  # Deep pink when recording
        neutral_color="#ff69b4",    # Hot pink to match background theme
        icon_name="microphone",
        icon_size="2x",
    )

with col2:
    # Only process if we have new audio (different from last processed)
    if audio_bytes and audio_bytes != st.session_state.last_audio_bytes:
        with st.spinner("🎙️ Processing your voice input..."):
            # Get the current language's STT code
            stt_language = LANGUAGES[st.session_state.language]["stt_code"]
            transcribed = transcribe_audio(audio_bytes, stt_language)
            st.session_state.last_audio_bytes = audio_bytes
            # Store the transcribed text for later use
            if transcribed and not transcribed.startswith("Error:") and not transcribed.startswith("Speech service error:"):
                st.session_state.last_transcription = transcribed
            else:
                st.session_state.last_transcription = None

        if transcribed is None:
            st.warning("Could not understand the audio. Please try again and speak clearly.")
        elif transcribed.startswith("Error:") or transcribed.startswith("Speech service error:"):
            st.error(transcribed)
        else:
            st.success(f"**Transcribed:** {transcribed}")
            st.info("💡 Click the button below to send, or copy the text to edit first!")

    # Show send button if we have a valid transcription
    if "last_transcription" in st.session_state and st.session_state.last_transcription:
        if st.button("📤 Send Voice Message", type="primary", use_container_width=True):
            st.session_state.voice_message = st.session_state.last_transcription
            st.session_state.last_transcription = None
            st.session_state.last_audio_bytes = None  # Reset for next recording
            st.rerun()

# Display chat history with TTS audio players
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Show audio player for assistant messages OUTSIDE chat_message container
    if message["role"] == "assistant":
        # Generate TTS audio if not already cached
        if idx not in st.session_state.tts_audio:
            with st.spinner("🔊 Generating audio..."):
                # Get the current language's TTS voice
                tts_voice = LANGUAGES[st.session_state.language]["tts_voice"]
                audio_data = generate_tts_audio(message["content"], tts_voice)
                if audio_data:
                    st.session_state.tts_audio[idx] = audio_data

        # Display audio player if audio exists
        if idx in st.session_state.tts_audio:
            st.audio(st.session_state.tts_audio[idx], format="audio/mp3")

# Handle voice message if available
if "voice_message" in st.session_state and st.session_state.voice_message:
    prompt = st.session_state.voice_message
    st.session_state.voice_message = None
    # Reset processing flag when handling voice message
    st.session_state.processing = False
else:
    # Regular chat input
    prompt = st.chat_input("Type your message here or use voice input above...")

# Reset processing flag if it got stuck
if st.session_state.processing and not prompt:
    st.session_state.processing = False

if prompt and not st.session_state.processing:
    # Set processing flag to prevent duplicate processing
    st.session_state.processing = True

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create model with personality-based system instruction + language instruction
                personality_prompt = PERSONALITIES[st.session_state.personality]["prompt"]
                language_instruction = LANGUAGES[st.session_state.language]["ai_instruction"]
                combined_instruction = f"{personality_prompt}\n\nIMPORTANT: {language_instruction}"

                model = genai.GenerativeModel(
                    'gemini-2.5-flash',
                    system_instruction=combined_instruction
                )

                # Generate response
                response = model.generate_content(prompt)
                assistant_response = response.text

                # Display response
                st.markdown(assistant_response)

                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })

                # Generate TTS audio for the new response
                new_msg_idx = len(st.session_state.messages) - 1
                with st.spinner("🔊 Generating audio..."):
                    # Get the current language's TTS voice
                    tts_voice = LANGUAGES[st.session_state.language]["tts_voice"]
                    audio_data = generate_tts_audio(assistant_response, tts_voice)
                    if audio_data:
                        st.session_state.tts_audio[new_msg_idx] = audio_data

            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

    # Reset processing flag and rerun to show audio player
    st.session_state.processing = False
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "💡 Tip: Use voice input by clicking the microphone button, or type your message directly!<br>"
    "Switch personalities in the sidebar to change the AI's behavior!"
    "</div>",
    unsafe_allow_html=True
)
