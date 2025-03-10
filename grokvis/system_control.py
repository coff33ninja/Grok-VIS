"""
System control functionality for GrokVIS.
Handles application launching, file operations, and system commands.
"""
import logging
import os
import platform
import subprocess
import psutil
import time
import json
from pathlib import Path

# Import from core module
from grokvis.speech import speak

# Common application paths by platform
APP_PATHS = {
    "windows": {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
        "notepad": r"C:\Windows\System32\notepad.exe",
        "calculator": r"C:\Windows\System32\calc.exe",
        "spotify": r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
        "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    },
    "macos": {
        "chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "firefox": "/Applications/Firefox.app/Contents/MacOS/firefox",
        "safari": "/Applications/Safari.app/Contents/MacOS/Safari",
        "word": "/Applications/Microsoft Word.app/Contents/MacOS/Microsoft Word",
        "excel": "/Applications/Microsoft Excel.app/Contents/MacOS/Microsoft Excel",
        "powerpoint": "/Applications/Microsoft PowerPoint.app/Contents/MacOS/Microsoft PowerPoint",
        "notes": "/Applications/Notes.app/Contents/MacOS/Notes",
        "calculator": "/Applications/Calculator.app/Contents/MacOS/Calculator",
        "spotify": "/Applications/Spotify.app/Contents/MacOS/Spotify",
        "vscode": "/Applications/Visual Studio Code.app/Contents/MacOS/Electron",
    },
    "linux": {
        "chrome": "google-chrome",
        "firefox": "firefox",
        "word": "libreoffice --writer",
        "excel": "libreoffice --calc",
        "powerpoint": "libreoffice --impress",
        "notepad": "gedit",
        "calculator": "gnome-calculator",
        "spotify": "spotify",
        "vscode": "code",
    }
}

# User-defined application shortcuts
USER_APPS_FILE = "user_apps.json"
user_apps = {}

def load_user_apps():
    """Load user-defined application shortcuts from file."""
    global user_apps
    try:
        if os.path.exists(USER_APPS_FILE):
            with open(USER_APPS_FILE, 'r') as f:
                user_apps = json.load(f)
    except Exception as e:
        logging.error(f"Error loading user apps: {e}")
        user_apps = {}

def save_user_apps():
    """Save user-defined application shortcuts to file."""
    try:
        with open(USER_APPS_FILE, 'w') as f:
            json.dump(user_apps, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving user apps: {e}")

def get_platform():
    """Get the current operating system platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "linux"

def launch_application(app_name):
    """Launch an application by name."""
    try:
        # Normalize app name
        app_name = app_name.lower().strip()
        
        # Get current platform
        current_platform = get_platform()
        
        # Check if it's a user-defined app
        if app_name in user_apps:
            app_path = user_apps[app_name]
        # Check if it's a known app
        elif app_name in APP_PATHS[current_platform]:
            app_path = APP_PATHS[current_platform][app_name]
            # Replace %USERNAME% with actual username on Windows
            if current_platform == "windows":
                app_path = app_path.replace("%USERNAME%", os.getenv("USERNAME"))
        else:
            speak(f"I don't know how to open {app_name}. Would you like to set up a shortcut for it?")
            return False
        
        # Launch the application
        if current_platform == "windows":
            subprocess.Popen([app_path])
        elif current_platform == "macos":
            subprocess.Popen(["open", app_path])
        else:  # Linux
            subprocess.Popen([app_path], shell=True)
            
        speak(f"Launching {app_name}")
        return True
    except Exception as e:
        logging.error(f"Error launching application {app_name}: {e}")
        speak(f"Sorry, I couldn't launch {app_name}.")
        return False

def close_application(app_name):
    """Close an application by name."""
    try:
        # Normalize app name
        app_name = app_name.lower().strip()
        
        # Map of common app names to process names
        process_map = {
            "chrome": ["chrome", "googlechrome"],
            "firefox": ["firefox", "mozilla firefox"],
            "edge": ["msedge", "microsoft edge"],
            "word": ["winword", "microsoft word"],
            "excel": ["excel", "microsoft excel"],
            "powerpoint": ["powerpnt", "microsoft powerpoint"],
            "notepad": ["notepad"],
            "calculator": ["calc", "calculator"],
            "spotify": ["spotify"],
            "vscode": ["code", "visual studio code"],
        }
        
        # Get process names to look for
        process_names = process_map.get(app_name, [app_name])
        
        # Find and terminate matching processes
        found = False
        for proc in psutil.process_iter(['pid', 'name']):
            proc_name = proc.info['name'].lower()
            if any(p in proc_name for p in process_names):
                proc.terminate()
                found = True
                
        if found:
            speak(f"Closed {app_name}")
            return True
        else:
            speak(f"I couldn't find {app_name} running.")
            return False
    except Exception as e:
        logging.error(f"Error closing application {app_name}: {e}")
        speak(f"Sorry, I couldn't close {app_name}.")
        return False

def take_screenshot():
    """Take a screenshot and save it to the desktop."""
    try:
        from PIL import ImageGrab
        import datetime
        
        # Create filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = os.path.join(desktop, f"screenshot_{timestamp}.png")
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        
        speak(f"Screenshot saved to your desktop")
        return True
    except Exception as e:
        logging.error(f"Error taking screenshot: {e}")
        speak("Sorry, I couldn't take a screenshot.")
        return False

def lock_computer():
    """Lock the computer."""
    try:
        current_platform = get_platform()
        
        if current_platform == "windows":
            subprocess.call('rundll32.exe user32.dll,LockWorkStation')
        elif current_platform == "macos":
            subprocess.call('pmset displaysleepnow', shell=True)
        else:  # Linux
            subprocess.call('gnome-screensaver-command --lock', shell=True)
            
        speak("Locking your computer")
        return True
    except Exception as e:
        logging.error(f"Error locking computer: {e}")
        speak("Sorry, I couldn't lock your computer.")
        return False

def shutdown_computer(delay=0):
    """Shutdown the computer with optional delay in minutes."""
    try:
        current_platform = get_platform()
        
        if delay > 0:
            speak(f"Scheduling shutdown in {delay} minutes")
        else:
            speak("Shutting down your computer")
            
        if current_platform == "windows":
            if delay > 0:
                subprocess.call(f'shutdown /s /t {delay * 60}', shell=True)
            else:
                subprocess.call('shutdown /s /t 0', shell=True)
        elif current_platform == "macos":
            if delay > 0:
                subprocess.call(f'sudo shutdown -h +{delay}', shell=True)
            else:
                subprocess.call('sudo shutdown -h now', shell=True)
        else:  # Linux
            if delay > 0:
                subprocess.call(f'sudo shutdown -h +{delay}', shell=True)
            else:
                subprocess.call('sudo shutdown -h now', shell=True)
                
        return True
    except Exception as e:
        logging.error(f"Error shutting down computer: {e}")
        speak("Sorry, I couldn't shut down your computer.")
        return False

def restart_computer():
    """Restart the computer."""
    try:
        current_platform = get_platform()
        
        speak("Restarting your computer")
            
        if current_platform == "windows":
            subprocess.call('shutdown /r /t 0', shell=True)
        elif current_platform == "macos":
            subprocess.call('sudo shutdown -r now', shell=True)
        else:  # Linux
            subprocess.call('sudo shutdown -r now', shell=True)
                
        return True
    except Exception as e:
        logging.error(f"Error restarting computer: {e}")
        speak("Sorry, I couldn't restart your computer.")
        return False

def get_system_status():
    """Get system status information."""
    try:
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = memory.used / (1024 * 1024 * 1024)  # Convert to GB
        memory_total = memory.total / (1024 * 1024 * 1024)  # Convert to GB
        
        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used = disk.used / (1024 * 1024 * 1024)  # Convert to GB
        disk_total = disk.total / (1024 * 1024 * 1024)  # Convert to GB
        
        # Format the response
        status = (
            f"CPU usage is at {cpu_percent:.1f}%. "
            f"Memory usage is at {memory_percent:.1f}%, using {memory_used:.1f} GB out of {memory_total:.1f} GB. "
            f"Disk usage is at {disk_percent:.1f}%, using {disk_used:.1f} GB out of {disk_total:.1f} GB."
        )
        
        speak(status)
        return True
    except Exception as e:
        logging.error(f"Error getting system status: {e}")
        speak("Sorry, I couldn't get your system status.")
        return False

def find_files(query, location=None):
    """Find files matching a query."""
    try:
        if location is None:
            # Default to user's home directory
            location = os.path.expanduser("~")
            
        speak(f"Searching for {query} in {location}")
        
        # Get list of files matching query
        results = []
        for root, dirs, files in os.walk(location):
            for file in files:
                if query.lower() in file.lower():
                    results.append(os.path.join(root, file))
                    
        # Report results
        if results:
            speak(f"I found {len(results)} files matching '{query}'.")
            for i, result in enumerate(results[:5]):  # Limit to first 5 results
                speak(f"Result {i+1}: {os.path.basename(result)}")
                
            if len(results) > 5:
                speak(f"And {len(results) - 5} more results.")
                
            return results
        else:
            speak(f"I couldn't find any files matching '{query}'.")
            return []
    except Exception as e:
        logging.error(f"Error finding files: {e}")
        speak("Sorry, I had trouble searching for files.")
        return []

def open_file(filepath):
    """Open a file with the default application."""
    try:
        current_platform = get_platform()
        
        if current_platform == "windows":
            os.startfile(filepath)
        elif current_platform == "macos":
            subprocess.call(['open', filepath])
        else:  # Linux
            subprocess.call(['xdg-open', filepath])
            
        speak(f"Opening {os.path.basename(filepath)}")
        return True
    except Exception as e:
        logging.error(f"Error opening file: {e}")
        speak("Sorry, I couldn't open that file.")
        return False

def create_folder(folder_name, location=None):
    """Create a new folder."""
    try:
        if location is None:
            # Default to user's home directory
            location = os.path.expanduser("~")
            
        # Create full path
        folder_path = os.path.join(location, folder_name)
        
        # Create folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            speak(f"Created folder {folder_name} in {location}")
        else:
            speak(f"Folder {folder_name} already exists in {location}")
            
        return folder_path
    except Exception as e:
        logging.error(f"Error creating folder: {e}")
        speak(f"Sorry, I couldn't create the folder {folder_name}.")
        return None

def add_app_shortcut(app_name, app_path):
    """Add a user-defined application shortcut."""
    try:
        # Normalize app name
        app_name = app_name.lower().strip()
        
        # Check if path exists
        if not os.path.exists(app_path):
            speak(f"I couldn't find an application at {app_path}.")
            return False
            
        # Add to user apps
        user_apps[app_name] = app_path
        save_user_apps()
        
        speak(f"Added shortcut for {app_name}.")
        return True
    except Exception as e:
        logging.error(f"Error adding app shortcut: {e}")
        speak(f"Sorry, I couldn't add a shortcut for {app_name}.")
        return False

# Initialize module
load_user_apps()