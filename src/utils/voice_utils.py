"""
Voice processing utilities for the Sultanate Legal AI Assistant.
Provides functionality for voice-to-text and text-to-speech.
"""

import os
import tempfile
import threading
import queue
import time
import json
import numpy as np
from typing import Optional, Callable, Dict, Any, List
import streamlit as st

# Optional imports that will be checked at runtime
try:
    import sys
    import importlib
    import subprocess
    import os
    
    # Try to import sounddevice
    try:
        import sounddevice as sd
        SOUNDDEVICE_AVAILABLE = True
    except ImportError:
        # Try to install it if not available
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "sounddevice"])
            importlib.invalidate_caches()
            import sounddevice as sd
            SOUNDDEVICE_AVAILABLE = True
        except Exception as e:
            print(f"Error installing sounddevice: {e}")
            SOUNDDEVICE_AVAILABLE = False
    
    # Try to import vosk
    try:
        from vosk import Model, KaldiRecognizer
        VOSK_AVAILABLE = True
    except ImportError:
        VOSK_AVAILABLE = False
    
    # Try to import pyttsx3
    try:
        import pyttsx3
        PYTTSX3_AVAILABLE = True
    except ImportError:
        # Try to install it if not available
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyttsx3"])
            importlib.invalidate_caches()
            import pyttsx3
            PYTTSX3_AVAILABLE = True
        except Exception as e:
            print(f"Error installing pyttsx3: {e}")
            PYTTSX3_AVAILABLE = False
            
except Exception as e:
    print(f"Error during library detection: {e}")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

class VoiceProcessor:
    """Class for handling voice input and converting it to text."""
    
    def __init__(self, use_vosk: bool = True, model_path: Optional[str] = None):
        """
        Initialize the voice processor.
        
        Args:
            use_vosk: Whether to use Vosk for offline voice recognition
            model_path: Path to the Vosk model directory
        """
        self.use_vosk = use_vosk
        self.model_path = model_path
        self.vosk_model = None
        self.recognizer = None
        self.recording = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None
        self.sample_rate = 16000  # Default sample rate for Vosk
        self.initialized = False
        self.init_error = None
        
        # Force reload of the libraries to ensure they're properly detected
        self._reload_libraries()
        
        # Check if required libraries are available
        if not SOUNDDEVICE_AVAILABLE:
            self.init_error = "sounddevice library is required for voice input. Install it with 'pip install sounddevice'."
            st.warning(self.init_error)
            return
        
        # Initialize Vosk if selected
        if use_vosk:
            if not VOSK_AVAILABLE:
                self.init_error = "Vosk library is required for offline voice recognition. Install it with 'pip install vosk'."
                st.warning(self.init_error)
                return
            
            if model_path and os.path.exists(model_path) and os.path.isdir(model_path):
                # Check if the model directory has content
                if len(os.listdir(model_path)) == 0:
                    self.init_error = f"Vosk model directory exists but is empty: {model_path}"
                    st.warning(self.init_error)
                    st.info("Please download a valid Vosk model using the download button.")
                    return
                    
                try:
                    st.info(f"Initializing Vosk model from {model_path}...")
                    self.vosk_model = Model(model_path)
                    self.recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)
                    self.initialized = True
                    st.success("Vosk model initialized successfully!")
                except Exception as e:
                    self.init_error = f"Error initializing Vosk model: {e}"
                    st.error(self.init_error)
                    st.info("Please download a valid Vosk model using the download button.")
            else:
                self.init_error = f"Vosk model path not found or is not a directory: {model_path}"
                st.warning(self.init_error)
                st.info("Please download a valid Vosk model using the download button.")
        else:
            # Using Whisper API
            try:
                import openai
                # Check if API key is set
                if not os.environ.get("OPENAI_API_KEY"):
                    self.init_error = "OpenAI API key not set. Please set the OPENAI_API_KEY environment variable."
                    st.warning(self.init_error)
                    st.info("Alternatively, download and use the Vosk model for offline voice recognition.")
                    return
                    
                self.initialized = True
                st.success("Voice processor initialized with Whisper API")
            except ImportError:
                self.init_error = "OpenAI library is required for Whisper API. Install it with 'pip install openai'."
                st.error(self.init_error)
    
    def _reload_libraries(self):
        """Force reload of required libraries to ensure they're properly detected."""
        global SOUNDDEVICE_AVAILABLE, VOSK_AVAILABLE, PYTTSX3_AVAILABLE
        
        try:
            import sys
            import importlib
            
            # Try to import sounddevice
            try:
                if 'sounddevice' in sys.modules:
                    importlib.reload(sys.modules['sounddevice'])
                import sounddevice as sd
                SOUNDDEVICE_AVAILABLE = True
            except ImportError:
                SOUNDDEVICE_AVAILABLE = False
            
            # Try to import vosk
            try:
                if 'vosk' in sys.modules:
                    importlib.reload(sys.modules['vosk'])
                from vosk import Model, KaldiRecognizer
                VOSK_AVAILABLE = True
            except ImportError:
                VOSK_AVAILABLE = False
            
            # Try to import pyttsx3
            try:
                if 'pyttsx3' in sys.modules:
                    importlib.reload(sys.modules['pyttsx3'])
                import pyttsx3
                PYTTSX3_AVAILABLE = True
            except ImportError:
                PYTTSX3_AVAILABLE = False
                
        except Exception as e:
            print(f"Error during library reload: {e}")
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback function for audio recording."""
        if status:
            print(f"Audio callback status: {status}")
        if self.recording:
            self.audio_queue.put(indata.copy())
    
    def start_recording(self):
        """Start recording audio from the microphone."""
        if not self.initialized:
            st.error("Voice processor is not properly initialized. Please initialize it first.")
            return
            
        if self.recording:
            return
        
        self.recording = True
        self.audio_queue = queue.Queue()
        
        # Start the recording in a separate thread
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()
    
    def _record_audio(self):
        """Record audio from the microphone."""
        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, callback=self._audio_callback):
                while self.recording:
                    time.sleep(0.1)
        except Exception as e:
            print(f"Error recording audio: {e}")
            self.recording = False
    
    def stop_recording(self) -> str:
        """
        Stop recording and process the audio to text.
        
        Returns:
            The transcribed text
        """
        if not self.initialized:
            st.error("Voice processor is not properly initialized. Please initialize it first.")
            return ""
            
        if not self.recording:
            return ""
        
        self.recording = False
        
        # Wait for the recording thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=1.0)
        
        # Process the recorded audio
        if self.use_vosk:
            return self._process_with_vosk()
        else:
            return self._process_with_whisper()
    
    def _process_with_vosk(self) -> str:
        """
        Process the recorded audio with Vosk.
        
        Returns:
            The transcribed text
        """
        if not self.initialized or not self.recognizer:
            st.error("Vosk recognizer not initialized. Please initialize the voice processor first.")
            return "Error: Vosk recognizer not initialized"
        
        # Reset the recognizer
        self.recognizer.Reset()
        
        # Check if we have any audio data
        if self.audio_queue.empty():
            st.warning("No audio data recorded. Please try speaking louder or check your microphone.")
            return ""
        
        # Process all audio chunks
        while not self.audio_queue.empty():
            audio_chunk = self.audio_queue.get()
            if len(audio_chunk) > 0:
                self.recognizer.AcceptWaveform(audio_chunk.tobytes())
        
        # Get the final result
        result_json = self.recognizer.FinalResult()
        try:
            result = json.loads(result_json)
            text = result.get("text", "")
            if not text:
                st.warning("No speech detected. Please try speaking louder or check your microphone.")
            return text
        except json.JSONDecodeError:
            st.error("Error processing audio data.")
            return "Error processing audio"
    
    def _process_with_whisper(self) -> str:
        """
        Process the recorded audio with OpenAI's Whisper API.
        
        Returns:
            The transcribed text
        """
        try:
            import openai
        except ImportError:
            return "Error: OpenAI library not installed. Install it with 'pip install openai'."
        
        # Check if API key is set
        if not openai.api_key:
            return "Error: OpenAI API key not set. Please set the OPENAI_API_KEY environment variable."
        
        # Save the recorded audio to a temporary file
        audio_data = []
        while not self.audio_queue.empty():
            audio_chunk = self.audio_queue.get()
            audio_data.append(audio_chunk)
        
        if not audio_data:
            return "No audio recorded"
        
        audio_data = np.concatenate(audio_data, axis=0)
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            sf.write(temp_file.name, audio_data, self.sample_rate)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe with Whisper API
            with open(temp_file_path, "rb") as audio_file:
                client = openai.OpenAI()
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                return transcript.text
        except Exception as e:
            return f"Error transcribing audio: {e}"
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


class TextToSpeech:
    """Class for converting text to speech."""
    
    def __init__(self, use_pyttsx3: bool = True, language: str = "en"):
        """
        Initialize the text-to-speech engine.
        
        Args:
            use_pyttsx3: Whether to use pyttsx3 for offline TTS
            language: Language for TTS (en or ar)
        """
        self.use_pyttsx3 = use_pyttsx3
        self.language = language
        self.engine = None
        self.initialized = False
        self.init_error = None
        
        # Force reload of the libraries to ensure they're properly detected
        self._reload_libraries()
        
        # Initialize pyttsx3 if selected
        if use_pyttsx3:
            if not PYTTSX3_AVAILABLE:
                self.init_error = "pyttsx3 library is required for offline TTS. Install it with 'pip install pyttsx3'."
                st.warning(self.init_error)
                return
            
            try:
                self.engine = pyttsx3.init()
                
                # Set language properties
                if language == "ar":
                    # Try to find an Arabic voice
                    voices = self.engine.getProperty('voices')
                    for voice in voices:
                        if "arabic" in voice.name.lower():
                            self.engine.setProperty('voice', voice.id)
                            break
                
                self.initialized = True
                st.success("Text-to-speech engine initialized successfully!")
            except Exception as e:
                self.init_error = f"Error initializing pyttsx3: {e}"
                st.error(self.init_error)
        else:
            # Using gTTS (requires internet)
            if not GTTS_AVAILABLE:
                st.warning("gTTS library is required for online TTS. Install it with 'pip install gtts'.")
                return
            self.initialized = True
            st.success("Text-to-speech engine initialized with gTTS (requires internet)")
    
    def _reload_libraries(self):
        """Force reload of required libraries to ensure they're properly detected."""
        global PYTTSX3_AVAILABLE, GTTS_AVAILABLE
        
        try:
            import sys
            import importlib
            
            # Try to import pyttsx3
            try:
                if 'pyttsx3' in sys.modules:
                    importlib.reload(sys.modules['pyttsx3'])
                import pyttsx3
                PYTTSX3_AVAILABLE = True
            except ImportError:
                PYTTSX3_AVAILABLE = False
            
            # Try to import gtts
            try:
                if 'gtts' in sys.modules:
                    importlib.reload(sys.modules['gtts'])
                from gtts import gTTS
                GTTS_AVAILABLE = True
            except ImportError:
                GTTS_AVAILABLE = False
                
        except Exception as e:
            print(f"Error during library reload: {e}")
    
    def speak(self, text: str) -> str:
        """
        Convert text to speech and play it.
        
        Args:
            text: The text to convert to speech
            
        Returns:
            Path to the audio file (for gTTS) or empty string (for pyttsx3)
        """
        if not self.initialized:
            st.error("Text-to-speech engine is not properly initialized.")
            return ""
            
        if self.use_pyttsx3:
            return self._speak_pyttsx3(text)
        else:
            return self._speak_gtts(text)
    
    def _speak_pyttsx3(self, text: str) -> str:
        """
        Speak the text using pyttsx3.
        
        Args:
            text: The text to speak
            
        Returns:
            Empty string (pyttsx3 plays audio directly)
        """
        if not self.engine:
            st.error("pyttsx3 engine not initialized.")
            return ""
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return ""
        except Exception as e:
            st.error(f"Error speaking text with pyttsx3: {e}")
            # Try falling back to gTTS if pyttsx3 fails
            if GTTS_AVAILABLE:
                st.info("Falling back to gTTS for this request.")
                return self._speak_gtts(text)
            return ""
    
    def _speak_gtts(self, text: str) -> str:
        """
        Speak the text using gTTS.
        
        Args:
            text: The text to speak
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file_path = temp_file.name
            
            # Generate the speech
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(temp_file_path)
            
            return temp_file_path
        except Exception as e:
            print(f"Error generating speech: {e}")
            return ""


def download_vosk_model(model_name="vosk-model-small-en-us-0.15", model_dir="models"):
    """Download a Vosk model for offline speech recognition."""
    import os
    import zipfile
    import requests
    import streamlit as st
    from tqdm import tqdm
    
    # Create model directory if it doesn't exist
    os.makedirs(model_dir, exist_ok=True)
    
    # Model URL
    model_url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    model_path = os.path.join(model_dir, model_name)
    zip_path = os.path.join(model_dir, f"{model_name}.zip")
    
    # Check if model already exists
    if os.path.exists(model_path) and os.path.isdir(model_path) and len(os.listdir(model_path)) > 0:
        print(f"Vosk model already exists at {model_path}")
        return model_path
    
    try:
        # Download the model
        with st.spinner(f"Downloading Vosk model from {model_url}..."):
            print(f"Downloading Vosk model from {model_url}...")
            response = requests.get(model_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            
            progress_bar = st.progress(0)
            
            with open(zip_path, 'wb') as f, tqdm(total=total_size, unit='iB', unit_scale=True) as t:
                downloaded = 0
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    t.update(len(data))
                    f.write(data)
                    # Update progress bar
                    if total_size > 0:
                        progress = min(downloaded / total_size, 1.0)
                        progress_bar.progress(progress)
            
            # Extract the model
            with st.spinner(f"Extracting model to {model_path}..."):
                print(f"Extracting model to {model_path}...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(model_dir)
            
            # Remove the zip file
            os.remove(zip_path)
            
            st.success(f"Vosk model downloaded and extracted to {model_path}")
            print(f"Vosk model downloaded and extracted to {model_path}")
            return model_path
    except Exception as e:
        error_msg = f"Error downloading Vosk model: {e}"
        st.error(error_msg)
        print(error_msg)
        return None
