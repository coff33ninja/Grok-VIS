import speech_recognition as sr
import requests
import datetime
import random
import wakeonlan
import socket
import spacy
import sqlite3
import cv2
import psutil
import pynvml
import subprocess
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import librosa
from sklearn.svm import OneClassSVM
import joblib
import glob
import os
import pvporcupine
import struct
import sounddevice as sd
from TTS.api import TTS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template_string
import threading

# Initialize logging
logging.basicConfig(filename='grokvis_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize core components
memory_model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")
pynvml.nvmlInit()
conn = sqlite3.connect("grokvis_memory.db")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
executor = ThreadPoolExecutor(max_workers=2)  # Thread pool for async tasks

# APScheduler setup
jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

# Flask app setup
app = Flask(__name__)

# Personality quips
jarvis_quips = [
    "At your service—Stark would be jealous.",
    "Task complete. Shall I polish your armor next?",
    "I’m no android, but I’ve got your back."
]

# Global variables
model = None
wake_word_handle = None

# Core Functions
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
        print("Sorry, I couldn’t speak right now.")

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
        speak("Sorry, I couldn’t record that.")

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
        speak("Sorry, I couldn’t train the voice model.")
        return None

def listen():
    """Listen for a command and verify the speaker's voice."""
    global model
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
        speak("Sorry, I didn’t catch that.")
        return ""
    except Exception as e:
        logging.error(f"Listening Error: {e}")
        speak("Sorry, I couldn’t process that command.")
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

# Memory Management
def store_memory(command, response):
    """Store a command and response in the memory database."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        embedding = memory_model.encode(command + " " + response).tobytes()
        conn.execute("INSERT INTO memory (timestamp, command, response, embedding) VALUES (?, ?, ?, ?)",
                     (timestamp, command, response, embedding))
        conn.commit()
    except Exception as e:
        logging.error(f"Memory Storage Error: {e}")
        speak("Sorry, I couldn’t store that memory.")

def recall_memory(query, top_k=1):
    """Recall the most similar past command and response."""
    try:
        query_emb = memory_model.encode(query)
        cursor = conn.execute("SELECT command, response, embedding FROM memory")
        results = []
        for cmd, resp, emb_blob in cursor:
            emb = np.frombuffer(emb_blob, dtype=np.float32)
            similarity = cosine_similarity([query_emb], [emb])[0][0]
            results.append((similarity, cmd, resp))
        results.sort(reverse=True)
        return [(cmd, resp) for _, cmd, resp in results[:top_k]]
    except Exception as e:
        logging.error(f"Memory Recall Error: {e}")
        speak("Sorry, I couldn’t recall that memory.")
        return []

def handle_memory(command):
    """Handle memory-related commands."""
    if "remember" in command:
        parts = command.split("remember")[-1].strip()
        store_memory(parts, "Noted.")
        speak(f"Got it, I’ll remember: {parts}.")
    elif "what did i" in command or "recall" in command:
        query = command.split("about")[-1].strip() if "about" in command else command
        recalled = recall_memory(query)
        if recalled:
            cmd, resp = recalled[0]
            speak(f"You said: '{cmd}', and I replied: '{resp}'")
        else:
            speak("Memory’s a bit fuzzy—nothing matches that.")

# Scheduler with APScheduler
def add_event(time_str, task):
    """Schedule an event using APScheduler."""
    try:
        event_time = datetime.datetime.strptime(time_str, "%H:%M")
        event_time = event_time.replace(year=datetime.datetime.now().year,
                                        month=datetime.datetime.now().month,
                                        day=datetime.datetime.now().day)
        if event_time < datetime.datetime.now():
            event_time += datetime.timedelta(days=1)
        scheduler.add_job(speak, 'date', run_date=event_time, args=[f"Reminder: {task} now."])
        speak(f"Scheduled: {task} at {time_str}.")
        store_memory(f"schedule {task} at {time_str}", "Added to calendar.")
    except Exception as e:
        logging.error(f"Scheduling Error: {e}")
        speak("Sorry, I couldn’t schedule that event.")

# Home Automation
def wake_pc(mac_address="YOUR_PC_MAC"):
    """Wake a PC using Wake-on-LAN."""
    try:
        wakeonlan.send_magic_packet(mac_address)
        speak("PC waking up. Don’t fry it.")
    except Exception as e:
        logging.error(f"Wake-on-LAN Error: {e}")
        speak("Sorry, I couldn’t wake the PC.")

def control_device(device, action):
    """Simulate controlling a smart device."""
    try:
        speak(f"{action}ing the {device}. Need more?")
    except Exception as e:
        logging.error(f"Device Control Error: {e}")
        speak("Sorry, I couldn’t control the device.")

# Async Weather Fetching
def fetch_weather(city):
    """Fetch weather data synchronously for threading."""
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    return response['main']['temp'], response['weather'][0]['description']

def get_weather(city):
    """Fetch and announce weather asynchronously."""
    try:
        future = executor.submit(fetch_weather, city)
        temp, desc = future.result()
        speak(f"{city}: {temp}°C, {desc}.")
        return {"temp": temp, "desc": desc}
    except Exception as e:
        logging.error(f"Weather API Error: {e}")
        speak("Sorry, I couldn’t fetch the weather.")

# Flask Dashboard
@app.route('/')
def dashboard():
    """Render the GROK-VIS dashboard."""
    try:
        # Fetch scheduled jobs
        jobs = scheduler.get_jobs()
        scheduled_tasks = [(job.next_run_time.strftime('%Y-%m-%d %H:%M'), job.args[0]) for job in jobs]

        # Fetch recent commands
        with open("command_log.txt", "r") as f:
            commands = f.readlines()[-10:]  # Last 10 commands

        html = """
        <html>
            <head><title>GROK-VIS Dashboard</title></head>
            <body>
                <h1>GROK-VIS Control Panel</h1>
                <h2>Scheduled Tasks</h2>
                <ul>{% for time, task in tasks %}<li>{{ time }} - {{ task }}</li>{% endfor %}</ul>
                <h2>Recent Commands</h2>
                <ul>{% for cmd in commands %}<li>{{ cmd }}</li>{% endfor %}</ul>
            </body>
        </html>
        """
        return render_template_string(html, tasks=scheduled_tasks, commands=commands)
    except Exception as e:
        logging.error(f"Dashboard Error: {e}")
        return "Error loading dashboard."

# Command Processing
def process_command(command):
    """Process the spoken command."""
    try:
        if not command:
            return

        # Log command for future LLM training
        with open("command_log.txt", "a") as f:
            f.write(f"{command}\n")

        if "turn on my pc" in command:
            wake_pc()
        elif "weather" in command:
            city = input("City: ")  # Fallback to text input
            get_weather(city)
        elif "schedule" in command:
            time_str = input("Time (HH:MM): ")
            task = input("Task: ")
            add_event(time_str, task)
        elif "remember" in command or "recall" in command:
            handle_memory(command)
        elif "quit" in command:
            speak("Shutting down. Stay legendary.")
            scheduler.shutdown()
            executor.shutdown()
            exit()
        else:
            store_memory(command, "Processed.")
            speak(random.choice(jarvis_quips))
    except Exception as e:
        logging.error(f"Command Processing Error: {e}")
        speak("Sorry, I couldn’t process that command.")

# Main Function
def grokvis_run():
    """Run the main GROK-VIS loop with wake word detection."""
    global model
    try:
        # Load or train the voice model
        if model is None:
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
                speak("Voice model trained. I’ll only listen to you now!")

        # Start Flask in a separate thread
        threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}, daemon=True).start()
        speak("Dashboard running at http://localhost:5000")

        # Start wake word listener
        wake_word_listener()
    except Exception as e:
        logging.error(f"Main Loop Error: {e}")
        speak("Sorry, something went wrong with the main loop.")

if __name__ == "__main__":
    grokvis_run()
