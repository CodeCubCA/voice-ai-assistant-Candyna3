import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""

# Function to transcribe audio
def transcribe_audio(audio_bytes):
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

        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return None  # Return None so we can show a better message
    except sr.RequestError as e:
        return f"Speech service error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"

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
        st.rerun()

    # Display current personality info
    current = PERSONALITIES[st.session_state.personality]
    st.info(f"{current['icon']} **{current['name']}**\n\n{current['description']}")

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
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
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="2x",
    )

with col2:
    if audio_bytes:
        with st.spinner("🎙️ Processing your voice input..."):
            transcribed = transcribe_audio(audio_bytes)

        if transcribed is None:
            st.warning("Could not understand the audio. Please try again and speak clearly.")
        elif transcribed.startswith("Error:") or transcribed.startswith("Speech service error:"):
            st.error(transcribed)
        else:
            st.success(f"**Transcribed:** {transcribed}")
            st.info("💡 Click the button below to send, or copy the text to edit first!")

            # Add a button to send the transcribed text directly
            if st.button("📤 Send Voice Message", type="primary", use_container_width=True):
                st.session_state.voice_message = transcribed
                st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle voice message if available
if "voice_message" in st.session_state and st.session_state.voice_message:
    prompt = st.session_state.voice_message
    st.session_state.voice_message = None
else:
    # Regular chat input
    prompt = st.chat_input("Type your message here or use voice input above...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Create model with personality-based system instruction
                model = genai.GenerativeModel(
                    'gemini-2.5-flash',
                    system_instruction=PERSONALITIES[st.session_state.personality]["prompt"]
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

            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
    "💡 Tip: Use voice input by clicking the microphone button, or type your message directly!<br>"
    "Switch personalities in the sidebar to change the AI's behavior!"
    "</div>",
    unsafe_allow_html=True
)
