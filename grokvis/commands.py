"""
Command processing functionality for GrokVIS.
Handles interpreting and executing user commands.
"""
import logging
import random
import re

# Import from other modules
from grokvis.core import jarvis_quips, alfred_quips, beatrice_quips, scheduler, executor, persona
from grokvis.speech import speak
from grokvis.memory import store_memory, handle_memory
from grokvis.scheduler import add_event, list_events, remove_event
from grokvis.home_automation import wake_pc, control_device, check_device_status
from grokvis.weather import get_weather, get_forecast

# Import new modules
from grokvis.knowledge import get_wikipedia_summary, get_news_headlines, get_word_definition, translate_text
from grokvis.entertainment import tell_joke, play_music, get_movie_listings, share_random_fact
from grokvis.productivity import start_timer, start_stopwatch, stop_stopwatch, add_to_shopping_list
from grokvis.productivity import show_shopping_list, take_note, show_notes, location_reminder
from grokvis.system import switch_persona, adjust_volume, sleep_mode, check_for_updates, is_sleeping

def process_command(command):
    """Process the spoken command."""
    try:
        if not command:
            return
            
        # Check if system is in sleep mode
        if is_sleeping():
            # Only respond to "wake up" command while sleeping
            if "wake up" in command.lower():
                from grokvis.system import sleep_until
                sleep_until = None
                speak("I'm awake and listening again.")
            return True

        # Log command for future LLM training
        with open("command_log.txt", "a") as f:
            f.write(f"{command}\n")

        # KNOWLEDGE COMMANDS
        if "tell me about" in command:
            topic = command.split("tell me about")[1].strip()
            get_wikipedia_summary(topic)
            
        elif "what's in the news" in command or "news headlines" in command:
            get_news_headlines()
            
        elif "define" in command:
            word = command.split("define")[1].strip()
            get_word_definition(word)
            
        elif "translate" in command and "to" in command:
            # Extract phrase and target language
            phrase = command.split("translate")[1].split("to")[0].strip()
            language = command.split("to")[1].strip()
            translate_text(phrase, language)

        # HOME AUTOMATION COMMANDS
        elif "turn on my pc" in command or "wake my pc" in command:
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
            
        elif "set temperature to" in command:
            # Extract temperature from command
            temp_str = command.split("set temperature to")[1].strip()
            temp = int(re.search(r'\d+', temp_str).group())
            speak(f"Setting temperature to {temp} degrees.")
            # This would connect to a smart thermostat API in a real implementation
            
        elif "set scene" in command:
            # Extract scene name from command
            scene = command.split("set scene")[1].strip()
            speak(f"Setting scene to {scene}.")
            # This would activate a predefined scene in a real implementation
            
        elif "is my" in command and "on" in command:
            # Extract device from command
            device = command.split("is my")[1].split("on")[0].strip()
            check_device_status(device)
            
        # WEATHER COMMANDS
        elif "weather" in command and "forecast" in command:
            city = command.split("in")[-1].strip() if "in" in command else input("City: ")
            days = 5  # Default to 5-day forecast
            get_forecast(city, days)
            
        elif "weather" in command:
            city = command.split("in")[-1].strip() if "in" in command else input("City: ")
            get_weather(city)
            
        # SCHEDULING COMMANDS
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
                
        elif "remind me to" in command and "when i get" in command.lower():
            # Extract task and location
            task = command.split("remind me to")[1].split("when")[0].strip()
            location = command.split("when i get")[1].strip()
            location_reminder(task, location)
            
        # MEMORY COMMANDS
        elif "remember" in command or "recall" in command or "what did i" in command:
            if "remember this conversation" in command:
                speak("I'll remember our current conversation.")
                # In a real implementation, this would save the entire conversation thread
            elif "forget what I just said" in command:
                speak("I've forgotten your last statement.")
                # In a real implementation, this would remove recent items from memory
            else:
                handle_memory(command)
            
        # ENTERTAINMENT COMMANDS
        elif "tell me a joke" in command or "joke" in command:
            tell_joke()
            
        elif "play some" in command and "music" in command:
            genre = command.split("play some")[1].split("music")[0].strip()
            play_music(genre)
            
        elif "what movies are playing" in command:
            location = "nearby"
            if "in" in command:
                location = command.split("in")[1].strip()
            get_movie_listings(location)
            
        elif "random fact" in command or "give me a fact" in command:
            share_random_fact()
            
        # PRODUCTIVITY COMMANDS
        elif "start a timer for" in command:
            duration = command.split("start a timer for")[1].strip()
            start_timer(duration)
            
        elif "start a stopwatch" in command:
            start_stopwatch()
            
        elif "stop the stopwatch" in command:
            stop_stopwatch()
            
        elif "add" in command and "to my shopping list" in command:
            item = command.split("add")[1].split("to my shopping list")[0].strip()
            add_to_shopping_list(item)
            
        elif "show my shopping list" in command:
            show_shopping_list()
            
        elif "take a note" in command:
            content = command.split("take a note")[1].strip()
            if content.startswith(":"):
                content = content[1:].strip()
            take_note(content)
            
        elif "show my notes" in command:
            show_notes()
            
        # SYSTEM COMMANDS
        elif "switch to" in command and ("alfred" in command.lower() or "beatrice" in command.lower()):
            if "alfred" in command.lower():
                new_persona = "Alfred"
            else:
                new_persona = "Beatrice"
            switch_persona(new_persona)
            
        elif "volume" in command:
            if any(word in command.lower() for word in ["up", "increase", "higher", "louder"]):
                adjust_volume("up")
            elif any(word in command.lower() for word in ["down", "decrease", "lower", "quieter"]):
                adjust_volume("down")
            else:
                speak("Please specify if you want to turn the volume up or down.")
                
        elif "go to sleep for" in command:
            duration = command.split("go to sleep for")[1].strip()
            sleep_mode(duration)
            
        elif "update yourself" in command or "check for updates" in command:
            check_for_updates()
            
        # QUIT COMMAND
        elif "quit" in command or "exit" in command or "shutdown" in command:
            speak("Shutting down. Stay legendary.")
            scheduler.shutdown()
            executor.shutdown()
            return False  # Signal to stop the main loop
            
        # DEFAULT RESPONSE
        else:
            store_memory(command, "Processed.")
            # Use persona-specific quips
            if persona == "Beatrice":
                speak(random.choice(beatrice_quips))
            else:  # Default to Alfred
                speak(random.choice(alfred_quips))
                
        return True  # Continue the main loop
    except Exception as e:
        logging.error(f"Command Processing Error: {e}")
        speak("Sorry, I couldn't process that command.")
        return True  # Continue despite the error