import streamlit as st
from gtts import gTTS
from io import BytesIO



# Supported Languages
LANGUAGES = {
    'en': 'English',
    'ar': 'Arabic',
    'ur': 'Urdu',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish'
}

def text_to_speech(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def main():
    st.title(" Text-to-Speech Converter ")

    # Text input
    text = st.text_area("Enter your text here:", height=150)

    # Language selection
    selected_lang = st.selectbox(
        " Select a language:",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x]
    )

    # Button to convert
    if st.button(" Speech Convert"):
        if text.strip() == "":
            st.warning("Please enter some text before converting.")
        else:
            with st.spinner("Generating speech..."):
                audio = text_to_speech(text, selected_lang)
                if audio:
                    st.success(" Speech successfully generated.")
                    st.audio(audio, format="audio/mp3")
                    st.download_button(
                        " Download Audio",
                        data=audio,
                        file_name=f"speech_{selected_lang}.mp3",
                        mime="audio/mp3"
                    )

if __name__ == "__main__":
    main()

