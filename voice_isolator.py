import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from io import BytesIO
import noisereduce as nr

#  Custom CSS styling for audio player, progress bar, and buttons
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

# Function to isolate voice from uploaded audio
def isolate_voice(audio_bytes, progress_bar):
    try:
        progress_bar.progress(10)  # Start progress
        
        #  Load audio from bytes (uploaded file)
        y, sr = librosa.load(BytesIO(audio_bytes), sr=None)
        progress_bar.progress(30)
        
        #  Separate harmonic (voice) from percussive (noise) parts
        y_harmonic, _ = librosa.effects.hpss(y)
        progress_bar.progress(60)
        
        #  Reduce background noise from harmonic signal
        y_clean = nr.reduce_noise(
            y=y_harmonic,
            sr=sr,
            stationary=True,
            prop_decrease=0.85  # Aggressive noise reduction
        )
        
        #  Spectral gating: remove residual quiet parts
        progress_bar.progress(80)
        S = librosa.stft(y_clean)
        S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        mask = S_db > -32
        y_isolated = librosa.istft(S * mask)
        
        # Save result to memory buffer (BytesIO)
        buffer = BytesIO()
        sf.write(buffer, y_isolated, sr, format='WAV')
        buffer.seek(0)
        
        progress_bar.progress(100)
        return buffer
    except Exception as e:
        st.error(f"Processing error: {str(e)}")
        return None

#  Main app UI
def main():
    st.title(" Voice Isolator")
    st.markdown("Upload audio to extract clean vocals")

    #  Upload audio file (MP3/WAV)
    uploaded_file = st.file_uploader(
        "Upload MP3/WAV (max 10MB)", 
        type=["mp3", "wav"],
        accept_multiple_files=False
    )

    if uploaded_file:
        col1, col2 = st.columns([5, 5])  # Split layout into two columns

        #  Play original audio
        with col1:
            st.subheader("Original Audio")
            st.audio(uploaded_file)

        #  Isolate vocals when button is clicked
        with col2:
            if st.button("Isolate Vocals", type="primary"):
                with st.spinner("Processing..."):
                    progress_bar = st.progress(0)
                    audio_bytes = uploaded_file.read()
                    isolated = isolate_voice(audio_bytes, progress_bar)

                    if isolated:
                        st.subheader(" Isolated Vocals")
                        st.audio(isolated)

                        #  Download isolated vocals
                        st.download_button(
                            " Download Clean Vocals",
                            data=isolated,
                            file_name="isolated_vocals.wav",
                            mime="audio/wav",
                            type="primary"
                        )

# Run the app
if __name__ == "__main__":
    main()

