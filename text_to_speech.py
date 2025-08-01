import streamlit as st
from gtts import gTTS              # Google Text-to-Speech
from io import BytesIO             # For handling in-memory audio file

# Supported Languages Dictionary
LANGUAGES = {
    'en': 'English',
    'ar': 'Arabic',
    'ur': 'Urdu',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'hi': 'Hindi',               
    'zh-cn': 'Chinese'           
}

# Function to convert text to speech
def text_to_speech(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)      # Create speech object
        audio_buffer = BytesIO()                   # Create in-memory audio buffer
        tts.write_to_fp(audio_buffer)              # Write audio to buffer
        audio_buffer.seek(0)                       # Reset pointer to start
        return audio_buffer
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

# Streamlit app UI
def main():
    st.title(" Text-to-Speech Converter ")         # App title

    # Text input field
    text = st.text_area("Enter your text here:", height=150)

    # Language dropdown menu
    selected_lang = st.selectbox(
        " Select a language:",
        options=list(LANGUAGES.keys()),            # List of language codes
        format_func=lambda x: LANGUAGES[x]         # Show full language name
    )

    # Convert text to speech when button clicked
    if st.button(" Speech Convert"):
        if text.strip() == "":
            st.warning("Please enter some text before converting.")
        else:
            with st.spinner("Generating speech..."):
                audio = text_to_speech(text, selected_lang)
                if audio:
                    st.success(" Speech successfully generated.")

                    # Play audio in app
                    st.audio(audio, format="audio/mp3")

                    # Download button for saving audio
                    st.download_button(
                        " Download Audio",
                        data=audio,
                        file_name=f"speech_{selected_lang}.mp3",
                        mime="audio/mp3"
                    )

# Run the app
if __name__ == "__main__":
    main()


