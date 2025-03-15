import os
import zipfile
import shutil
from pathlib import Path

def ensure_directory(directory):
    """Ensure the directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def extract_wakeword_file():
    """Extract the wake word file if it exists as a zip"""
    # Define paths
    voice_samples_dir = Path("voice_samples")
    default_dir = voice_samples_dir / "Default"
    wakeword_zip = default_dir / "Hey--Grok_en_windows_v3_0_0.zip"
    
    # Ensure directories exist
    ensure_directory(voice_samples_dir)
    ensure_directory(default_dir)
    
    # Check if the zip file exists
    if os.path.exists(wakeword_zip):
        print(f"Found wake word file: {wakeword_zip}")
        try:
            # Extract the zip file
            with zipfile.ZipFile(wakeword_zip, 'r') as zip_ref:
                zip_ref.extractall(default_dir)
            print(f"Successfully extracted wake word file to {default_dir}")
            return True
        except Exception as e:
            print(f"Error extracting wake word file: {e}")
            return False
    else:
        print(f"Wake word file not found at: {wakeword_zip}")
        print("Please ensure you have the correct wake word file in the voice_samples/Default directory.")
        return False

if __name__ == "__main__":
    print("Checking for wake word file...")
    extract_wakeword_file()
    print("Done.")