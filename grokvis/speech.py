"""
Speech and audio processing functionality for GrokVIS.
Handles speech recognition, text-to-speech, and voice model training.
"""
import os
import datetime
import logging
import struct
import speech_recognition as sr
import sounddevice as sd
import librosa
import numpy as np
import joblib
import glob
from sklearn.svm import OneClassSVM
import pvporcupine

# Import from core module
from grokvis.core import tts, model, wake_word_handle, jarvis_quips, persona
from grokvis.commands import process_command

def speak(text):
    """Speak the given text aloud using Coqui TTS."""
    try:
        print(text)
        tts.tts_to_file(text=text, file_path="output.wav")
        audio_data, samplerate = sd.read("output.wav")
        sd.play(audio_data, samplerate=samplerate)
        sd.wait()
    except Exception as e:
        logging.error(f"TTS Error: {e}")
        print("Sorry, I couldn't speak right now.")

def record_clip(filename):
    """Record a short audio clip and save it to a file."""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something...")
            audio = recognizer.listen(source)
            with open(filename, "wb") as f:
                f.write(audio.get_wav_data())
    except Exception as e:
        logging.error(f"Recording Error: {e}")
        speak("Sorry, I couldn't record that.")

def extract_mfcc(file_path):
    """Extract MFCC features from an audio file."""
    try:
        audio, sample_rate = librosa.load(file_path, sr=16000)
        mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
        return np.mean(mfcc.T, axis=0)
    except Exception as e:
        logging.error(f"MFCC Extraction Error: {e}")
        return None

def train_one_class_model(directory):
    """Train a One-Class SVM model on voice samples."""
    try:
        files = glob.glob(f"{directory}/*.wav")
        X = [extract_mfcc(f) for f in files if extract_mfcc(f) is not None]
        model = OneClassSVM(kernel='rbf', gamma='auto')
        model.fit(X)
        joblib.dump(model, 'voice_model.pkl')
        return model
    except Exception as e:
        logging.error(f"Model Training Error: {e}")
        speak("Sorry, I couldn't train the voice model.")
        return None

def listen():
    """Listen for a command and verify the speaker's voice."""
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())
            mfcc = extract_mfcc("temp.wav")
            if mfcc is None or model.predict([mfcc]) != 1:
                speak("Sorry, I only listen to my owner.")
                return ""
            command = recognizer.recognize_google(audio).lower()
            return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except Exception as e:
        logging.error(f"Listening Error: {e}")
        speak("Sorry, I couldn't process that command.")
        return ""

def wake_word_listener():
    """Listen for the wake word 'Hey GrokVis' using Porcupine."""
    global wake_word_handle
    try:
        access_key = "YOUR_PICOVOICE_ACCESS_KEY"  # Replace with your Picovoice key
        keywords = ["Hey GrokVis"]
        wake_word_handle = pvporcupine.create(access_key=access_key, keywords=keywords, sensitivities=[0.5])

        def audio_callback(indata, frames, time, status):
            pcm = struct.pack('<' + ('h' * len(indata)), *indata)
            if wake_word_handle.process(pcm) >= 0:
                print("Wake word detected!")
                command = listen()
                if command:
                    process_command(command)

        with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, blocksize=512):
            print("Listening for wake word...")
            while True:
                pass
    except Exception as e:
        logging.error(f"Wake Word Detection Error: {e}")
        speak("Sorry, wake word detection failed.")

def setup_personality():
    """First-time setup to choose between Alfred (male) or Beatrice (female) persona."""
    global tts
    try:
        # Check if persona is already set
        if os.path.exists('persona_config.txt'):
            with open('persona_config.txt', 'r') as f:
                persona = f.read().strip()
            if persona == "Alfred":
                tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")  # Male-like voice
                print("Greetings, I'm Alfred, your loyal assistant.")
                # We'll speak after TTS is fully initialized
            elif persona == "Beatrice":
                tts = TTS(model_name="tts_models/en/vctk/vits", speaker="p228")  # Female voice
                print("Hello, I'm Beatrice, here to assist you with grace.")
                # We'll speak after TTS is fully initialized
            return persona

        # First-time setup - use a temporary TTS for the initial prompt
        temp_tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        temp_tts.tts_to_file(
            text="Welcome! I need a persona. Would you prefer Alfred, the gentleman, or Beatrice, the lady? Say 'Alfred' or 'Beatrice'.",
            file_path="output.wav"
        )
        audio_data, samplerate = sd.read("output.wav")
        sd.play(audio_data, samplerate=samplerate)
        sd.wait()
        
        # Listen for response
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for persona choice...")
            audio = recognizer.listen(source)
            try:
                choice = recognizer.recognize_google(audio).lower()
                print(f"You chose: {choice}")
            except:
                choice = ""
                print("Couldn't recognize choice")
        
        if "alfred" in choice.lower():
            tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")  # Male-like voice
            persona = "Alfred"
            print("Very well, I'm Alfred, at your service.")
        elif "beatrice" in choice.lower():
            tts = TTS(model_name="tts_models/en/vctk/vits", speaker="p228")  # Female voice, speaker p228
            persona = "Beatrice"
            print("Delighted! I'm Beatrice, ready to assist with elegance.")
        else:
            print("I didn't catch that. Defaulting to Alfred for now.")
            tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
            persona = "Alfred"
        
        # Save the choice
        with open('persona_config.txt', 'w') as f:
            f.write(persona)
            
        return persona
    except Exception as e:
        logging.error(f"Persona Setup Error: {e}")
        print("Sorry, something went wrong during setup. Defaulting to Alfred.")
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        return "Alfred"

def train_voice_model():
    """Load or train the voice model."""
    global model
    try:
        model = joblib.load('voice_model.pkl')
        speak("Voice model loaded successfully.")
    except FileNotFoundError:
        speak("I need to learn your voice. Please say 10 phrases after each prompt.")
        if not os.path.exists('voice_samples/my_voice'):
            os.makedirs('voice_samples/my_voice')
        for i in range(10):
            speak(f"Phrase {i+1}:")
            record_clip(f"voice_samples/my_voice/sample_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.wav")
        model = train_one_class_model('voice_samples/my_voice')
        speak("Voice model trained. I'll only listen to you now!")
    return model