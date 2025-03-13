"""Text-to-Speech (TTS) management module.
Handles TTS initialization and speech synthesis.
"""
from TTS.api import TTS
import os
import sounddevice as sd
import soundfile as sf

# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak(text, persona, command):
    """Synthesize speech from text and save to a file based on persona and command."""
    # Construct the directory and file path
    directory = f"voice_samples/{persona}"
    file_path = os.path.join(directory, f"{command}.wav")

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Check if the audio file already exists
    if not os.path.isfile(file_path):
        tts.tts_to_file(text=text, file_path=file_path)

    # Play the audio file using sounddevice
    data, fs = sf.read(file_path, dtype='float32')  # Load the audio file
    sd.play(data, fs)  # Play the audio file
    sd.wait()  # Wait until the audio is finished playing
