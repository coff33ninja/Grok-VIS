# GrokVIS - Voice Interactive System

GrokVIS is a modular voice assistant with memory, scheduling, and home automation capabilities. It features a web dashboard, weather services, and voice recognition with speaker verification.

## Features

- **Voice Recognition**: Listens for wake word "Hey GrokVIS" and processes voice commands
- **Speaker Verification**: Uses voice biometrics to ensure only authorized users can issue commands
- **Personality Selection**: Choose between Alfred (male butler) or Beatrice (female assistant) personas
- **Memory System**: Stores and recalls conversations using semantic search
- **Scheduling**: Sets reminders and manages events
- **Home Automation**: Controls smart devices and supports Wake-on-LAN
- **Weather Services**: Fetches current weather and forecasts
- **Web Dashboard**: Provides a browser-based interface for monitoring and control
- **Knowledge Base**: Fetches information from Wikipedia, news, dictionaries, and translation services
- **Entertainment**: Tells jokes, plays music, shows movie listings, and shares random facts
- **Productivity Tools**: Manages timers, stopwatches, shopping lists, notes, and location-based reminders
- **System Controls**: Adjusts volume, enters sleep mode, and checks for updates
- **Application Control**: Launches and closes applications, takes screenshots, and manages system functions
- **File Management**: Searches for files, creates folders, and opens documents

## Project Structure

The project has been modularized into the following components:

```
grokvis/
├── __init__.py       # Package initialization
├── core.py           # Core functionality and initialization
├── speech.py         # Speech recognition and TTS
├── memory.py         # Memory storage and retrieval
├── scheduler.py      # Event scheduling
├── home_automation.py # Device control
├── weather.py        # Weather services
├── web.py            # Web dashboard
├── commands.py       # Command processing
├── knowledge.py      # Information retrieval and language services
├── entertainment.py  # Fun and entertainment features
├── productivity.py   # Time management and organization tools
├── system.py         # System control and configuration
└── system_control.py # Application and file management
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Grok-VIS.git
cd Grok-VIS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
```

4. Configure API keys:
   - Replace `YOUR_PICOVOICE_ACCESS_KEY` in `speech.py` with your Picovoice key
   - Replace `YOUR_API_KEY` in `weather.py` with your OpenWeatherMap API key
   - Replace `YOUR_PC_MAC` in `home_automation.py` with your PC's MAC address

## Usage

Run the application:
```bash
python main.py
```

The system will:
1. Initialize all components
2. Ask you to choose a persona (Alfred or Beatrice) on first run
3. Train or load your voice model
4. Start the web dashboard at http://localhost:5000
5. Begin listening for the wake word "Hey GrokVIS"

## Voice Commands

### Basic Commands
- **Weather**: "What's the weather in [city]?" or "Give me the forecast for [city]"
- **Scheduling**: "Schedule [task] at [time]", "Show my schedule", "Remove [task]"
- **Memory**: "Remember [information]", "What did I say about [topic]?"
- **Home Automation**: "Turn on/off [device]", "Check if [device] is online"
- **System**: "Quit" or "Shutdown"

### Knowledge Commands
- **Wikipedia**: "Tell me about [topic]" - Get information from Wikipedia
- **News**: "What's in the news today?" - Get latest news headlines
- **Dictionary**: "Define [word]" - Look up word definitions
- **Translation**: "Translate [phrase] to [language]" - Translate text to another language

### Home Automation Commands
- **Temperature**: "Set the temperature to [value] degrees" - Control smart thermostat
- **Scenes**: "Set scene [scene name]" - Activate predefined combinations of device settings
- **Status Check**: "Is my [device] on?" - Check status of specific devices

### Entertainment Commands
- **Jokes**: "Tell me a joke" - Get a random joke
- **Music**: "Play some [genre] music" - Play music by genre
- **Movies**: "What movies are playing nearby?" - Get movie listings
- **Facts**: "Give me a random fact" - Get interesting trivia

### Productivity Commands
- **Timers**: "Start a timer for [time]" - Set countdown timers
- **Stopwatch**: "Start a stopwatch" / "Stop the stopwatch" - Track elapsed time
- **Shopping Lists**: "Add [item] to my shopping list" / "Show my shopping list"
- **Notes**: "Take a note: [content]" / "Show my notes" - Quick note-taking
- **Location Reminders**: "Remind me to [task] when I get to [location]"

### System Commands
- **Persona**: "Switch to [Alfred/Beatrice]" - Change assistant persona
- **Volume**: "Volume up" / "Volume down" - Adjust system volume
- **Sleep Mode**: "Go to sleep for [time period]" - Temporarily disable wake word detection
- **Updates**: "Update yourself" - Check for and install updates
- **Wake Up**: "Wake up" - Exit sleep mode early

### Application Control Commands
- **Launch Apps**: "Open [application]" / "Launch [application]" - Start applications
- **Close Apps**: "Close [application]" - Terminate running applications
- **Screenshots**: "Take a screenshot" - Capture and save screen image
- **System Control**: "Lock my computer" - Lock your workstation
- **Power Management**: "Shutdown computer in [minutes]" / "Restart computer" - Control power state
- **System Info**: "System status" / "How's my computer" - Get CPU, memory, and disk usage

### File Management Commands
- **File Search**: "Find [query] files" - Search for files matching a pattern
- **Folder Creation**: "Create folder [name]" - Create new directories
- **App Shortcuts**: "Add shortcut for [app]" - Create custom application shortcuts

## Web Dashboard

Access the dashboard at http://localhost:5000 to:
- View scheduled tasks
- See recent commands
- Monitor system statistics

## Key Enhancements

### Expanded Voice Commands

- **What's Done**: Added over 20 new voice commands across multiple categories:
  - **Knowledge**: Wikipedia lookups, news headlines, word definitions, translations
  - **Entertainment**: Jokes, music playback, movie listings, random facts
  - **Productivity**: Timers, stopwatches, shopping lists, notes, location reminders
  - **System Controls**: Persona switching, volume control, sleep mode, updates
- **How It Works**: Each command category has its own module with specialized functions
- **Impact**: Transforms GrokVIS from a basic assistant to a comprehensive voice interface

### Personality System

- **What's Done**: Added a personality selection system with two distinct personas:
  - **Alfred**: A male butler-like assistant with a formal, professional tone
  - **Beatrice**: A female assistant with an elegant, warm tone
- **How It Works**: On first run, GrokVIS asks you to choose a persona. Your choice is saved to `persona_config.txt` and used for all future interactions.
- **Impact**: Creates a more personalized experience with voice and language style matching your preference.

### Async Handling

- **What's Done**: Added a ThreadPoolExecutor with 2 workers to handle API calls asynchronously. The get_weather function now uses executor.submit to fetch weather data in a separate thread, keeping the main loop responsive.
- **Impact**: No more waiting around when you ask for the weather—GrokVIS stays snappy.

### UI Dashboard

- **What's Done**: Integrated a Flask web server running on localhost:5000. The dashboard shows:
    - Scheduled Tasks: Pulls upcoming jobs from APScheduler's jobs.db.
    - Recent Commands: Displays the last 10 commands from command_log.txt.
    - System Statistics: Shows CPU, memory, and GPU usage (if available)
- **Impact**: You've got a pro-level control panel to monitor GrokVIS in real time.

### Voice Model

- **What's Done**: One-Class SVM for speaker verification—it's reliable and lightweight.
- **Future**: Ready to upgrade to more advanced models when you've got more data or GPU power.

## Customization

- Add new commands by extending the `process_command()` function in `commands.py`
- Customize the wake word in `speech.py`
- Add new web dashboard features in `web.py`
- Add new personality options by:
  1. Adding new TTS voice models in `speech.py`
  2. Creating new quips lists in `core.py`
  3. Updating the `setup_personality()` function to include your new option

### Extending Functionality Modules

- **Knowledge Module**: Add new information sources in `knowledge.py`
  - Integrate additional APIs for specialized knowledge domains
  - Add methods for different types of information retrieval

- **Entertainment Module**: Expand entertainment options in `entertainment.py`
  - Connect to music streaming services
  - Add games or interactive entertainment features
  - Integrate with video streaming platforms

- **Productivity Module**: Enhance productivity tools in `productivity.py`
  - Add calendar integration
  - Implement task prioritization
  - Create project management features

- **System Module**: Add system controls in `system.py`
  - Implement additional device controls
  - Add network management features
  - Create system monitoring capabilities




## Testing Framework

The Grok-VIS project includes a comprehensive testing framework to ensure all components work correctly and dependencies are properly installed.

### Test Structure

The testing framework consists of:

- **Core Tests**: Verify the basic structure and imports of the project
- **Dependency Tests**: Check if all required packages are installed
- **Speech Tests**: Validate speech recognition and synthesis components
- **Utility Scripts**: Tools for running tests and checking dependencies

### Running Tests

Several batch files are provided to simplify testing:

1. **Run All Tests**:
   ```
   run_tests.bat
   ```

2. **Check Dependencies**:
   ```
   check_dependencies.bat
   ```

3. **Install Dependencies**:
   ```
   install_dependencies.bat
   ```

4. **Run Specific Test**:
   ```
   run_specific_test.bat test_core
   ```

For detailed information about the testing framework, see:
- [TESTING.md](TESTING.md) - Comprehensive testing documentation
- [tests/README.md](tests/README.md) - Specific test file documentation

## How to Run Grok-VIS

- Run `python main.py` to start GrokVIS
- On first run, it will ask you to choose between Alfred and Beatrice
- Speak your choice
- GrokVIS will confirm your selection and continue with initialization
- To change your persona later, run `python reset_persona.py` and restart GrokVIS

## License

[MIT License](LICENSE)

## Acknowledgments

- This project uses various open-source libraries and APIs
- Inspired by JARVIS from the Iron Man movies
