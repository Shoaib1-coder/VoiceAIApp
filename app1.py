import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
from gtts import gTTS
import google.generativeai as genai
import os
import tempfile
import time
from elevenlabs import generate, save, set_api_key, voices


# ----------------- DATABASE FUNCTIONS -----------------
#def get_connection():
    #conn = mysql.connector.connect(
        #host="host="local",
        #user="root",  # Your MySQL username
        #password="your_mysql_password",  # Your MySQL password
        #database="your_database",  # Your MySQL database name 
        #port=3306
    #)
    #return conn

#def create_user(username, password):
    #conn = get_connection()
    #cursor = conn.cursor()
    #cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    #conn.commit()
    #conn.close()

#def login_user(username, password):
    #conn = get_connection()
    #cursor = conn.cursor()
    #cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    #data = cursor.fetchone()
    #conn.close()
    #return data

# ----------------- SESSION SETUP -----------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = "Login"

# ----------------- NAVIGATION -----------------
selected = option_menu(
    menu_title=None,
    options=["llEleven" ,"Home", "Login", "Sign up", "Docu"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
def show_llEleven():
     st.title("Welcome to My MY llElevenlab App") 
     st.subheader(" In the ancient land of Eldoria, where the skies were painted with shades of mystic hues and the forests whispered secrets of old, there existed a dragon named Zephyros. Unlike the fearsome tales of dragons that plagued human hearts with terror, Zephyros was a creature of wonder and wisdom, revered by all who knew of his existence.")
     st.text("you can work with  AI chatbot and Text to speech and speech to text and voice cloning ,voice changer,AI Speech Classifier ")            
 
     
   

     
     st.markdown(
            """
            <h1 style='font-size: 3.2em; color: #4A90E2;'>🎙️ Create the Most <span style='color:#FF4B4B;'>Realistic Speech</span></h1>
            <h3 style='color: #555;'>with our AI Audio Platform</h3>
            <p style='font-size: 1.2em; color: #666;'>
                Pioneering research in <strong>Text to Speech</strong>, <strong>AI Voice Generation</strong>, and beyond.
            </p>
            """,
            unsafe_allow_html=True
        )

        

# -------------- Footer --------------
        
     st.markdown("""
      <hr>
      <center style="color: #aaa;">Made with ❤️ using Streamlit • © 2025 VoiceAI</center>
      """, unsafe_allow_html=True)   

# ----------------- HOME PAGE -----------------
def show_home():
    st.title("🏠 Home Page")

    # Sidebar for navigation between different pages
    st.sidebar.title("🎧 AI Voice Toolkit")
    selected_page = st.sidebar.radio(
        "Navigate",
        ["Text to Speech", "Speech to Text", "Voice Changer", "Sound Effects", "Voice Isolator", "AI Speech Classifier"]
    )

    # Show content based on the selected page in the sidebar
    if selected_page == "Text to Speech":
        # Set your API key (you can also use environment variables for safety)
        ELEVEN_API_KEY = st.secrets.get("ELEVEN_API_KEY") or "your-elevenlabs-api-key"
        set_api_key(ELEVEN_API_KEY)

# Streamlit UI
        st.set_page_config(page_title="🎙️ ElevenLabs TTS", layout="centered")
        st.title("🎤 AI Voice Generator (ElevenLabs)")
        st.markdown("Generate realistic speech using [ElevenLabs](https://www.elevenlabs.io)")

        text = st.text_area("Enter text to convert to speech:", height=150)

          # List of available voices
        available_voices = voices()
        voice_options = [voice.name for voice in available_voices]
        selected_voice = st.selectbox("Choose a voice:", voice_options)
        if st.button("Generate Speech"):
          if not text.strip():
           st.warning("Please enter some text.")
        elif not selected_voice:
           st.warning("Please select a voice.")
        else:
           voice_id = next((v.voice_id for v in available_voices if v.name == selected_voice), None)
           if voice_id:
               audio = generate(text=text, voice=voice_id, model="eleven_monolingual_v1")
               filename = "output.mp3"
               save(audio, filename)
               st.audio(filename, format="audio/mp3")

               with open(filename, "rb") as f:
                st.download_button("Download Audio", f, file_name="speech.mp3", mime="audio/mpeg")

               os.remove(filename)
           else:
              st.error("Selected voice is not available.")



