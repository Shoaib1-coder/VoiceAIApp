import streamlit as st
import google.generativeai as genai
import os
from pydub import AudioSegment
from io import BytesIO
import tempfile

# Configure Gemini
def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-2.0-flash")

def convert_audio(audio_file):
    """Convert audio to WAV format in memory"""
    try:
        # Read audio file
        audio = AudioSegment.from_file(BytesIO(audio_file.read()))
        
        # Export to WAV in memory
        wav_buffer = BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        return wav_buffer
        
    except Exception as e:
        st.error(f"Audio conversion error: {str(e)}")
        return None

def classify_speech(audio_file, gemini_api_key):
    try:
        # Convert audio to WAV format
        wav_buffer = convert_audio(audio_file)
        if not wav_buffer:
            return None
            
        # Save temporary WAV file (Gemini needs file path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(wav_buffer.read())
            tmp_path = tmp.name
        
        # Initialize Gemini model
        model = configure_gemini(gemini_api_key)
        
        # Use Gemini to analyze speech
        response = model.generate_content(
            "Analyze the emotion in this audio and respond with ONLY one word: "
            "'Happy', 'Sad', 'Angry', 'Neutral', 'Excited', or 'Fearful'. "
            f"Audio file: {tmp_path}"
        )
        
        # Clean up
        os.unlink(tmp_path)
        return response.text.strip()
    
    except Exception as e:
        st.error(f"Classification error: {str(e)}")
        return None

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

if __name__ == "__main__":
    speech_classifier_app()
