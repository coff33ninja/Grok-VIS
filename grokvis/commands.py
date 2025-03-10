"""
Command processing functionality for GrokVIS.
Handles interpreting and executing user commands.
"""
import logging
import random

# Import from other modules
from grokvis.core import jarvis_quips, scheduler, executor
from grokvis.speech import speak
from grokvis.memory import store_memory, handle_memory
from grokvis.scheduler import add_event, list_events, remove_event
from grokvis.home_automation import wake_pc, control_device, check_device_status
from grokvis.weather import get_weather, get_forecast

def process_command(command):
    """Process the spoken command."""
    try:
        if not command:
            return

        # Log command for future LLM training
        with open("command_log.txt", "a") as f:
            f.write(f"{command}\n")

        # Home automation commands
        if "turn on my pc" in command or "wake my pc" in command:
            wake_pc()
        elif "turn on" in command or "turn off" in command or "dim" in command:
            action = "turn on" if "turn on" in command else "turn off" if "turn off" in command else "dim"
            # Extract the device name from the command
            device = command.split(action)[1].strip()
            control_device(device, action.split()[0])
        elif "check" in command and ("status" in command or "online" in command):
            # Extract the device name from the command
            device = command.split("check")[1].replace("status", "").replace("online", "").strip()
            check_device_status(device)
            
        # Weather commands
        elif "weather" in command and "forecast" in command:
            city = command.split("in")[-1].strip() if "in" in command else input("City: ")
            days = 5  # Default to 5-day forecast
            get_forecast(city, days)
        elif "weather" in command:
            city = command.split("in")[-1].strip() if "in" in command else input("City: ")
            get_weather(city)
            
        # Scheduling commands
        elif "schedule" in command or "remind me" in command:
            if "list" in command or "show" in command:
                list_events()
            elif "remove" in command or "delete" in command or "cancel" in command:
                task_keyword = command.split("remove")[-1].strip() if "remove" in command else \
                               command.split("delete")[-1].strip() if "delete" in command else \
                               command.split("cancel")[-1].strip()
                remove_event(task_keyword)
            else:
                time_str = input("Time (HH:MM): ")
                task = input("Task: ")
                add_event(time_str, task)
                
        # Memory commands
        elif "remember" in command or "recall" in command or "what did i" in command:
            handle_memory(command)
            
        # System commands
        elif "quit" in command or "exit" in command or "shutdown" in command:
            speak("Shutting down. Stay legendary.")
            scheduler.shutdown()
            executor.shutdown()
            exit()
            
        # Default response
        else:
            store_memory(command, "Processed.")
            speak(random.choice(jarvis_quips))
    except Exception as e:
        logging.error(f"Command Processing Error: {e}")
        speak("Sorry, I couldn't process that command.")