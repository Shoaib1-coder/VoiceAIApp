import streamlit as st
import pyttsx3  # Offline TTS
import gtts  # Online TTS (Google)
from io import BytesIO
import langdetect
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

st.title("Text-to-Speech Converter")

# Supported Languages
LANGUAGES = {
    'en': {'name': 'English', 'engine': 'both'},
    'ar': {'name': 'Arabic', 'engine': 'google'},
    'ur': {'name': 'Urdu', 'engine': 'google'}, 
    'de': {'name': 'German', 'engine': 'both'},
    'fr': {'name': 'French', 'engine': 'both'},
    'es': {'name': 'Spanish', 'engine': 'both'}
}

def detect_language(text):
    """Detect language from text"""
    try:
        lang = langdetect.detect(text)
        return lang if lang in LANGUAGES else 'en'
    except:
        return 'en'

def text_to_speech(text, language, engine='auto'):
    """Convert text to speech audio"""
    lang_code = language if len(language) == 2 else 'en'
    
    try:
        if engine == 'google' or (engine == 'auto' and LANGUAGES[lang_code]['engine'] != 'pyttsx3'):
            # Use Google TTS
            tts = gtts.gTTS(text, lang=lang_code)
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer, 'google'
        else:
            # Use pyttsx3 (offline)
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Try to set voice for the language
            for voice in voices:
                if language in voice.languages[0].lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                tmp_path = tmp.name
            
            engine.save_to_file(text, tmp_path)
            engine.runAndWait()
            
            # Convert to BytesIO
            audio = AudioSegment.from_wav(tmp_path)
            audio_buffer = BytesIO()
            audio.export(audio_buffer, format='wav')
            audio_buffer.seek(0)
            
            os.unlink(tmp_path)
            return audio_buffer, 'pyttsx3'
            
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None, None

def main():
    st.title("🔊 Text-to-Speech Converter")
    st.markdown("Convert text to speech with automatic language detection")
    
    # Text input
    text = st.text_area("Enter text to convert to speech:", height=150)
    
    if text:
        # Language detection
        detected_lang = detect_language(text)
        lang_name = LANGUAGES.get(detected_lang, {}).get('name', 'English')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"Detected Language: **{lang_name}**")
            
            # Language override
            selected_lang = st.selectbox(
                "Or select language:",
                options=list(LANGUAGES.keys()),
                format_func=lambda x: LANGUAGES[x]['name'],
                index=list(LANGUAGES.keys()).index(detected_lang)
            )
        
        with col2:
            engine = st.radio(
                "TTS Engine:",
                ["Auto", "Google", "Offline"],
                horizontal=True
            )
            
            if st.button("Generate Speech", type="primary"):
                with st.spinner("Generating audio..."):
                    audio_buffer, used_engine = text_to_speech(
                        text,
                        selected_lang,
                        engine.lower() if engine != "Auto" else "auto"
                    )
                    
                    if audio_buffer:
                        st.success(f"Generated using {used_engine} engine")
                        st.audio(audio_buffer)
                        
                        # Download option
                        st.download_button(
                            "Download Audio",
                            data=audio_buffer,
                            file_name=f"tts_{selected_lang}.wav",
                            mime="audio/wav"
                        )

if __name__ == "__main__":
    main()
