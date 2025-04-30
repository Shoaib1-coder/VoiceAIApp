# voice_changer.py (updated for integration)

import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from io import BytesIO
import matplotlib.pyplot as plt
from scipy import signal

def voice_changer_app():
    """Main function for the voice changer app"""
    # Custom CSS (only needed if not already in main app)
    st.markdown("""
    <style>
        .stAudio {
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎤 Voice Changer App")
    st.markdown("Upload an audio file and apply various voice effects in real-time!")

    # Supported effects
    EFFECTS = {
        "Normal": lambda x, sr: (x, sr),
        "Pitch Up": lambda x, sr: (librosa.effects.pitch_shift(x, sr=sr, n_steps=4), sr),
        "Pitch Down": lambda x, sr: (librosa.effects.pitch_shift(x, sr=sr, n_steps=-4), sr),
        "Robot Voice": lambda x, sr: (signal.lfilter([0.5, 0.5], [1], x), sr),
        "Echo": lambda x, sr: (x + 0.3 * np.roll(x, sr//3), sr),
        "Whisper": lambda x, sr: (x * np.random.uniform(0.2, 0.5, len(x)), sr),
        "Slow Motion": lambda x, sr: (librosa.effects.time_stretch(x, rate=0.7), sr),
        "Fast Forward": lambda x, sr: (librosa.effects.time_stretch(x, rate=1.5), sr),
        "Radio Effect": lambda x, sr: (signal.lfilter([1, -0.97], [1], x), sr),
        "Underwater": lambda x, sr: (signal.lfilter([1], [1, -0.97], x), sr)
    }

    # File upload section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload an audio file (WAV, MP3)",
            type=["wav", "mp3"]
        )
    
    with col2:
        effect_name = st.selectbox(
            "Select Voice Effect",
            list(EFFECTS.keys())
        )
    
    if uploaded_file is not None:
        # ... rest of your existing voice changer code ...
        # (Keep all the processing functions the same)
        pass

def main():
    """Standalone execution"""
    voice_changer_app()

if __name__ == "__main__":
    main()