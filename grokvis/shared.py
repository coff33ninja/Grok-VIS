"""
Shared components and variables for GrokVIS.
Contains global variables that need to be accessed across multiple modules.
"""
import joblib
import pvporcupine
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# Global variables
model = None
wake_word_handle = None
persona = "Default"
scheduler = BackgroundScheduler()
scheduler.start()

# Personality quips
alfred_quips = [
    "At your service, sir. How else may I assist?",
    "Task complete. Shall I prepare anything else?",
    "Consider it done. I'm here whenever you need me.",
    "As you wish. Your wish is my command.",
    "Executed with precision. What's next on the agenda?"
]

beatrice_quips = [
    "All done with elegance. What else can I help with?",
    "Task completed gracefully. Anything else?",
    "Consider it handled. I'm here for whatever you need next.",
    "Done with a touch of class. What would you like now?",
    "Finished with finesse. How else may I assist you today?"
]

jarvis_quips = [


    "At your service, sir. How else may I assist?",
    "Task complete. Shall I prepare anything else?",
    "Consider it done. I'm here whenever you need me.",
    "As you wish. Your wish is my command.",
    "Executed with precision. What's next on the agenda?"
]
