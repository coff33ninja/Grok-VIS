"""
Text-to-Speech (TTS) management module.
Handles TTS initialization and speech synthesis.
"""
from TTS.api import TTS

# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak(text):
    """Synthesize speech from text."""
    tts.tts_to_file(text=text, file_path="temp.wav")
    # Play the audio file using sounddevice or other audio player
