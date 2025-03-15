"""
Setup wake word detection for Grok-VIS.
This script will:
1. Download the wake word file if it doesn't exist
2. Extract the wake word file
3. Place it in the correct location (models/wakeword)
"""
import os
import requests
import zipfile
import shutil
from pathlib import Path

def ensure_directory(directory):
    """Ensure the directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    return directory

def download_wakeword_file():
    """Download the wake word file if it doesn't exist"""
    # Define paths
    models_dir = ensure_directory(Path("models"))
    wakeword_dir = ensure_directory(Path("models/wakeword"))
    wakeword_zip = wakeword_dir / "Hey--Grok_en_windows_v3_0_0.zip"
    
    # Check if the wake word file already exists in the models directory
    if os.path.exists(wakeword_zip):
        print(f"Wake word file already exists at: {wakeword_zip}")
        return wakeword_zip
    
    # Check if the wake word file exists in the voice_samples directory
    voice_samples_zip = Path("voice_samples/Default/Hey--Grok_en_windows_v3_0_0.zip")
    if os.path.exists(voice_samples_zip):
        print(f"Found wake word file at: {voice_samples_zip}")
        shutil.copy2(voice_samples_zip, wakeword_zip)
        print(f"Copied wake word file to: {wakeword_zip}")
        return wakeword_zip
    
    # Check if the wake word file exists in the voice_samples root directory
    voice_samples_root_zip = Path("voice_samples/Hey--Grok_en_windows_v3_0_0.zip")
    if os.path.exists(voice_samples_root_zip):
        print(f"Found wake word file at: {voice_samples_root_zip}")
        shutil.copy2(voice_samples_root_zip, wakeword_zip)
        print(f"Copied wake word file to: {wakeword_zip}")
        return wakeword_zip
    
    # If the file doesn't exist, download it
    print("Wake word file not found. Please download it manually from the Picovoice Console.")
    print("1. Go to https://console.picovoice.ai/")
    print("2. Create an account and access key")
    print("3. Download the 'Hey Grok' wake word for Windows")
    print("4. Place the file in the models/wakeword directory as 'Hey--Grok_en_windows_v3_0_0.zip'")
    
    return None

def extract_wakeword_file(zip_path):
    """Extract the wake word file"""
    if zip_path and os.path.exists(zip_path):
        try:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(zip_path))
            print(f"Successfully extracted wake word file to {os.path.dirname(zip_path)}")
            return True
        except Exception as e:
            print(f"Error extracting wake word file: {e}")
            return False
    return False

def update_code_references():
    """Update code references to point to the new model locations"""
    # Update speech.py
    speech_py = Path("grokvis/speech.py")
    if os.path.exists(speech_py):
        with open(speech_py, 'r') as f:
            content = f.read()
        
        # Update wake word path references
        if "model_path=" not in content:
            content = content.replace(
                "wake_word_handle = pvporcupine.create(",
                "wake_word_handle = pvporcupine.create(model_path='models/wakeword/Hey--Grok_en_windows_v3_0_0.ppn',"
            )
            
            with open(speech_py, 'w') as f:
                f.write(content)
            print(f"Updated code references in: {speech_py}")
        else:
            print(f"Code references already updated in: {speech_py}")

if __name__ == "__main__":
    print("Setting up wake word detection...")
    zip_path = download_wakeword_file()
    if zip_path:
        extract_wakeword_file(zip_path)
        update_code_references()
    print("Done setting up wake word detection.")