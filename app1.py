import streamlit as st
from streamlit_option_menu import option_menu
from voice_changer import main as voice_changer_main
from voice_isolator import main as voice_isolator_main
from sound_effects import main as sound_effects_main
from speech_to_text import main as speech_to_text
from text_to_speech import main as tts_main
from gtts import gTTS
from langdetect import detect
import os
import tempfile
import time

# ----------------- NAVIGATION -----------------
selected = option_menu(
    menu_title=None,
    options=["llEleven", "Home", "Docu"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# ----------------- llEleven PAGE -----------------
def show_llEleven():
    st.title("Welcome to My VoiceAI Lab – Multifeatured AI Voice Toolkit") 
    st.subheader(" GO to Home Page and go to Sidebar My Use Features")
    st.subheader("In the ancient land of Eldoria, where the skies were painted with shades of mystic hues...")

    st.text("You can work with AI chatbot, Text to Speech, Speech to Text, Voice Cloning, Voice Changer, AI Speech Classifier")            

    st.markdown("""
        <h1 style='font-size: 3.2em; color: #4A90E2;'> Create the Most <span style='color:#FF4B4B;'>Realistic Speech</span></h1>
        <h3 style='color: #555;'>with our AI Audio Platform</h3>
        <p style='font-size: 1.2em; color: #666;'>
            Pioneering research in <strong>Text to Speech</strong>, <strong>AI Voice Generation</strong>, and beyond.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("""
      <hr>
      <center style="color: red;">Made by Shoaib • © 2025 VoiceAI</center>
    """, unsafe_allow_html=True)

# ----------------- HOME PAGE -----------------
def show_home():
    st.sidebar.title("AI Voice Toolkit")
    selected_page = st.sidebar.radio(
        "Navigate",
        [ "Text to Speech", "Speech to Text", "Voice Changer", "Sound Effects", "Voice Isolator"]
    )

    
       
    if selected_page == "Text to Speech":
        tts_main()
    elif selected_page == "Speech to Text":
        speech_to_text()
    elif selected_page == "Voice Changer":
        voice_changer_main()
    elif selected_page == "Sound Effects":
        sound_effects_main()
    elif selected_page == "Voice Isolator":
        voice_isolator_main()
 

# ----------------- DOCUMENTATION PAGE -----------------
def show_documentation():
    st.title("Documentation")
    st.write("""
    - **Text to Speech**: Convert your text into human-like voice.
    - **Speech to Text**: Convert spoken audio into written text.
    - **Voice Changer**: Modify your voice pitch and tone.
    - **Sound Effects**: Add background sound effects to your recordings.
    - **Voice Isolator**: Remove noise and isolate voice clearly.
   

    > Just open the app and explore the tools directly!
    """)

# ----------------- PAGE ROUTING -----------------
if selected == "llEleven":
    show_llEleven()
elif selected == "Home":
    show_home()
elif selected == "Docu":
    show_documentation()




