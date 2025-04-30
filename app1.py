import streamlit as st
from streamlit_option_menu import option_menu
from voice_changer import main as voice_changer_main
from speech import speech_classifier_app
from voice_isolator import main as voice_isolator_main
from sound_effects import main as sound_effects_main
from speech_to_text import main as speech_to_text
from text_to_speech import main as tts_main
import mysql.connector
from gtts import gTTS
from langdetect import detect
import google.generativeai as genai
import os
import tempfile
import time



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

def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    data = cursor.fetchone()
    conn.close()
    return data

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
     st.subheader(" GO to Home My Use Features")
     st.subheader(" In the ancient land of Eldoria, where the skies were painted with shades of mystic hues and the forests whispered secrets of old, there existed a dragon named Zephyros. Unlike the fearsome tales of dragons that plagued human hearts with terror, Zephyros was a creature of wonder and wisdom, revered by all who knew of his existence.")
     st.text("you can work with  AI chatbot and Text to speech and speech to text and voice cloning ,voice changer,AI Speech Classifier ")            
 
     
   

     
     st.markdown(
            """
            <h1 style='font-size: 3.2em; color: #4A90E2;'> Create the Most <span style='color:#FF4B4B;'>Realistic Speech</span></h1>
            <h3 style='color: #555;'>with our AI Audio Platform</h3>
            <p style='font-size: 1.2em; color: #666;'>
                Pioneering research in <strong>Text to Speech</strong>, <strong>AI Voice Generation</strong>, and beyond.
            </p>
            """,
            unsafe_allow_html=True
        )

        


        
     st.markdown("""
      <hr>
      <center style="color: red;">Made by Shoaib • © 2025 VoiceAI</center>
      """, unsafe_allow_html=True)   


def show_home():
    

    # Sidebar for navigation between different pages
    st.sidebar.title(" AI Voice Toolkit")
    selected_page = st.sidebar.radio(
         "Navigate",
        
        [ "AI Chatbot","Text to Speech", "Speech to Text", "Voice Changer", "Sound Effects", "Voice Isolator", "AI Speech Classifier"]
    )

    # Show content based on the selected page in the sidebar
    if selected_page == "AI Chatbot":
        
        
    elif selected_page == "Text to Speech":
        tts_main()
       
    elif selected_page == "Speech to Text":
         speech_to_text()
      
        
    elif selected_page == "Voice Changer":
        voice_changer_main()
         
    elif selected_page == "Sound Effects":
        sound_effects_main()
        
    elif selected_page == "Voice Isolator":
        voice_isolator_main()
    elif selected_page == "AI Speech Classifier":
        speech_classifier_app() 
        

    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.rerun()                      



def show_login():
    st.title(" Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
      user = login_user(username, password)
      if user:
            st.success("Login Successful!")
            st.session_state.logged_in = True
            st.session_state.page = "Home"
            st.rerun()  # Redirect to Home page
      else:
            st.error("Invalid username or password!")

# ----------------- SIGN UP PAGE -----------------
def show_signup():
    st.title(" Sign Up")

    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if "signup_success" not in st.session_state:
        st.session_state.signup_success = False

    if st.button("Sign Up"):
        if not username:
            st.error("Please enter a username.")
        elif not password:
            st.error("Please enter a password.")
        else:
            try:
                #create_user(username, password)
                st.session_state.signup_success = True
            except Exception as e:
                st.error(f"Error creating account: {e}")

    # Show success message after signup
    if st.session_state.signup_success:
        st.success("Account created successfully! Please log in.")
        #if st.button("Go to Login"):
            #st.session_state.page = "Login"
            #st.session_state.signup_success = False
            #st.experimental_rerun()

# ----------------- DOCUMENTATION PAGE -----------------
def show_documentation():
    st.title(" Documentation")
    st.write("""
    

    - **Text to Speech**: Convert your text into human-like voice.
    - **Speech to Text**: Convert spoken audio into written text.
    - **Voice Changer**: Modify your voice pitch and tone.
    - **Sound Effects**: Add background sound effects to your recordings.
    - **Voice Isolator**: Remove noise and isolate voice clearly.
    - **AI Speech Classifier**: Analyze and classify types of speech.

    > Login is required only to access Home features. You can sign up easily!
    """)


if selected == "llEleven":
    show_llEleven()
elif selected == "Home":
    #if st.session_state.logged_in:
        show_home()
    #else:
        #st.warning("Please login first!")
        #show_login()

elif selected == "Login":
    st.session_state.page = "Login"
    show_login()

elif selected == "Sign up":
    st.session_state.page = "Sign up"
    show_signup()

elif selected == "Docu":
    st.session_state.page = "Documentation"
    show_documentation()



