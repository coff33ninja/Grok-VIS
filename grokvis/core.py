"""Core functionality for the GrokVIS assistant.
Contains initialization, model loading, and main execution loop.
"""

import logging
import os
import threading
import sqlite3
import speech_recognition as sr
import pynvml
import spacy
import numpy as np  # Not currently used but kept for potential future use
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


# Delayed imports to avoid circular dependencies
def _import_grokvis_modules():
    from grokvis.speech import (
        train_voice_model,
        wake_word_listener,
        setup_personality,
        speak,
    )
    from grokvis.web import app
    from grokvis.hardware_manager import get_hardware_manager
    from grokvis.shared import persona, jarvis_quips, alfred_quips, beatrice_quips

    return (
        train_voice_model,
        wake_word_listener,
        setup_personality,
        speak,
        app,
        get_hardware_manager,
        persona,
    )


# Global variables
memory_model = None
nlp = None
conn = None
executor = None
scheduler = None
persona = "Default"  # Default persona


def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        filename="grokvis_errors.log",
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",  # Ensure UTF-8 encoding for Windows compatibility
    )


def initialize_components():
    """Initialize core components of GrokVIS."""
    global memory_model, nlp, conn, executor, scheduler

    # Load core components
    try:
        memory_model = SentenceTransformer("all-MiniLM-L6-v2")
        nlp = spacy.load("en_core_web_sm")
        pynvml.nvmlInit()
        conn = sqlite3.connect("grokvis_memory.db")
        executor = ThreadPoolExecutor(max_workers=2)

        # APScheduler setup
        jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.db")}
        scheduler = BackgroundScheduler(jobstores=jobstores)
        scheduler.start()
        logging.info("Core components initialized successfully")
    except Exception as e:
        logging.error(f"Initialization error: {e}")
        raise


def greet_user():
    """Greet the user and ask for their desired persona."""
    # Delayed import of speak
    _, _, _, speak, _, _, _ = _import_grokvis_modules()

    speak(
        "Hello! What persona would you like to use? You can choose Alfred, Beatrice, or any other available persona."
    )

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your response...")
        audio = recognizer.listen(source)

    try:
        response = recognizer.recognize_google(audio)
        print(f"You said: {response}")

        global persona
        if "alfred" in response.lower():
            persona = "Alfred"
            speak("You have chosen Alfred.")
        elif "beatrice" in response.lower():
            persona = "Beatrice"
            speak("You have chosen Beatrice.")
        else:
            persona = "Default"
            speak("You have chosen a default persona.")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said.")
        persona = "Default"
    except sr.RequestError as e:
        speak(f"Could not request results: {e}")
        persona = "Default"


def grokvis_run():
    """Run the main GROK-VIS loop with wake word detection."""
    setup_logging()
    initialize_components()

    # Import modules after initialization to avoid circular imports
    train_voice_model, wake_word_listener, _, speak, app, get_hardware_manager, _ = (
        _import_grokvis_modules()
    )

    try:
        # Greet user
        greet_user()

        # Persona-specific greeting
        if persona == "Alfred":
            speak("Greetings, I'm Alfred, your loyal assistant.")
        elif persona == "Beatrice":
            speak("Hello, I'm Beatrice, here to assist you with grace.")
        else:
            speak("Hello, I'm your assistant, ready to help.")

        # Initialize hardware manager
        hw_manager = get_hardware_manager()

        # Train voice model
        train_voice_model()

        # Start Flask app in a separate thread
        threading.Thread(
            target=app.run, kwargs={"host": "0.0.0.0", "port": 5000}, daemon=True
        ).start()
        speak("Dashboard running at http://localhost:5000")

        # Start wake word listener
        wake_word_listener()
    except Exception as e:
        logging.error(f"Main Loop Error: {e}")
        speak("Sorry, something went wrong with the main loop.")
    finally:
        # Cleanup
        if executor:
            executor.shutdown()
        if scheduler:
            scheduler.shutdown()
        if conn:
            conn.close()
        pynvml.nvmlShutdown()


if __name__ == "__main__":
    grokvis_run()
