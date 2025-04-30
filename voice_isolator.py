import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from io import BytesIO
import noisereduce as nr

# Page Config
st.set_page_config(
    page_title="Voice Isolator",
    page_icon="🔊",
    layout="wide"
)

# Custom CSS for Streamlit Cloud
st.markdown("""
<style>
    .stAudio {
        border-radius: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def isolate_voice(audio_bytes, progress_bar):
    """Isolate vocals using in-memory processing"""
    try:
        progress_bar.progress(10)
        
        # Load audio directly from bytes
        y, sr = librosa.load(BytesIO(audio_bytes), sr=None)
        
        # Step 1: Harmonic-Percussive Separation
        progress_bar.progress(30)
        y_harmonic, _ = librosa.effects.hpss(y)
        
        # Step 2: Noise reduction
        progress_bar.progress(60)
        y_clean = nr.reduce_noise(
            y=y_harmonic,
            sr=sr,
            stationary=True,
            prop_decrease=0.85  # More aggressive reduction for voice isolation
        )
        
        # Step 3: Spectral gate to remove residual noise
        progress_bar.progress(80)
        S = librosa.stft(y_clean)
        S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        mask = S_db > -32  # Slightly more permissive threshold
        y_isolated = librosa.istft(S * mask)
        
        # Convert to bytes
        buffer = BytesIO()
        sf.write(buffer, y_isolated, sr, format='WAV')
        buffer.seek(0)
        
        progress_bar.progress(100)
        return buffer
    
    except Exception as e:
        st.error(f"Processing error: {str(e)}")
        return None

def main():
    st.title("🔊 Cloud Voice Isolator")
    st.markdown("""
    Upload audio to extract clean vocals (works on Streamlit Cloud)
    """)
    
    uploaded_file = st.file_uploader(
        "Upload MP3/WAV (max 10MB)", 
        type=["mp3", "wav"],
        accept_multiple_files=False
    )
    
    if uploaded_file:
        col1, col2 = st.columns([5,5])
        
        with col1:
            st.subheader("Original Audio")
            st.audio(uploaded_file)
            
        with col2:
            if st.button("✨ Isolate Vocals", type="primary"):
                with st.spinner("Processing..."):
                    progress_bar = st.progress(0)
                    audio_bytes = uploaded_file.read()
                    isolated = isolate_voice(audio_bytes, progress_bar)
                    
                    if isolated:
                        st.subheader("Isolated Vocals")
                        st.audio(isolated)
                        
                        st.download_button(
                            "⬇️ Download Clean Vocals",
                            data=isolated,
                            file_name="isolated_vocals.wav",
                            mime="audio/wav",
                            type="primary"
                        )

if __name__ == "__main__":
    main()