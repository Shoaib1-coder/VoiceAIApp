
import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from io import BytesIO
import matplotlib.pyplot as plt
from scipy import signal

def voice_changer_app():
    
    st.markdown("""
    <style>
        .stAudio {
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stButton>button {
            width: 100%;
            margin-top: 15px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title(" Voice Changer")
    st.markdown("Upload audio and modify voice characteristics in real-time")

    # Supported effects with gender modification
    EFFECTS = {
        "Normal": lambda x, sr, gender: (x, sr),
        "Pitch Up": lambda x, sr, gender: (librosa.effects.pitch_shift(x, sr=sr, n_steps=4 if gender == "female" else 2), sr),
        "Pitch Down": lambda x, sr, gender: (librosa.effects.pitch_shift(x, sr=sr, n_steps=-4 if gender == "male" else -2), sr),
        "Robot Voice": lambda x, sr, gender: (signal.lfilter([0.5, 0.5], [1], x), sr),
        "Echo": lambda x, sr, gender: (x + 0.3 * np.roll(x, sr//3), sr),
        "Whisper": lambda x, sr, gender: (x * np.random.uniform(0.2, 0.5, len(x)), sr),
        "Slow Motion": lambda x, sr, gender: (librosa.effects.time_stretch(x, rate=0.7), sr),
        "Fast Forward": lambda x, sr, gender: (librosa.effects.time_stretch(x, rate=1.5), sr),
        "Radio Effect": lambda x, sr, gender: (signal.lfilter([1, -0.97], [1], x), sr),
        "Underwater": lambda x, sr, gender: (signal.lfilter([1], [1, -0.97], x), sr)
    }

    
    uploaded_file = st.file_uploader(
        "Upload Audio (MP3/WAV)",
        type=["mp3", "wav"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        effect_name = st.selectbox(
            "Voice Effect",
            list(EFFECTS.keys())
        )
        
    with col2:
        gender = st.radio(
            "Target Gender",
            ["male", "female"],
            horizontal=True
        )
    
    if uploaded_file and st.button("Apply Voice Change", type="primary"):
        with st.spinner("Processing audio..."):
            try:
              
                y, sr = librosa.load(uploaded_file, sr=None)
                
               
                y_processed, sr = EFFECTS[effect_name](y, sr, gender)
                
               
                y_processed = librosa.util.normalize(y_processed)
                
                
                buffer = BytesIO()
                sf.write(buffer, y_processed, sr, format='WAV')
                buffer.seek(0)
                
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original Voice")
                    st.audio(uploaded_file)
                    
                with col2:
                    st.subheader("Modified Voice")
                    st.audio(buffer)
                    
                  
                    st.download_button(
                        "Download Modified Audio",
                        data=buffer,
                        file_name=f"{gender}_{effect_name.lower().replace(' ', '_')}.wav",
                        mime="audio/wav"
                    )
                    
                n
                st.subheader("Waveform Comparison")
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
                
                librosa.display.waveshow(y, sr=sr, ax=ax1, color='blue')
                ax1.set_title("Original Voice")
                
                librosa.display.waveshow(y_processed, sr=sr, ax=ax2, color='red')
                ax2.set_title("Modified Voice")
                
                plt.tight_layout()
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error processing audio: {str(e)}")

def main():
    voice_changer_app()

if __name__ == "__main__":
    main()
