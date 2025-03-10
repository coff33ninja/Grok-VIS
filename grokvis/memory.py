"""
Memory management functionality for GrokVIS.
Handles storing and retrieving memories from the database.
"""
import datetime
import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Import from core module
from grokvis.core import memory_model, conn
from grokvis.speech import speak

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
        speak("Sorry, I couldn't store that memory.")

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
        speak("Sorry, I couldn't recall that memory.")
        return []

def handle_memory(command):
    """Handle memory-related commands."""
    if "remember" in command:
        parts = command.split("remember")[-1].strip()
        store_memory(parts, "Noted.")
        speak(f"Got it, I'll remember: {parts}.")
    elif "what did i" in command or "recall" in command:
        query = command.split("about")[-1].strip() if "about" in command else command
        recalled = recall_memory(query)
        if recalled:
            cmd, resp = recalled[0]
            speak(f"You said: '{cmd}', and I replied: '{resp}'")
        else:
            speak("Memory's a bit fuzzy—nothing matches that.")

def initialize_memory_db():
    """Initialize the memory database if it doesn't exist."""
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            command TEXT,
            response TEXT,
            embedding BLOB
        )
        ''')
        conn.commit()
    except Exception as e:
        logging.error(f"Memory DB Initialization Error: {e}")
        speak("Sorry, I couldn't initialize the memory database.")