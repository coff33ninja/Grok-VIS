"""Text-to-Speech (TTS) management module.
Handles lazy TTS initialization and speech synthesis.
"""

import os
import logging
from TTS.api import TTS
import sounddevice as sd
import soundfile as sf

# Configure logging to keep track of the system’s groove
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Global variable for TTS instance
_tts_instance = None

def get_tts_instance():
    """Lazily initialize and return the TTS instance."""
    global _tts_instance
    if _tts_instance is None:
        try:
            # Import hardware manager here to avoid circular imports
            from grokvis.hardware_manager import get_hardware_manager
            
            # Get hardware-optimized TTS configuration
            hw_manager = get_hardware_manager()
            tts_config = hw_manager.get_tts_config()
            
            logger.info(f"Initializing TTS instance with config: {tts_config}")
            logger.info(f"Hardware detected: {hw_manager.get_summary()}")
            
            _tts_instance = TTS(**tts_config)
            
            # Log which device is being used
            device_type = "GPU" if tts_config['gpu'] else "CPU"
            logger.info(f"TTS initialized using {device_type}")
            
        except Exception as e:
            logger.error("Failed to initialize TTS: %s", e)
            # Fallback to CPU-only configuration if hardware detection fails
            logger.info("Falling back to CPU-only configuration")
            _tts_instance = TTS(
                model_name="tts_models/en/ljspeech/tacotron2-DDC",
                progress_bar=False,
                gpu=True
            )
    return _tts_instance

def speak(text, persona="Default", command=None):
    """
    Synthesize speech from text and play it in real-time.
    
    Parameters:
        text (str): The text to be synthesized.
        persona (str, optional): Identifier for organizing voice samples. Defaults to "Default".
        command (str, optional): Command or label used to name the output file. If None, a timestamp will be used.
    """
    # If command is not provided, use a timestamp
    if command is None:
        import datetime
        command = f"speech_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Construct the directory and file path
    directory = os.path.join("models/voice", persona)
    file_path = os.path.join(directory, f"{command}.wav")

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Synthesize and play the audio in real-time
    try:
        tts = get_tts_instance()
        logger.info("Synthesizing speech for text: '%s'", text)
        audio_data = tts.tts(text=text)
        
        # Play the audio data using sounddevice
        logger.info("Playing synthesized audio in real-time")
        sd.play(audio_data, samplerate=tts.sample_rate)
        sd.wait()
    except Exception as e:
        logger.error("Failed to synthesize or play speech: %s", e)
        raise
    """
    Synthesize speech from text, save it as a WAV file, and play it.
    
    Parameters:
        text (str): The text to be synthesized.
        persona (str, optional): Identifier for organizing voice samples. Defaults to "Default".
        command (str, optional): Command or label used to name the output file. If None, a timestamp will be used.
    """
    # If command is not provided, use a timestamp
    if command is None:
        import datetime
        command = f"speech_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    # Construct the directory and file path
    directory = os.path.join("models/voice", persona)
    file_path = os.path.join(directory, f"{command}.wav")

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # If the file isn't already synthesized, generate it
    if not os.path.isfile(file_path):
        try:
            tts = get_tts_instance()
            logger.info("Synthesizing speech for text: '%s'", text)
            tts.tts_to_file(text=text, file_path=file_path)
        except Exception as e:
            logger.error("Failed to synthesize speech: %s", e)
            raise

    # Play the audio file using sounddevice
    try:
        data, fs = sf.read(file_path, dtype='float32')
        logger.info("Playing audio file: %s", file_path)
        sd.play(data, fs)
        sd.wait()
    except Exception as e:
        logger.error("Error during audio playback: %s", e)
        raise
