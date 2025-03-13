"""
Scheduling functionality for GrokVIS.
Handles scheduling events and reminders.
"""
import datetime
import logging

# Import from shared module
from grokvis.shared import scheduler
from grokvis.speech import speak
from grokvis.memory import store_memory

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
        speak("Sorry, I couldn't schedule that event.")

def list_events():
    """List all scheduled events."""
    try:
        jobs = scheduler.get_jobs()
        if not jobs:
            speak("You have no scheduled events.")
            return

        speak("Here are your scheduled events:")
        for job in jobs:
            run_time = job.next_run_time.strftime("%Y-%m-%d %H:%M")
            task = job.args[0] if job.args else "Unknown task"
            speak(f"{run_time}: {task}")
    except Exception as e:
        logging.error(f"List Events Error: {e}")
        speak("Sorry, I couldn't list your events.")

def remove_event(task_keyword):
    """Remove an event containing the given keyword."""
    try:
        jobs = scheduler.get_jobs()
        removed = False

        for job in jobs:
            if job.args and task_keyword.lower() in job.args[0].lower():
                job_id = job.id
                scheduler.remove_job(j极Id)
                speak(f"Removed event: {job.args[0]}")
                removed = True

        if not removed:
            speak(f"No events found containing '{task_keyword}'.")
    except Exception as e:
        logging.error(f"Remove Event Error: {e}")
        speak("Sorry, I couldn't remove that event.")
