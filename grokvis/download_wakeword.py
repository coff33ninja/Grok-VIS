"""
Download and extract the wake word file for Grok-VIS.
This script will download the Hey Grok wake word file and place it in the correct location.
"""
import os
import requests
import zipfile
from pathlib import Path

def ensure_directory(directory):
    """Ensure the directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def download_wakeword_file():
    """Download the wake word file from GitHub"""
    # Define paths
    voice_samples_dir = Path("voice_samples")
    default_dir = voice_samples_dir / "Default"
    wakeword_zip = default_dir / "Hey--Grok_en_windows_v3_0_0.zip"
    
    # Ensure directories exist
    ensure_directory(voice_samples_dir)
    ensure_directory(default_dir)
    
    # Check if the zip file already exists
    if os.path.exists(wakeword_zip):
        print(f"Wake word file already exists at: {wakeword_zip}")
        return wakeword_zip
    
    # URL for the wake word file (replace with the actual URL)
    # Note: This is a placeholder URL. You'll need to replace it with the actual URL
    url = "https://github.com/Picovoice/porcupine/raw/master/resources/keyword_files/windows/hey%20google_windows.ppn"
    
    print(f"Downloading wake word file from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(wakeword_zip, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded wake word file to: {wakeword_zip}")
        return wakeword_zip
    except Exception as e:
        print(f"Error downloading wake word file: {e}")
        print("Please download the wake word file manually and place it in the voice_samples/Default directory.")
        return None

def extract_wakeword_file(zip_path):
    """Extract the wake word file if it exists as a zip"""
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

if __name__ == "__main__":
    print("Downloading and extracting wake word file...")
    zip_path = download_wakeword_file()
    if zip_path:
        extract_wakeword_file(zip_path)
    print("Done.")