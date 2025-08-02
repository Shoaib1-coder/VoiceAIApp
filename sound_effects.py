import streamlit as st
from pydub import AudioSegment, effects, silence
import numpy as np
import librosa
import soundfile as sf
from io import BytesIO

st.set_page_config(page_title="Basic Audio Editor", layout="centered")
st.title("🎧 Basic Audio Editing App")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg", "m4a", "flac"])
second_file = st.file_uploader("Upload a second file (for merge/join)", type=["mp3", "wav", "ogg", "m4a", "flac"], key="merge")
bg_music_file = st.file_uploader("Upload Background Music (optional)", type=["mp3", "wav", "ogg", "m4a", "flac"], key="bgm")

if uploaded_file:
    audio = AudioSegment.from_file(uploaded_file)
    st.audio(uploaded_file, format='audio/wav')

    with st.expander("🎚️ Editing Options"):
        start_time = st.number_input("Start time to cut (seconds)", min_value=0.0, max_value=len(audio) / 1000, value=0.0)
        end_time = st.number_input("End time to cut (seconds)", min_value=0.0, max_value=len(audio) / 1000, value=len(audio) / 1000)

        fade_in = st.slider("Fade In (ms)", 0, 5000, 0)
        fade_out = st.slider("Fade Out (ms)", 0, 5000, 0)

        normalize_audio = st.checkbox("Normalize")
        remove_silence = st.checkbox("Silence Removal")
        reverse = st.checkbox("Reverse Audio")

        volume_change = st.slider("Volume Adjustment (dB)", -30, 30, 0)
        stretch_rate = st.slider("Time Stretch (Slow ← 1.0 → Fast)", 0.5, 2.0, 1.0)
        bg_volume = st.slider("Background Music Volume (%)", 0, 100, 30)
        convert_format = st.selectbox("Convert Format", ["WAV", "MP3"])

    if st.button("Apply Effects"):
        # Trim
        edited = audio[int(start_time * 1000):int(end_time * 1000)]

        # Fade
        if fade_in > 0:
            edited = edited.fade_in(fade_in)
        if fade_out > 0:
            edited = edited.fade_out(fade_out)

        # Normalize
        if normalize_audio:
            edited = effects.normalize(edited)

        # Silence Removal
        if remove_silence:
            chunks = silence.split_on_silence(edited, silence_thresh=-40)
            if chunks:
                edited = chunks[0]
                for c in chunks[1:]:
                    edited += c

        # Volume
        if volume_change != 0:
            edited += volume_change

        # Reverse
        if reverse:
            edited = edited.reverse()

        # Add background music
        if bg_music_file:
            bg_music = AudioSegment.from_file(bg_music_file)
            bg_music = bg_music - (100 - bg_volume)  # Lower bg music volume

            # Loop or trim to match length
            if len(bg_music) < len(edited):
                repeat_times = len(edited) // len(bg_music) + 1
                bg_music = bg_music * repeat_times
            bg_music = bg_music[:len(edited)]

            # Overlay
            edited = edited.overlay(bg_music)

        # Convert to NumPy array for time-stretch
        samples = np.array(edited.get_array_of_samples()).astype(np.float32) / (2**15)
        if stretch_rate != 1.0:
            samples = librosa.effects.time_stretch(samples, stretch_rate)

        buffer = BytesIO()
        sf.write(buffer, samples, samplerate=edited.frame_rate, format=convert_format)
        st.success("✅ Audio edited successfully!")
        st.audio(buffer, format=f"audio/{convert_format.lower()}")
        st.download_button("📥 Download Edited Audio", buffer, file_name=f"edited.{convert_format.lower()}")

    # Merge
    if second_file and st.button("Merge Audio Files"):
        audio2 = AudioSegment.from_file(second_file)
        merged = audio + audio2
        buffer = BytesIO()
        merged.export(buffer, format=convert_format.lower())
        st.success("✅ Files merged!")
        st.audio(buffer, format=f"audio/{convert_format.lower()}")
        st.download_button("📥 Download Merged Audio", buffer, file_name=f"merged.{convert_format.lower()}")
