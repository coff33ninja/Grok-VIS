import os
from grokvis.setup_wakeword import download_wakeword_file, extract_wakeword_file
import datetime
import logging
import sounddevice as sd
import speech_recognition as sr
import librosa
import numpy as np
import joblib
import glob
from sklearn.svm import OneClassSVM
import pvporcupine
from grokvis.shared import model, wake_word_handle, persona
from grokvis.tts_manager import speak

def extract_mfcc(filename):
    """Extract MFCC features from an audio file."""
    try:
        y, sr = librosa.load(filename, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return np.mean(mfcc.T, axis=0)
    except Exception as e:
        logging.error(f"MFCC Extraction Error: {e}")
        return None

def train_one_class_model(directory):
    """Train a one-class SVM model on voice samples."""
    try:
        features = []
        for file in glob.glob(f"{directory}/*.wav"):
            mfcc = extract_mfcc(file)
            if mfcc is not None:
                features.append(mfcc)
        if not features:
            raise ValueError("No valid audio samples found for training.")
        clf = OneClassSVM(kernel='rbf', gamma='auto', nu=0.01)
        clf.fit(features)
        joblib.dump(clf, 'models/voice/voice_model.pkl')
        return clf
    except Exception as e:
        logging.error(f"Model Training Error: {e}")
        speak("Sorry, I couldn't train the voice model. Please check your samples and try again.")
        return None

def train_voice_model(retrain=False):
    """Load or train the voice model. Optionally retrain with new samples."""
    global model
    try:
        if retrain or not os.path.exists('models/voice/voice_model.pkl'):
            raise FileNotFoundError("Forcing retrain or model not found.")
        model = joblib.load('models/voice/voice_model.pkl')
        speak("Voice model loaded successfully.")
    except FileNotFoundError:
        speak("I need to learn your voice. Please say 10 phrases after each prompt.")
        if not os.path.exists('voice_samples/my_voice'):
            os.makedirs('voice_samples/my_voice')
        for i in range(10):
            speak(f"Phrase {i+1}:")
            record_clip(f"voice_samples/my_voice/sample_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.wav")
        model = train_one_class_model('voice_samples/my_voice')
        if model:
            speak("Voice model trained successfully. I'll only listen to you now!")
    return model

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
        speak("Sorry, I couldn't record that. Please check your microphone and try again.")

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
        speak("Sorry, I didn't catch that. Please repeat your command.")
        return ""
    except Exception as e:
        logging.error(f"Listening Error: {e}")
        speak("Sorry, I couldn't process that command. Please try again.")
        return ""

def wake_word_listener(sensitivity=0.5):
    """Listen for the wake word 'Hey Grok' using Porcupine."""
    global wake_word_handle
    try:
        access_key = os.environ.get("PICOVOICE_ACCESS_KEY", "YpmwAcCDdDu82WlIAbZWMn840MiaGELoTIt+Ssh3LivetKM1k+Nw3w==")
        keywords = ["Hey Grok"]
        zip_path = download_wakeword_file()
        if zip_path:
            extract_wakeword_file(zip_path)

        try:
            wake_word_handle = pvporcupine.create(
                model_path='models/wakeword/Hey--Grok_en_windows_v3_0_0.ppn',
                access_key=access_key, keywords=keywords, sensitivities=[sensitivity]
            )
        except pvporcupine.PorcupineInvalidArgumentError as e:
            logging.error(f"Invalid argument for Porcupine: {e}")
            speak("Wake word detection failed due to invalid configuration.")
            return
        except pvporcupine.PorcupineActivationError as e:
            logging.error(f"Porcupine activation error: {e}. Please check the model path and access key.")
            speak("Wake word detection failed due to invalid access key.")
            return

        def audio_callback(indata, _frames, _time, status):
            """Process audio input for wake word detection."""
            if status:
                logging.warning(f"Audio callback status: {status}")
                return
            pcm = indata.flatten().astype(np.int16)
            keyword_index = wake_word_handle.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected! Executing command...")
                sd.stop()
                command = listen()
                if command:
                    from grokvis.commands import process_command
                    process_command(command)
                sd.start()

        print(f"Listening for wake word with sensitivity {sensitivity}... (Press Ctrl+C to exit)")
        with sd.InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=wake_word_handle.sample_rate,
            blocksize=wake_word_handle.frame_length,
            dtype=np.int16,
        ):
            try:
                while True:
                    sd.sleep(100)
            except KeyboardInterrupt:
                print("Wake word detection stopped.")
            finally:
                if wake_word_handle:
                    wake_word_handle.delete()
                    wake_word_handle = None
    except Exception as e:
        logging.error(f"Wake Word Detection Error: {e}")
        speak("Sorry, wake word detection failed.")
        if wake_word_handle:
            wake_word_handle.delete()
            wake_word_handle = None

def setup_personality():
    """First-time setup to choose between Alfred (male) or Beatrice (female) persona."""
    try:
        if os.path.exists('persona_config.txt'):
            with open('persona_config.txt', 'r') as f:
                persona = f.read().strip()
            print(f"Welcome back, I'm {persona}.")
            return persona

        speak("Welcome! I need a persona. Would you prefer Alfred, the gentleman, or Beatrice, the lady? Say 'Alfred' or 'Beatrice'.")

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
            persona = "Alfred"
            print("Very well, I'm Alfred, at your service.")
        elif "beatrice" in choice.lower():
            persona = "Beatrice"
            print("Delighted! I'm Beatrice, ready to assist with elegance.")
        else:
            print("I didn't catch that. Defaulting to Alfred for now.")
            persona = "Alfred"

        with open('persona_config.txt', 'w') as f:
            f.write(persona)

        return persona
    except Exception as e:
        logging.error(f"Persona Setup Error: {e}")
        print("Sorry, something went wrong during setup. Defaulting to Alfred.")
        return "Alfred"