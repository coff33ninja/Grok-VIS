"""
Place the wake word file in the correct location.
This script will copy the wake word file from the tests directory to the voice_samples/Default directory.
"""
import os
import shutil
from pathlib import Path

def ensure_directory(directory):
    """Ensure the directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def place_wakeword_file():
    """Place the wake word file in the correct location"""
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
        return True
    
    # Check if the wake word file exists in the tests directory
    test_wakeword = Path("tests") / "Hey--Grok_en_windows_v3_0_0.zip"
    if os.path.exists(test_wakeword):
        print(f"Found wake word file in tests directory: {test_wakeword}")
        try:
            shutil.copy(test_wakeword, wakeword_zip)
            print(f"Successfully copied wake word file to: {wakeword_zip}")
            return True
        except Exception as e:
            print(f"Error copying wake word file: {e}")
            return False
    
    print("Wake word file not found in tests directory.")
    print("Please place the Hey--Grok_en_windows_v3_0_0.zip file in the voice_samples/Default directory.")
    return False

if __name__ == "__main__":
    print("Placing wake word file...")
    place_wakeword_file()
    print("Done.")