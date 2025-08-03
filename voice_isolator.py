# voice_isolator.py

import streamlit as st
import numpy as np
import librosa
import noisereduce as nr
import soundfile as sf
from io import BytesIO
from pydub import AudioSegment

def main():
    st.set_page_config(page_title="Voice Isolator", layout="centered")
    st.markdown("##  Voice Isolator")
    st.markdown("Upload audio to extract clean vocals")
    st.markdown("#### Upload MP3, WAV, OGG, M4A, FLAC (max 10MB)")

    # Upload
    uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "ogg", "m4a", "flac"])

    # Convert and load audio
    def convert_and_load_audio(uploaded_file):
        try:
            audio = AudioSegment.from_file(uploaded_file)
            wav_io = BytesIO()
            audio.export(wav_io, format='wav')
            wav_io.seek(0)
            y, sr = librosa.load(wav_io, sr=None)
            return y, sr, None
        except Exception as e:
            return None, None, f"Error: {str(e)}"

    if uploaded_file:
        st.audio(uploaded_file, format="audio/mpeg")
        y, sr, error = convert_and_load_audio(uploaded_file)

        if error:
            st.error(error)
        else:
            st.info(" Audio loaded. Processing to isolate voice...")

            reduced_noise = nr.reduce_noise(y=y, sr=sr)

            output_buffer = BytesIO()
            sf.write(output_buffer, reduced_noise, sr, format='WAV')
            output_buffer.seek(0)

            st.success("Voice isolation complete. Download below.")
            st.audio(output_buffer, format="audio/wav")
            st.download_button(
                label=" Download Isolated Voice",
                data=output_buffer,
                file_name="clean_voice.wav",
                mime="audio/wav"
            )
