# Import necessary libraries
import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from io import BytesIO
import matplotlib.pyplot as plt

# Page subtitle
st.subheader("Sound Effects ")

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

# Function to apply selected audio effect
def apply_effect(audio_bytes, effect_name, **params):
    """Apply sound effect to audio bytes"""
    
    # Load audio from uploaded file bytes
    y, sr = librosa.load(BytesIO(audio_bytes), sr=None)
    
    # Apply different effects based on selection
    if effect_name == "Reverb":
        wet = params.get("wet_level", 0.3)  # Get reverb mix level
        delay = int(sr * params.get("delay_ms", 100)/1000)  # Convert ms to sample delay
        y_eff = y + wet * np.roll(y, delay)  # Add delayed signal
    
    elif effect_name == "Echo":
        repeats = params.get("repeats", 3)  # How many echoes
        decay = params.get("decay", 0.5)  # Echo decay factor
        y_eff = y.copy()
        for i in range(1, repeats+1):
            y_eff += decay**i * np.roll(y, i*int(sr*0.2))  # Add delayed decaying echoes

    elif effect_name == "Pitch Shift":
        steps = params.get("steps", 4)  # Number of semitone steps
        y_eff = librosa.effects.pitch_shift(y, sr=sr, n_steps=steps)  # Shift pitch

    elif effect_name == "Distortion":
        gain = params.get("gain", 20)  # How strong the distortion
        y_eff = np.tanh(y * gain)  # Apply soft clipping distortion

    elif effect_name == "Robot Voice":
        y_fft = librosa.stft(y)  # Convert to frequency domain
        y_mag = np.abs(y_fft)  # Get magnitude only (remove phase variation)
        y_eff = librosa.istft(y_mag * np.exp(1j * np.angle(y_fft)))  # Reconstruct with original phase

    else:  # No effect applied
        y_eff = y

    # Write processed audio to memory buffer as WAV
    buffer = BytesIO()
    sf.write(buffer, y_eff, sr, format='WAV')
    buffer.seek(0)  # Reset pointer to start
    return buffer  # Return processed audio as BytesIO object

# Function to display waveform
def plot_waveform(y, sr, title):
    fig, ax = plt.subplots(figsize=(10, 3))  # Create plot area
    librosa.display.waveshow(y, sr=sr, ax=ax)  # Plot waveform
    ax.set_title(title)  # Set title
    ax.grid(True)
    st.pyplot(fig)  # Display plot in Streamlit

# Main app function
def main():
    st.title("  Sound Effects")  # App title
    st.markdown("Apply studio-quality effects to your audio files")  # Description
    
    # File uploader accepts common audio formats
    uploaded_file = st.file_uploader(
        "Upload Audio (MP3 WAV OGG M4A FLAC max 10MB)",
        type=["mp3", "wav","ogg","m4a","flac"]
    )
    
    if uploaded_file:
        # Create two side-by-side columns
        col1, col2 = st.columns([5, 5])
        
        with col1:
            st.subheader("Original Audio")
            st.audio(uploaded_file)  # Play uploaded audio
            y_orig, sr = librosa.load(BytesIO(uploaded_file.read()), sr=None)  # Load audio
            plot_waveform(y_orig, sr, "Original Waveform")  # Show waveform
            uploaded_file.seek(0)  # Reset pointer so it can be read again
            
        with col2:
            st.subheader("Effects Panel")
            
            # Select sound effect from dropdown
            effect = st.selectbox(
                "Choose Effect",
                ["None", "Reverb", "Echo", "Pitch Shift", "Distortion", "Robot Voice"]
            )
            
            # Define effect parameters dynamically based on selection
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
            
            # When "Apply Effect" button is clicked
            if st.button("Apply Effect", type="primary"):
                with st.spinner("Processing..."):  # Show spinner during processing
                    audio_bytes = uploaded_file.read()  # Read audio as bytes
                    processed = apply_effect(audio_bytes, effect, **params)  # Apply effect
                    
                    st.subheader("Processed Audio")
                    st.audio(processed)  # Play processed audio
                    
                    y_proc, sr = librosa.load(processed, sr=None)  # Load processed audio
                    plot_waveform(y_proc, sr, f"{effect} Effect")  # Show new waveform
                    
                    # Download button for processed audio
                    st.download_button(
                        "Download Processed Audio",
                        data=processed,
                        file_name=f"processed_{effect.lower().replace(' ','_')}.wav",
                        mime="audio/wav"
                    )

# Launch the app
if __name__ == "__main__":
    main()

   
