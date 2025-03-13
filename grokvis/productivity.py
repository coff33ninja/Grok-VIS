"""
Productivity functionality for GrokVIS.
Handles timers, stopwatches, shopping lists, notes, and location-based reminders.
"""
import logging
import time
import json
import os
import threading
import sqlite3
from datetime import datetime, timedelta

# Import from core module
from grokvis.speech import speak
from grokvis.shared import scheduler

# Global variables
timers = {}
stopwatches = {}
shopping_lists = {}
notes = []

def start_timer(duration_str):
    """Start a countdown timer."""
    try:
        # Parse the duration string (e.g., "5 minutes", "1 hour 30 minutes")
        duration_seconds = 0

        if "hour" in duration_str:
            hours = int(duration_str.split("hour")[0].strip().split()[-1])
            duration_seconds += hours * 3600

        if "minute" in duration_str:
            if "hour" in duration_str:
                minutes_part = duration_str.split("hour")[1]
            else:
                minutes_part = duration_str
            minutes = int(minutes_part.split("minute")[0].strip().split()[-1])
            duration_seconds += minutes * 60

        if "second" in duration_str:
            if "minute" in duration_str:
                seconds_part = duration_str.split("minute")[1]
            elif "hour" in duration_str:
                seconds_part = duration_str.split("hour")[1]
            else:
                seconds_part = duration_str
            seconds = int(seconds_part.split("second")[0].strip().split()[-1])
            duration_seconds += seconds

        if duration_seconds == 0:
            # If no specific time units found, try to parse as a number of minutes
            try:
                minutes = int(duration_str.split()[0])
                duration_seconds = minutes * 60
            except:
                speak("I couldn't understand the timer duration. Please specify like '5 minutes' or '1 hour 30 minutes'.")
                return

        # Create a unique ID for this timer
        timer_id = f"timer_{int(time.time())}"
        end_time = datetime.now() + timedelta(seconds=duration_seconds)

        # Store the timer
        timers[timer_id] = {
            "end_time": end_time,
            "duration": duration_seconds,
            "remaining": duration_seconds
        }

        # Format the duration for speech
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        duration_speech = ""
        if hours > 0:
            duration_speech += f"{hours} hour{'s' if hours > 1 else ''} "
        if minutes > 0:
            duration_speech += f"{minutes} minute{'s' if minutes > 1 else ''} "
        if seconds > 0 and hours == 0:  # Only mention seconds if less than an hour
            duration_speech += f"{seconds} second{'s' if seconds > 1 else ''}"

        speak(f"Timer set for {duration_speech.strip()}.")

        # Schedule the timer to go off
        scheduler.add_job(
            timer_complete,
            'date',
            run_date=end_time,
            args=[timer_id],
            id=timer_id
        )

        return timer_id
    except Exception as e:
        logging.error(f"Timer Error: {e}")
        speak("Sorry, I had trouble setting that timer.")
        return None

def timer_complete(timer_id):
    """Called when a timer completes."""
    try:
        if timer_id in timers:
            speak("Timer complete!")
            del timers[timer_id]
    except Exception as e:
        logging.error(f"Timer Complete Error: {e}")

def start_stopwatch():
    """Start a stopwatch."""
    try:
        # Create a unique ID for this stopwatch
        stopwatch_id = f"stopwatch_{int(time.time())}"

        # Store the stopwatch
        stopwatches[stopwatch_id] = {
            "start_time": datetime.now(),
            "running": True
        }

        speak("Stopwatch started.")
        return stopwatch_id
    except Exception as e:
        logging.error(f"Stopwatch Error: {e}")
        speak("Sorry, I had trouble starting the stopwatch.")
        return None

def stop_stopwatch(stopwatch_id=None):
    """Stop a running stopwatch and report the elapsed time."""
    try:
        # If no ID provided, stop the most recent stopwatch
        if stopwatch_id is None and stopwatches:
            stopwatch_id = list(stopwatches.keys())[-1]

        if stopwatch_id in stopwatches:
            stopwatch = stopwatches[stopwatch_id]

            if stopwatch["running"]:
                elapsed = datetime.now() - stopwatch["start_time"]
                stopwatch["running"] = False
                stopwatch["elapsed"] = elapsed

                # Format the elapsed time for speech
                total_seconds = int(elapsed.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                elapsed_speech = ""
                if hours > 0:
                    elapsed_speech += f"{hours} hour{'s' if hours > 1 else ''} "
                if minutes > 0:
                    elapsed_speech += f"{minutes} minute{'s' if minutes > 1 else ''} "
                elapsed_speech += f"{seconds} second{'s' if seconds > 1 else ''}"

                speak(f"Stopwatch stopped. Elapsed time: {elapsed_speech.strip()}.")
                return elapsed
            else:
                speak("This stopwatch is already stopped.")
                return stopwatch["elapsed"]
        else:
            speak("No active stopwatch found.")
            return None
    except Exception as e:
        logging.error(f"Stop Stopwatch Error: {e}")
        speak("Sorry, I had trouble stopping the stopwatch.")
        return None

def add_to_shopping_list(item, list_name="default"):
    """Add an item to a shopping list."""
    try:
        # Initialize the list if it doesn't exist
        if list_name not in shopping_lists:
            shopping_lists[list_name] = []

        # Add the item to the list
        shopping_lists[list_name].append({
            "item": item,
            "added": datetime.now().isoformat(),
            "completed": False
        })

        # Save the shopping lists to a file
        save_shopping_lists()

        speak(f"Added {item} to your {list_name} shopping list.")
    except Exception as e:
        logging.error(f"Shopping List Error: {e}")
        speak(f"Sorry, I had trouble adding {item} to your shopping list.")

def show_shopping_list(list_name="default"):
    """Show the contents of a shopping list."""
    try:
        if list_name not in shopping_lists or not shopping_lists[list_name]:
            speak(f"Your {list_name} shopping list is empty.")
            return

        items = [item["item"] for item in shopping_lists[list_name] if not item["completed"]]

        if not items:
            speak(f"All items in your {list_name} shopping list are marked as completed.")
            return

        speak(f"Here's your {list_name} shopping list:")
        for i, item in enumerate(items):
            speak(f"{i+1}. {item}")
    except Exception as e:
        logging.error(f"Show Shopping List Error: {e}")
        speak("Sorry, I had trouble showing your shopping list.")

def save_shopping_lists():
    """Save shopping lists to a file."""
    try:
        with open("shopping_lists.json", "w") as f:
            json.dump(shopping_lists, f)
    except Exception as e:
        logging.error(f"Save Shopping Lists Error: {e}")

def load_shopping_lists():
    """Load shopping lists from a file."""
    global shopping_lists
    try:
        if os.path.exists("shopping_lists.json"):
            with open("shopping_lists.json", "r") as f:
                shopping_lists = json.load(f)
    except Exception as e:
        logging.error(f"Load Shopping Lists Error: {e}")
        shopping_lists = {}

def take_note(content):
    """Save a note."""
    try:
        # Create a new note
        note = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "id": len(notes) + 1
        }

        # Add it to the notes list
        notes.append(note)

        # Save the notes to a file
        save_notes()

        speak(f"Note saved: {content}")
    except Exception as e:
        logging.error(f"Take Note Error: {e}")
        speak("Sorry, I had trouble saving your note.")

def show_notes(count=5):
    """Show recent notes."""
    try:
        if not notes:
            speak("You don't have any notes yet.")
            return

        recent_notes = sorted(notes, key=lambda x: x["timestamp"], reverse=True)[:count]

        speak(f"Here are your {len(recent_notes)} most recent notes:")
        for i, note in enumerate(recent_notes):
            timestamp = datetime.fromisoformat(note["timestamp"]).strftime("%B %d, %Y at %I:%M %p")
            speak(f"{i+1}. On {timestamp}: {note['content']}")
    except Exception as e:
        logging.error(f"Show Notes Error: {e}")
        speak("Sorry, I had trouble showing your notes.")

def save_notes():
    """Save notes to a file."""
    try:
        with open("notes.json", "w") as f:
            json.dump(notes, f)
    except Exception as e:
        logging.error(f"Save Notes Error: {e}")

def load_notes():
    """Load notes from a file."""
    global notes
    try:
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as f:
                notes = json.load(f)
    except Exception as e:
        logging.error(f"Load Notes Error: {e}")
        notes = []

def location_reminder(task, location):
    """Set a reminder for when you reach a specific location."""
    try:
        # In a real implementation, this would use geofencing or location services
        # For demonstration, we'll just save it to a database

        conn = sqlite3.connect("location_reminders.db")
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS location_reminders (
            id INTEGER PRIMARY KEY,
            task TEXT,
            location TEXT,
            created_at TIMESTAMP,
            completed INTEGER
        )
        ''')

        # Insert the reminder
        cursor.execute(
            "INSERT INTO location_reminders (task, location, created_at, completed) VALUES (?, ?, ?, ?)",
            (task, location, datetime.now().isoformat(), 0)
        )

        conn.commit()
        conn.close()

        speak(f"I'll remind you to {task} when you get to {location}.")
    except Exception as e:
        logging.error(f"Location Reminder Error: {e}")
        speak("Sorry, I had trouble setting that location reminder.")

# Initialize the productivity module
def initialize():
    """Initialize the productivity module."""
    load_shopping_lists()
    load_notes()
