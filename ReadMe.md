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
└── commands.py       # Command processing
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

- **Weather**: "What's the weather in [city]?" or "Give me the forecast for [city]"
- **Scheduling**: "Schedule [task] at [time]", "Show my schedule", "Remove [task]"
- **Memory**: "Remember [information]", "What did I say about [topic]?"
- **Home Automation**: "Turn on/off [device]", "Check if [device] is online"
- **System**: "Quit" or "Shutdown"

## Web Dashboard

Access the dashboard at http://localhost:5000 to:
- View scheduled tasks
- See recent commands
- Monitor system statistics

## Key Enhancements

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

## Package Structure
grokvis/
├── __init__.py       # Package initialization
├── core.py           # Core functionality and initialization
├── speech.py         # Speech recognition and TTS
├── memory.py         # Memory storage and retrieval
├── scheduler.py      # Event scheduling
├── home_automation.py # Device control
├── weather.py        # Weather services
├── web.py            # Web dashboard
└── commands.py       # Command processing


## How to Test
- Run python main.py to start GrokVIS
- On first run, it will ask you to choose between Alfred and Beatrice
- Speak your choice
- GrokVIS will confirm your selection and continue with initialization
- To change your persona later, run python reset_persona.py and restart GrokVIS

## License

[MIT License](LICENSE)

## Acknowledgments

- This project uses various open-source libraries and APIs
- Inspired by JARVIS from the Iron Man movies
