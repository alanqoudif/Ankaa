"""
Voice UI components for the Streamlit interface of the Legal AI Assistant.
"""

import os
import time
import streamlit as st
from typing import Callable, Optional
import base64

def render_voice_input_button(on_voice_input: Callable[[str], None]):
    """
    Render a button for voice input.
    
    Args:
        on_voice_input: Callback function to handle the transcribed voice input
    """
    # Get the current language from session state
    lang = st.session_state.language
    
    # Translations
    button_text = "Voice Input" if lang == "en" else "إدخال صوتي"
    recording_text = "Recording... Click to stop" if lang == "en" else "جاري التسجيل... انقر للإيقاف"
    processing_text = "Processing your voice input..." if lang == "en" else "جاري معالجة المدخلات الصوتية..."
    
    # Check if voice processor is initialized
    if "voice_processor" not in st.session_state or st.session_state.voice_processor is None:
        st.warning("Voice input is not available. Please check voice processor initialization.")
        return
    
    # Create a container for the voice input button
    voice_container = st.container()
    
    with voice_container:
        # Create columns for the button and status
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Check if we're already recording
            is_recording = st.session_state.get("is_recording", False)
            
            if is_recording:
                # Show stop recording button
                if st.button(recording_text, key="stop_recording", type="primary"):
                    st.session_state.is_recording = False
                    
                    # Show processing message
                    with col2:
                        with st.spinner(processing_text):
                            # Stop recording and get the transcribed text
                            transcribed_text = st.session_state.voice_processor.stop_recording()
                            
                            if transcribed_text:
                                # Call the callback function with the transcribed text
                                on_voice_input(transcribed_text)
                            else:
                                st.error("No speech detected. Please try again.")
            else:
                # Show start recording button
                if st.button(button_text, key="start_recording"):
                    st.session_state.is_recording = True
                    
                    # Start recording
                    st.session_state.voice_processor.start_recording()
                    
                    # Force a rerun to show the stop button
                    st.rerun()
        
        # Show recording status
        with col2:
            if is_recording:
                # Show a pulsing recording indicator
                st.markdown("""
                <style>
                .recording-indicator {
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    background-color: red;
                    border-radius: 50%;
                    margin-right: 8px;
                    animation: pulse 1.5s infinite;
                }
                @keyframes pulse {
                    0% { opacity: 1; }
                    50% { opacity: 0.3; }
                    100% { opacity: 1; }
                }
                </style>
                <div>
                    <span class="recording-indicator"></span>
                    <span>Recording...</span>
                </div>
                """, unsafe_allow_html=True)

def render_text_to_speech_button(text: str):
    """
    Render a button to read the text aloud.
    
    Args:
        text: The text to read aloud
    """
    # Get the current language from session state
    lang = st.session_state.language
    
    # Translations
    button_text = "Read Aloud" if lang == "en" else "قراءة بصوت عالٍ"
    
    # Check if TTS engine is initialized
    if "tts_engine" not in st.session_state or st.session_state.tts_engine is None:
        return
    
    # Create a unique key for this button
    button_key = f"tts_button_{hash(text)}"
    
    if st.button(button_text, key=button_key):
        # Generate speech
        audio_file = st.session_state.tts_engine.speak(text)
        
        # If using gTTS, play the audio file
        if audio_file and os.path.exists(audio_file):
            try:
                # Read the audio file
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                
                # Create a base64 encoded audio string
                audio_base64 = base64.b64encode(audio_bytes).decode()
                
                # Create an HTML audio element
                audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
                """
                
                # Display the audio element
                st.markdown(audio_html, unsafe_allow_html=True)
                
                # Clean up the audio file after a delay
                def cleanup_audio_file():
                    time.sleep(60)  # Wait for 60 seconds
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                
                # Start cleanup in a separate thread
                import threading
                cleanup_thread = threading.Thread(target=cleanup_audio_file)
                cleanup_thread.daemon = True
                cleanup_thread.start()
                
            except Exception as e:
                st.error(f"Error playing audio: {e}")

def render_voice_status(is_available: bool, model_path: Optional[str] = None):
    """
    Render the status of voice recognition.
    
    Args:
        is_available: Whether voice recognition is available
        model_path: Path to the voice recognition model
    """
    # Get the current language from session state
    lang = st.session_state.language
    
    if is_available:
        st.success("Voice recognition is available" if lang == "en" else "التعرف على الصوت متاح")
        if model_path:
            st.info(f"Using model: {os.path.basename(model_path)}")
    else:
        st.warning("Voice recognition is not available" if lang == "en" else "التعرف على الصوت غير متاح")
        st.info("Install required packages: pip install vosk sounddevice soundfile" if lang == "en" else 
                "قم بتثبيت الحزم المطلوبة: pip install vosk sounddevice soundfile")

def download_vosk_model():
    """Render a button to download the Vosk model for offline voice recognition."""
    # Get the current language from session state
    lang = st.session_state.language
    
    # Translations
    button_text = "Download Vosk Model for Offline Voice Recognition" if lang == "en" else "تحميل نموذج Vosk للتعرف على الصوت بدون إنترنت"
    downloading_text = "Downloading Vosk model..." if lang == "en" else "جاري تحميل نموذج Vosk..."
    
    if st.button(button_text):
        with st.spinner(downloading_text):
            from utils.voice_utils import download_vosk_model
            model_path = download_vosk_model()
            
            if model_path and os.path.exists(model_path):
                st.success(f"Vosk model downloaded to {model_path}")
                
                # Initialize voice processor with the downloaded model
                from utils.voice_utils import VoiceProcessor
                try:
                    st.session_state.voice_processor = VoiceProcessor(use_vosk=True, model_path=model_path)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error initializing voice processor: {e}")
            else:
                st.error("Failed to download Vosk model")
