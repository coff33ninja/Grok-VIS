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
            logger.info("Initializing TTS instance...")
            _tts_instance = TTS(
                model_name="tts_models/en/ljspeech/tacotron2-DDC",
                progress_bar=False,
                gpu=False
            )
        except Exception as e:
            logger.error("Failed to initialize TTS: %s", e)
            raise
    return _tts_instance

def speak(text, persona, command):
    """
    Synthesize speech from text, save it as a WAV file, and play it.
    
    Parameters:
        text (str): The text to be synthesized.
        persona (str): Identifier for organizing voice samples.
        command (str): Command or label used to name the output file.
    """
    # Construct the directory and file path
    directory = os.path.join("voice_samples", persona)
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
