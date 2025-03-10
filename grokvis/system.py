"""
System control functionality for GrokVIS.
Handles persona switching, volume control, sleep mode, and updates.
"""
import logging
import os
import time
import subprocess
import threading
import requests
import json
from datetime import datetime, timedelta

# Import from core module
from grokvis.speech import speak
from grokvis.core import persona, wake_word_handle

# Global variables
sleep_until = None
volume_level = 50  # Default volume level (0-100)

def switch_persona(new_persona):
    """Switch to a different assistant persona."""
    try:
        # Check if the persona exists
        if new_persona.lower() not in ["alfred", "beatrice"]:
            speak(f"Sorry, I don't have a persona named {new_persona}.")
            return False
            
        # Save the new persona choice
        with open('persona_config.txt', 'w') as f:
            f.write(new_persona.capitalize())
            
        speak(f"I'll switch to {new_persona} persona after restart.")
        speak("Please restart me to complete the switch.")
        return True
    except Exception as e:
        logging.error(f"Switch Persona Error: {e}")
        speak("Sorry, I had trouble switching personas.")
        return False

def adjust_volume(direction):
    """Adjust the system volume up or down."""
    global volume_level
    try:
        # Determine the direction
        if direction.lower() in ["up", "increase", "higher", "louder"]:
            # Increase volume by 10%
            volume_level = min(100, volume_level + 10)
            direction_text = "up"
        elif direction.lower() in ["down", "decrease", "lower", "quieter"]:
            # Decrease volume by 10%
            volume_level = max(0, volume_level - 10)
            direction_text = "down"
        else:
            speak("Please specify 'up' or 'down' for volume adjustment.")
            return
            
        # In a real implementation, this would use platform-specific commands
        # For Windows: nircmd.exe setvolume 0 65535 65535
        # For macOS: osascript -e "set volume output volume 50"
        # For Linux: amixer -D pulse sset Master 50%
        
        # For demonstration, we'll just update our internal volume level
        speak(f"Volume adjusted {direction_text} to {volume_level}%.")
        
        # Simulate the volume change by adjusting TTS volume in future versions
    except Exception as e:
        logging.error(f"Volume Adjustment Error: {e}")
        speak("Sorry, I had trouble adjusting the volume.")

def sleep_mode(duration_str):
    """Temporarily disable wake word detection for a specified time period."""
    global sleep_until
    try:
        # Parse the duration string (e.g., "5 minutes", "1 hour")
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
            
        if duration_seconds == 0:
            # If no specific time units found, try to parse as a number of minutes
            try:
                minutes = int(duration_str.split()[0])
                duration_seconds = minutes * 60
            except:
                speak("I couldn't understand the sleep duration. Please specify like '5 minutes' or '1 hour'.")
                return
                
        # Calculate wake time
        sleep_until = datetime.now() + timedelta(seconds=duration_seconds)
        
        # Format the duration for speech
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        duration_speech = ""
        if hours > 0:
            duration_speech += f"{hours} hour{'s' if hours > 1 else ''} "
        if minutes > 0:
            duration_speech += f"{minutes} minute{'s' if minutes > 1 else ''} "
            
        speak(f"Going to sleep for {duration_speech.strip()}. I won't respond to wake words until then.")
        
        # Start a thread to wake up after the specified duration
        threading.Thread(target=wake_up_after_sleep, args=[duration_seconds], daemon=True).start()
    except Exception as e:
        logging.error(f"Sleep Mode Error: {e}")
        speak("Sorry, I had trouble entering sleep mode.")

def wake_up_after_sleep(duration_seconds):
    """Wake up after the specified sleep duration."""
    try:
        time.sleep(duration_seconds)
        global sleep_until
        sleep_until = None
        speak("I'm awake and listening again.")
    except Exception as e:
        logging.error(f"Wake Up Error: {e}")
        # Reset sleep_until in case of error
        sleep_until = None

def is_sleeping():
    """Check if the system is currently in sleep mode."""
    if sleep_until is None:
        return False
    return datetime.now() < sleep_until

def check_for_updates():
    """Check for and install updates to GrokVIS."""
    try:
        # In a real implementation, this would check a GitHub repository or other source
        # For demonstration, we'll simulate an update check
        
        speak("Checking for updates...")
        
        # Simulate a network request
        time.sleep(2)
        
        # Randomly determine if an update is available (for demonstration)
        import random
        update_available = random.choice([True, False])
        
        if update_available:
            speak("An update is available. Would you like me to install it now?")
            # In a real implementation, this would wait for user confirmation
            # and then perform the update
            
            # For demonstration, we'll just simulate the update process
            speak("Installing update. This may take a few minutes...")
            time.sleep(3)
            speak("Update installed successfully. Please restart me to apply the changes.")
        else:
            speak("You're already running the latest version of GrokVIS.")
    except Exception as e:
        logging.error(f"Update Check Error: {e}")
        speak("Sorry, I had trouble checking for updates.")