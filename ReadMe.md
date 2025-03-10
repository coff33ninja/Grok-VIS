# GROK-VIS Setup and Installation

## Necessary Imports

Here are all the imports required for the script:

```python
import speech_recognition as sr
import requests
import datetime
import random
import wakeonlan
import socket
import spacy
import sqlite3
import cv2
import psutil
import pynvml
import subprocess
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import librosa
from sklearn.svm import OneClassSVM
import joblib
import glob
import os
import pvporcupine
import struct
import sounddevice as sd
from TTS.api import TTS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template_string
import threading
```

## Setup Instructions

### Install Dependencies

Run this command to install everything you need:

```bash
pip install speechrecognition requests wakeonlan spacy sqlite3 opencv-python psutil pynvml numpy sentence-transformers scikit-learn librosa joblib pvporcupine sounddevice TTS apscheduler SQLAlchemy flask
```

Then download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

### API Keys and Customizations

- Replace "YOUR_PICOVOICE_ACCESS_KEY" with your Picovoice access key (get it from the Picovoice Console).
- Replace "YOUR_API_KEY" with your OpenWeatherMap API key (sign up at openweathermap.org).
- Update "YOUR_PC_MAC" with your PC’s MAC address (e.g., "00:11:22:33:44:55") for Wake-on-LAN.

## Run the Script

Save as `grokvis.py` and run:

```bash
python grokvis.py
```

After starting the script, try these commands:

- **Voice Command**: Say "Hey GrokVis" followed by commands like:
    - "Turn on my PC"
    - "What’s the weather in London?"
    - "Schedule a reminder at 15:00 for tea"
    - "Quit"
- **Dashboard**: Open your browser to [http://localhost:5000](http://localhost:5000) to see the dashboard.

## Key Enhancements

### Async Handling

- **What’s Done**: Added a ThreadPoolExecutor with 2 workers to handle API calls asynchronously. The get_weather function now uses executor.submit to fetch weather data in a separate thread, keeping the main loop responsive.
- **Impact**: No more waiting around when you ask for the weather—GROK-VIS stays snappy.

### UI Dashboard

- **What’s Done**: Integrated a Flask web server running on localhost:5000. The dashboard shows:
    - Scheduled Tasks: Pulls upcoming jobs from APScheduler’s jobs.db.
    - Recent Commands: Displays the last 10 commands from command_log.txt.
- **How It Looks**: A simple HTML page with two lists—tasks (e.g., "2025-03-11 15:00 - Reminder: tea now") and commands (e.g., "weather in London").
- **Impact**: You’ve got a pro-level control panel to monitor GROK-VIS in real time.

### Voice Model

- **What’s Done**: Left the One-Class SVM as-is—it’s reliable and lightweight for now.
- **Future**: Ready to upgrade to Deep Speaker when you’ve got more data or GPU power.

## Testing It Out

- **Wake Word**: Say “Hey GrokVis” and watch it spring to life.
- **Weather**: Ask for the weather in a city—it’ll fetch it in the background while staying responsive.
- **Dashboard**: Visit [http://localhost:5000](http://localhost:5000) in your browser to see your tasks and commands.

GROK-VIS is now a lean, mean, responsive machine with a slick UI—your digital butler just got a turbo boost! What’s next, DJ—tweak the dashboard, add MQTT for home automation, or something wilder? Let’s keep this symphony rocking!
