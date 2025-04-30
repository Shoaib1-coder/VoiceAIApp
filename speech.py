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
        # Convert audio to WAV format
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            audio = AudioSegment.from_file(audio_file)
            audio.export(tmp.name, format="wav")
            tmp_path = tmp.name
        
        # Initialize Gemini model
        model = configure_gemini(gemini_api_key)
        
        # Use Gemini to analyze speech
        response = model.generate_content(
            f"Analyze the emotion in this audio file and classify it as only one of these: "
            f"'Happy', 'Sad', 'Angry', 'Neutral', 'Excited', 'Fearful'. "
            f"Respond with just the emotion word. Audio file path: {tmp_path}"
        )
        
        # Clean up
        os.unlink(tmp_path)
        return response.text.strip()
    
    except Exception as e:
        st.error(f"Error during classification: {str(e)}")
        return None

# Main app function
def speech_classifier_app():
    st.title("🎙️ AI Speech Emotion Classifier")
    st.markdown("Upload an audio file to detect emotional tone using Google Gemini")
    
    # Get Gemini API key from Streamlit secrets
    if 'GEMINI_API_KEY' in st.secrets:
        gemini_api_key = st.secrets['GEMINI_API_KEY']
    else:
        st.error("Gemini API key not found in secrets")
        st.stop()
    
    uploaded_file = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"])
    
    if uploaded_file:
        st.audio(uploaded_file, format="audio/wav")
        
        if st.button("Analyze Emotion", type="primary"):
            with st.spinner("Analyzing speech emotion..."):
                emotion = classify_speech(uploaded_file, gemini_api_key)
                
                if emotion:
                    st.success("Analysis Complete!")
                    
                    # Display result with emoji
                    emotion_map = {
                        "Happy": "😊 Happy",
                        "Sad": "😢 Sad", 
                        "Angry": "😠 Angry",
                        "Neutral": "😐 Neutral",
                        "Excited": "🤩 Excited",
                        "Fearful": "😨 Fearful"
                    }
                    
                    display_text = emotion_map.get(emotion, f"❓ {emotion}")
                    st.subheader(f"Detected Emotion: {display_text}")

def main():
    speech_classifier_app()

if __name__ == "__main__":
    main()
