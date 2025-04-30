import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os
from io import BytesIO
import tempfile

# Page Config
st.title("🎤 Universal Speech-to-Text Converter")

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
</style>
""", unsafe_allow_html=True)

SUPPORTED_FORMATS = {
    "mp3": "mp3",
    "wav": "wav",
    "ogg": "ogg",
    "m4a": "mp4",
    "flac": "flac"
}

def convert_to_wav(audio_file, file_extension):
    """Convert any audio format to WAV"""
    with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as tmp:
        tmp.write(audio_file.read())
        input_path = tmp.name
    
    output_path = input_path.replace(f".{file_extension}", ".wav")
    
    try:
        audio = AudioSegment.from_file(input_path, format=file_extension)
        audio.export(output_path, format="wav")
        return output_path
    finally:
        if os.path.exists(input_path):
            os.unlink(input_path)

def transcribe_audio(audio_path):
    """Convert speech to text using Google's recognizer"""
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "API unavailable"

def main():
    st.title("🗣️ Universal Speech-to-Text Converter")
    st.markdown("Upload audio files in any format to convert speech to text")
    
    uploaded_file = st.file_uploader(
        "Upload Audio File",
        type=list(SUPPORTED_FORMATS.keys()),
        accept_multiple_files=False
    )
    
    if uploaded_file:
        col1, col2 = st.columns([4,6])
        
        with col1:
            st.subheader("Original Audio")
            st.audio(uploaded_file)
            file_ext = uploaded_file.name.split(".")[-1].lower()
            
            if st.button("Convert to Text", type="primary"):
                with st.spinner("Processing..."):
                    # Convert to WAV if needed
                    if file_ext != "wav":
                        wav_path = convert_to_wav(uploaded_file, file_ext)
                    else:
                        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                            tmp.write(uploaded_file.read())
                            wav_path = tmp.name
                    
                    # Transcribe
                    try:
                        text = transcribe_audio(wav_path)
                        
                        with col2:
                            st.subheader("Transcribed Text")
                            st.markdown(f'<div class="text-output">{text}</div>', unsafe_allow_html=True)
                            
                            # Download as text file
                            txt_buffer = BytesIO()
                            txt_buffer.write(text.encode('utf-8'))
                            txt_buffer.seek(0)
                            
                            st.download_button(
                                "Download as TXT",
                                data=txt_buffer,
                                file_name="transcription.txt",
                                mime="text/plain",
                                type="primary"
                            )
                    finally:
                        if os.path.exists(wav_path):
                            os.unlink(wav_path)

if __name__ == "__main__":
    main()