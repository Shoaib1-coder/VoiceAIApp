import streamlit as st
from streamlit_option_menu import option_menu
from voice_changer import main as voice_changer_main
from voice_isolator import main as voice_isolator_main
from speech_to_text import main as speech_to_text
from text_to_speech import main as tts_main

# ----------------- NAVIGATION -----------------
selected = option_menu(
    menu_title=None,
    options=["Home", "Tools", "Documentation"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# ----------------- HOME PAGE -----------------
def show_home():
    st.title("Welcome to My VoiceAI Lab") 
    st.subheader("Go to the Home Page and use the sidebar to explore features.")
    st.subheader("In the ancient land of Eldoria, where the skies were painted with shades of mystic hues...")

    st.text("You can work with Text to Speech, Speech to Text, Voice Cloning, and Voice Changer.")

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

# ----------------- TOOLS PAGE -----------------
def show_tools():
    st.sidebar.title("AI Voice Toolkit")
    selected_page = st.sidebar.radio(
        "Navigate",
        ["Text to Speech", "Speech to Text", "Voice Changer", "Voice Isolator"]
    )

    if selected_page == "Text to Speech":
        tts_main()
    elif selected_page == "Speech to Text":
        speech_to_text()
    elif selected_page == "Voice Changer":
        voice_changer_main()
    elif selected_page == "Voice Isolator":
        voice_isolator_main()

# ----------------- DOCUMENTATION PAGE -----------------
def show_documentation():
    st.title("Documentation")
    st.write("""
    - **Text to Speech**: Convert your text into human-like voice.
    - **Speech to Text**: Convert spoken audio into written text.
    - **Voice Changer**: Modify your voice pitch and tone.
    - **Voice Isolator**: Remove background noise and isolate vocals.

    > Just open the app and explore the tools directly!
    """)

# ----------------- PAGE ROUTING -----------------
if selected == "Home":
    show_home()
elif selected == "Tools":
    show_tools()
elif selected == "Documentation":
    show_documentation()





