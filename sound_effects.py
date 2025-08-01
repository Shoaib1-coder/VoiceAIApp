# Import necessary libraries
import streamlit as st
import numpy as np
import librosa
import librosa.display
import soundfile as sf
from pydub import AudioSegment
from io import BytesIO
import matplotlib.pyplot as plt

# Page subtitle
st.subheader("Sound Effects")

# Custom CSS styling for Streamlit components
st.markdown("""
<style>
    .stAudio {
        border-radius: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSlider > div > div > div > div {
        background: #4CAF50;
    }
    .effect-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Function to load any audio format using pydub and convert to numpy array
def load_audio(uploaded_file):
    audio = AudioSegment.from_file(uploaded_file)
    buf = BytesIO()
    audio.export(buf, format="wav")
    buf.seek(0)
    y, sr = librosa.load(buf, sr=None)
    return y, sr

# Function to apply selected audio effect
def apply_effect(audio_bytes, effect_name, **params):
    """Apply sound effect to audio bytes"""
    audio = AudioSegment.from_file(BytesIO(audio_bytes))
    buf = BytesIO()
    audio.export(buf, format="wav")
    buf.seek(0)
    y, sr = librosa.load(buf, sr=None)

    if effect_name == "Reverb":
        wet = params.get("wet_level", 0.3)
        delay = int(sr * params.get("delay_ms", 100) / 1000)
        y_eff = y + wet * np.roll(y, delay)

    elif effect_name == "Echo":
        repeats = params.get("repeats", 3)
        decay = params.get("decay", 0.5)
        y_eff = y.copy()
        for i in range(1, repeats + 1):
            y_eff += decay**i * np.roll(y, i * int(sr * 0.2))

    elif effect_name == "Pitch Shift":
        steps = params.get("steps", 4)
        y_eff = librosa.effects.pitch_shift(y, sr=sr, n_steps=steps)

    elif effect_name == "Distortion":
        gain = params.get("gain", 20)
        y_eff = np.tanh(y * gain)

    elif effect_name == "Robot Voice":
        y_fft = librosa.stft(y)
        y_mag = np.abs(y_fft)
        y_eff = librosa.istft(y_mag * np.exp(1j * np.angle(y_fft)))

    else:
        y_eff = y

    buffer = BytesIO()
    sf.write(buffer, y_eff, sr, format='WAV')
    buffer.seek(0)
    return buffer

# Function to display waveform
def plot_waveform(y, sr, title):
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, ax=ax)
    ax.set_title(title)
    ax.grid(True)
    st.pyplot(fig)

# Main app function
def main():
    st.title("🎛️ Sound Effects")
    st.markdown("Apply studio-quality effects to your audio files")

    uploaded_file = st.file_uploader(
        "Upload Audio (MP3, WAV, OGG, M4A, FLAC - Max 10MB)",
        type=["mp3", "wav", "ogg", "m4a", "flac"]
    )

    if uploaded_file:
        col1, col2 = st.columns([5, 5])

        with col1:
            st.subheader("Original Audio")
            st.audio(uploaded_file)
            y_orig, sr = load_audio(uploaded_file)
            plot_waveform(y_orig, sr, "Original Waveform")
            uploaded_file.seek(0)

        with col2:
            st.subheader("Effects Panel")

            effect = st.selectbox(
                "Choose Effect",
                ["None", "Reverb", "Echo", "Pitch Shift", "Distortion", "Robot Voice"]
            )

            params = {}
            if effect == "Reverb":
                params["wet_level"] = st.slider("Reverb Amount", 0.1, 0.9, 0.3)
                params["delay_ms"] = st.slider("Reverb Delay (ms)", 50, 500, 100)

            elif effect == "Echo":
                params["repeats"] = st.slider("Echo Repeats", 1, 5, 3)
                params["decay"] = st.slider("Echo Decay", 0.1, 0.9, 0.5)

            elif effect == "Pitch Shift":
                params["steps"] = st.slider("Pitch Steps", -12, 12, 4)

            elif effect == "Distortion":
                params["gain"] = st.slider("Distortion Gain", 5, 50, 20)

            if st.button("Apply Effect", type="primary"):
                with st.spinner("Processing..."):
                    audio_bytes = uploaded_file.read()
                    processed = apply_effect(audio_bytes, effect, **params)

                    st.subheader("Processed Audio")
                    st.audio(processed)

                    y_proc, sr = librosa.load(processed, sr=None)
                    plot_waveform(y_proc, sr, f"{effect} Effect")

                    st.download_button(
                        "Download Processed Audio",
                        data=processed,
                        file_name=f"processed_{effect.lower().replace(' ', '_')}.wav",
                        mime="audio/wav"
                    )

# Launch the app
if __name__ == "__main__":
    main()



   
