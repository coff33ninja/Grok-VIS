"""
Setup wake word detection for Grok-VIS.
This script will:
1. Download the wake word file if it doesn't exist
2. Extract the wake word file and verify the model
3. Place it in the correct location (models/wakeword) and update references
"""

import os
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
    """Download or locate the wake word file if it doesn't exist"""
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

    # If the file doesn't exist, provide manual download instructions
    print(
        "Wake word file not found. Please download it manually from the Picovoice Console:"
    )
    print("1. Go to https://console.picovoice.ai/")
    print("2. Create an account and generate an access key")
    print("3. Download the 'Hey Grok' wake word for Windows")
    print(
        "4. Place the file in the models/wakeword directory as 'Hey--Grok_en_windows_v3_0_0.zip'"
    )

    return None


def extract_wakeword_file(zip_path):
    """Extract the wake word file and verify the .ppn file exists"""
    if zip_path and os.path.exists(zip_path):
        try:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(os.path.dirname(zip_path))
            print(
                f"Successfully extracted wake word file to {os.path.dirname(zip_path)}"
            )

            # Verify the .ppn file exists
            ppn_file = (
                Path(os.path.dirname(zip_path)) / "Hey--Grok_en_windows_v3_0_0.ppn"
            )
            if not ppn_file.exists():
                print(
                    f"Error: Expected .ppn file not found at {ppn_file}. Check the zip file contents."
                )
                return False
            print(f"Verified wake word model at: {ppn_file}")
            return True
        except Exception as e:
            print(f"Error extracting wake word file: {e}")
            return False
    return False


def update_code_references():
    """Update code references to point to the new model location"""
    speech_py = Path("grokvis/speech.py")
    if os.path.exists(speech_py):
        with open(speech_py, "r") as f:
            content = f.read()

        # Check if model_path is already present
        if "model_path=" not in content:
            # Create a backup
            backup_path = speech_py.with_suffix(".py.bak")
            shutil.copy2(speech_py, backup_path)
            print(f"Created backup of speech.py at: {backup_path}")

            # Update wake word path references
            content = content.replace(
                "wake_word_handle = pvporcupine.create(",
                "wake_word_handle = pvporcupine.create(model_path='models/wakeword/Hey--Grok_en_windows_v3_0_0.ppn',",
            )

            with open(speech_py, "w") as f:
                f.write(content)
            print(f"Updated code references in: {speech_py}")
            print(
                "Please verify the changes in grokvis/speech.py to ensure correctness."
            )
        else:
            print(f"Code references already updated in: {speech_py}")


if __name__ == "__main__":
    print("Setting up wake word detection...")
    zip_path = download_wakeword_file()
    if zip_path and extract_wakeword_file(zip_path):
        update_code_references()
    print("Done setting up wake word detection.")
