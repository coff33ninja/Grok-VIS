"""Core functionality for the GrokVIS assistant.
Contains initialization, model loading, and main execution loop.
"""
import logging
import os
import datetime
import random
import joblib
import threading
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer
import spacy
import pynvml
import sqlite3
import speech_recognition as sr
from grokvis.speech import train_voice_model, wake_word_listener, setup_personality, speak
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from grokvis.web import app
from grokvis.shared import model, wake_word_handle, persona, jarvis_quips, alfred_quips, beatrice_quips

# Global variables
memory_model = None
nlp = None
conn = None
executor = None

# Initialize logging
def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(filename='grokvis_errors.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables and initialization
def initialize_components():
    """Initialize core components of GrokVIS."""
    global memory_model, nlp, conn, executor, scheduler, persona

    # Initialize core components
    memory_model = SentenceTransformer('all-MiniLM-L6-v2')
    nlp = spacy.load("en_core_web_sm")
    pynvml.nvmlInit()
    conn = sqlite3.connect("grokvis_memory.db")
    executor = ThreadPoolExecutor(max_workers=2)  # Thread pool for async tasks

    # APScheduler setup
    from grokvis.shared import scheduler
    jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')}
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler(jobstores=jobstores)
    scheduler.start()

def greet_user():
    """Greet the user and ask for their desired persona."""
    speak("Hello! What persona would you like to use? You can choose Alfred, Beatrice, or any other available persona.")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for your response...")
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        response = recognizer.recognize_google(audio)
        print(f"You said: {response}")

        # Set persona based on recognized response
        global persona
        if "Alfred" in response:
            persona = "Alfred"
            speak("You have chosen Alfred.")
        elif "Beatrice" in response:
            persona = "Beatrice"
            speak("You have chosen Beatrice.")
        else:
            persona = "Default"  # Fallback persona
            speak("You have chosen a default persona.")

    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said.")
        persona = "Default"  # Fallback persona
    except sr.RequestError as e:
        speak("Could not request results from the speech recognition service.")
        persona = "Default"  # Fallback persona

# Main Function
def grokvis_run():
    """Run the main GROK-VIS loop with wake word detection."""
    try:
        # Setup logging
        setup_logging()

        # Initialize components
        initialize_components()

        # Greet the user and ask for persona
        greet_user()

        # Now that TTS is initialized, we can properly greet the user
        if persona == "Alfred":
            speak("Greetings, I'm Alfred, your loyal assistant.")
        elif persona == "Beatrice":
            speak("Hello, I'm Beatrice, here to assist you with grace.")

        # Load or train the voice model
        train_voice_model()

        # Start Flask in a separate thread
        threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}, daemon=True).start()
        speak("Dashboard running at http://localhost:5000")

        # Start wake word listener
        wake_word_listener()
    except Exception as e:
        logging.error(f"Main Loop Error: {e}")
        speak("Sorry, something went wrong with the main loop.")
