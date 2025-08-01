import streamlit as st
import speech_recognition as sr           # For speech recognition
from pydub import AudioSegment            # To handle various audio formats
import os
from io import BytesIO
import tempfile
import langdetect                         # To auto-detect language from transcribed text

# Page title
st.title("Speech to Text")

# Add custom CSS styling for UI
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

# Supported file formats for upload
SUPPORTED_FORMATS = {
    "mp3": "mp3",
    "wav": "wav",
    "ogg": "ogg",
    "m4a": "mp4",
    "flac": "flac"
}

# Languages supported for transcription (added Hindi and Chinese)
LANGUAGE_CODES = {
    'en': 'English',
    'ar': 'Arabic',
    'ur': 'Urdu',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'hi': 'Hindi',
    'zh-cn': 'Chinese'
}

# Converts uploaded audio file to WAV format in memory
def convert_to_wav(audio_file, file_extension):
    try:
        audio = AudioSegment.from_file(BytesIO(audio_file.read()), format=file_extension)
        wav_buffer = BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        return wav_buffer
    except Exception as e:
        st.error(f"Conversion error: {str(e)}")
        return None

# Detect language from transcribed text using langdetect
def detect_language(text):
    try:
        lang = langdetect.detect(text)
        return LANGUAGE_CODES.get(lang, 'Unknown')
    except:
        return 'Unknown'

# Perform speech recognition on WAV audio
def transcribe_audio(audio_buffer, language='auto'):
    r = sr.Recognizer()
    with sr.AudioFile(audio_buffer) as source:
        audio_data = r.record(source)
        try:
            if language == 'auto':
                # Try auto mode first
                text = r.recognize_google(audio_data, language='en')  # fallback base language
                detected_lang = detect_language(text)

                # Try fallback detection if langdetect fails
                if detected_lang == 'Unknown':
                    for lang in ['en-US', 'ar-SA', 'ur-PK', 'de-DE', 'hi-IN', 'zh-CN']:
                        try:
                            text = r.recognize_google(audio_data, language=lang)
                            detected_lang = detect_language(text)
                            break
                        except:
                            continue
                return text, detected_lang
            else:
                # Manual language selection
                lang_code = next((k for k, v in LANGUAGE_CODES.items() if v == language), 'en-US')
                google_lang_code = {
                    'en': 'en-US', 'ar': 'ar-SA', 'ur': 'ur-PK',
                    'de': 'de-DE', 'fr': 'fr-FR', 'es': 'es-ES',
                    'hi': 'hi-IN', 'zh-cn': 'zh-CN'
                }.get(lang_code, 'en-US')
                text = r.recognize_google(audio_data, language=google_lang_code)
                return text, language
        except sr.UnknownValueError:
            return "Could not understand audio", "Unknown"
        except sr.RequestError:
            return "API unavailable", "Unknown"

# Main Streamlit app UI
def main():
    st.title(" Speech-to-Text Converter")
    st.markdown("Upload audio files in any format to convert speech to text with automatic language detection")
    
    uploaded_file = st.file_uploader(
        "Upload Audio File (MP3, WAV, OGG, M4A, FLAC)",
        type=list(SUPPORTED_FORMATS.keys()),
        accept_multiple_files=False
    )
    
    if uploaded_file:
        col1, col2 = st.columns([4, 6])

        with col1:
            st.subheader("Original Audio")
            st.audio(uploaded_file)

            # Detect file extension
            file_ext = uploaded_file.name.split(".")[-1].lower()

            # Language selection option
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
                    # Convert uploaded file to WAV
                    wav_buffer = convert_to_wav(uploaded_file, file_ext)

                    if wav_buffer:
                        # Transcribe audio
                        text, detected_lang = transcribe_audio(wav_buffer, selected_lang)

                        with col2:
                            st.subheader("Transcribed Text")

                            # RTL (right-to-left) styling for Urdu/Arabic
                            text_class = "rtl-text" if detected_lang in ['Arabic', 'Urdu'] else ""
                            st.markdown(
                                f'<div class="text-output {text_class}">{text}</div>', 
                                unsafe_allow_html=True
                            )

                            st.info(f"Detected Language: {detected_lang}")

                            # Prepare text file for download
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

# Run the app
if __name__ == "__main__":
    main()
