import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os
from io import BytesIO
import tempfile
import langdetect

# Page Config
st.set_page_config(
    page_title="Universal Speech-to-Text Converter",
    page_icon="🗣️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stAudio {
        border-radius: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stDownloadButton>button {
        width: 100%;
        justify-content: center;
    }
    .text-output {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    .rtl-text {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

SUPPORTED_FORMATS = {
    "mp3": "mp3",
    "wav": "wav",
    "ogg": "ogg",
    "m4a": "mp4",
    "flac": "flac"
}

LANGUAGE_CODES = {
    'en': 'English',
    'ar': 'Arabic',
    'ur': 'Urdu',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish'
}

def convert_to_wav(audio_file, file_extension):
    """Convert any audio format to WAV in memory"""
    try:
        audio = AudioSegment.from_file(BytesIO(audio_file.read()), format=file_extension)
        wav_buffer = BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        return wav_buffer
    except Exception as e:
        st.error(f"Conversion error: {str(e)}")
        return None

def detect_language(text):
    """Detect language from text"""
    try:
        lang = langdetect.detect(text)
        return LANGUAGE_CODES.get(lang, 'Unknown')
    except:
        return 'Unknown'

def transcribe_audio(audio_buffer, language='auto'):
    """Convert speech to text with automatic language detection"""
    r = sr.Recognizer()
    with sr.AudioFile(audio_buffer) as source:
        audio_data = r.record(source)
        try:
            if language == 'auto':
                # First try with auto-detection
                text = r.recognize_google(audio_data, language='auto')
                detected_lang = detect_language(text)
                
                # If auto-detection fails, try specific languages
                if detected_lang == 'Unknown':
                    for lang in ['en-US', 'ar-SA', 'ur-PK', 'de-DE']:
                        try:
                            text = r.recognize_google(audio_data, language=lang)
                            detected_lang = detect_language(text)
                            break
                        except:
                            continue
                return text, detected_lang
            else:
                # Use specified language
                lang_code = next((k for k, v in LANGUAGE_CODES.items() if v == language), 'en-US')
                text = r.recognize_google(audio_data, language=lang_code)
                return text, language
        except sr.UnknownValueError:
            return "Could not understand audio", "Unknown"
        except sr.RequestError:
            return "API unavailable", "Unknown"

def main():
    st.title("🗣️ Universal Speech-to-Text Converter")
    st.markdown("Upload audio files in any format to convert speech to text with automatic language detection")
    
    uploaded_file = st.file_uploader(
        "Upload Audio File (MP3, WAV, OGG, M4A, FLAC)",
        type=list(SUPPORTED_FORMATS.keys()),
        accept_multiple_files=False
    )
    
    if uploaded_file:
        col1, col2 = st.columns([4,6])
        
        with col1:
            st.subheader("Original Audio")
            st.audio(uploaded_file)
            file_ext = uploaded_file.name.split(".")[-1].lower()
            
            language_option = st.radio(
                "Language Option",
                ["Auto Detect", "Specify Language"],
                horizontal=True
            )
            
            selected_lang = "auto"
            if language_option == "Specify Language":
                selected_lang = st.selectbox(
                    "Select Language",
                    list(LANGUAGE_CODES.values())
                )
            
            if st.button("Convert to Text", type="primary"):
                with st.spinner("Processing..."):
                    # Convert to WAV format
                    wav_buffer = convert_to_wav(uploaded_file, file_ext)
                    
                    if wav_buffer:
                        # Transcribe
                        text, detected_lang = transcribe_audio(wav_buffer, selected_lang)
                        
                        with col2:
                            st.subheader("Transcribed Text")
                            
                            # Apply RTL styling for Arabic/Urdu
                            text_class = "rtl-text" if detected_lang in ['Arabic', 'Urdu'] else ""
                            st.markdown(
                                f'<div class="text-output {text_class}">{text}</div>', 
                                unsafe_allow_html=True
                            )
                            
                            st.info(f"Detected Language: {detected_lang}")
                            
                            # Download as text file
                            txt_buffer = BytesIO()
                            txt_buffer.write(text.encode('utf-8'))
                            txt_buffer.seek(0)
                            
                            st.download_button(
                                "Download as TXT",
                                data=txt_buffer,
                                file_name=f"transcription_{detected_lang}.txt",
                                mime="text/plain",
                                type="primary"
                            )

if __name__ == "__main__":
    main()
