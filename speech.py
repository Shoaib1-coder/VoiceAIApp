import streamlit as st
import google.generativeai as genai
import os
from pydub import AudioSegment
import tempfile

# Configure Gemini
def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# Classify speech from audio file
def classify_speech(audio_file, gemini_api_key):
    try:
        # Convert audio to text (using Gemini's speech-to-text)
        model = configure_gemini(gemini_api_key)
        
        # Save audio temporarily (Gemini requires file path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio = AudioSegment.from_file(audio_file)
            audio.export(tmp.name, format="wav")
            tmp_path = tmp.name
        
        # Use Gemini to analyze speech
        response = model.generate_content(
            f"Analyze this audio file and classify the speech into one of these categories: "
            f"'Happy', 'Sad', 'Angry', 'Neutral', 'Excited', 'Fearful'. "
            f"Only respond with the most likely emotion category. Audio file: {tmp_path}"
        )
        
        os.unlink(tmp_path)  # Delete temp file
        return response.text.strip()
    
    except Exception as e:
        st.error(f"Classification error: {str(e)}")
        return None

# Main app function
def speech_classifier_app():
    st.title("🎙️ AI Speech Emotion Classifier")
    st.markdown("Upload an audio file to detect the emotional tone using Google Gemini")
    
    # Get Gemini API key (from secrets or input)
    if 'gemini_api_key' in st.secrets:
        gemini_api_key = st.secrets['gemini_api_key']
    else:
        gemini_api_key = st.text_input("Enter Google Gemini API Key", type="password")
    
    uploaded_file = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"])
    
    if uploaded_file and gemini_api_key:
        if st.button("Analyze Speech"):
            with st.spinner("Classifying emotion..."):
                emotion = classify_speech(uploaded_file, gemini_api_key)
                
                if emotion:
                    st.success(f"Detected Emotion: **{emotion}**")
                    
                    # Display emotion with icon
                    emotion_icons = {
                        "Happy": "😊",
                        "Sad": "😢",
                        "Angry": "😠",
                        "Neutral": "😐",
                        "Excited": "🤩",
                        "Fearful": "😨"
                    }
                    icon = emotion_icons.get(emotion, "❓")
                    st.subheader(f"{icon} {emotion}")
                    
                    # Play original audio
                    st.audio(uploaded_file, format="audio/wav")

def main():
    speech_classifier_app()

if __name__ == "__main__":
    main()