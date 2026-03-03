from PIL import Image
import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS
import tempfile

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


st.set_page_config(page_title="Bhagavad Gita Assistant", page_icon="🕉️")

st.image(Image.open("images/krishna_arjuna.jpeg"), use_container_width=True)


st.caption("")


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def transcribe_audio(audio_bytes):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        # Save audio bytes to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        with open(temp_audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(temp_audio_path, file.read()),
                model="whisper-large-v3",
                response_format="json",
                language="en", 
                temperature=0.0
            )
        
        os.remove(temp_audio_path) # Clean up
        return transcription.text
    except Exception as e:
        st.error(f"Transcription error: {e}")
        return None

def text_to_speech(text):
    try:
        # Detect language
        lang = 'en'
        if any(0x0900 <= ord(char) <= 0x097F for char in text): # Devanagari (Hindi/Sanskrit)
            lang = 'hi'
        elif any(0x0C80 <= ord(char) <= 0x0CFF for char in text): # Kannada
            lang = 'kn'
        
        tts = gTTS(text=text, lang=lang)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"TTS error: {e}")
        return None

# Custom CSS for Vibrant Theme
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF5E6 100%);
    }

    /* Title - Gradient Text */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .gradient-text {
        background: -webkit-linear-gradient(45deg, #FF9933, #FF5E62);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Subtitle/Caption styling */
    .stCaption {
        font-size: 1.1rem !important;
        color: #555 !important;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Voice Button - Green Gradient */
    [data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 50px !important;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    [data-testid="stPopover"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(56, 239, 125, 0.6) !important;
    }

    /* Input Box Focus - Orange Accent */
    .stTextInput > div > div > input:focus {
        border-color: #FF9933 !important;
        box-shadow: 0 0 0 2px rgba(255, 153, 51, 0.3) !important;
    }
    
    /* Image Styling */
    img {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# Custom Title with isolated emoji to prevent gradient override
st.markdown("<h1 style='text-align: center;'>🕉️ <span class='gradient-text'>Bhagavad Gita Chatbot</span></h1>", unsafe_allow_html=True)

# Use a popover for a cleaner UI
with st.popover("🎙️ Voice Chat"):
    audio_value = st.audio_input("Speak your question")

prompt = st.chat_input("Ask something about the Bhagavad Gita...")

final_prompt = None

if audio_value:
    with st.spinner("Transcribing..."):
        transcribed_text = transcribe_audio(audio_value.read())
        if transcribed_text:
            final_prompt = transcribed_text

if prompt:
    final_prompt = prompt

if final_prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    # Call FastAPI Backend
    try:
        api_base = os.getenv("API_BASE", "https://gitamind.onrender.com")
        response = requests.post(
            f"{api_base}/chat",
            json={"messages": st.session_state.messages}
        )
        if response.status_code == 200:
            data = response.json()
        else:
            st.error(f"Backend error: {response.text}")
            data = {}

        # -----------------------
        # Extract reply safely
        # -----------------------
        reply = (
            data.get("answer")
            or data.get("verse")
            or "No response generated."
        )

        confidence = data.get("confidence", 0)
        formatted = f"{reply}\n\n🧠 Confidence: {confidence}%"

        # Generate Audio Response
        audio_file_path = text_to_speech(reply)

        # Store + render assistant
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted
        })

        with st.chat_message("assistant"):
            st.markdown(reply)
            st.caption(f"🧠 Confidence: {confidence}%")
            if audio_file_path:
                st.audio(audio_file_path, format="audio/mp3", autoplay=True)
                
    except Exception as e:
        st.error(f"Agent error: {e}")
