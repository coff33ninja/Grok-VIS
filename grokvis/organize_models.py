"""
Organize model files for Grok-VIS.
This script will:
1. Move the wake word files to the models/wakeword directory
2. Move the voice model to the models/voice directory
3. Update references in the code to point to the new locations
"""
import os
import shutil
import zipfile
from pathlib import Path

def ensure_directory(directory):
    """Ensure the directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    return directory

def organize_wakeword_files():
    """Move wake word files to models/wakeword directory"""
    # Define paths
    source_dir = Path("voice_samples/Default")
    target_dir = Path("models/wakeword")
    
    # Ensure target directory exists
    ensure_directory(target_dir)
    
    # Check for wake word files in source directory
    wakeword_zip = source_dir / "Hey--Grok_en_windows_v3_0_0.zip"
    wakeword_ppn = source_dir / "Hey--Grok_en_windows_v3_0_0.ppn"
    
    # Move zip file if it exists
    if os.path.exists(wakeword_zip):
        target_zip = target_dir / wakeword_zip.name
        if not os.path.exists(target_zip):
            shutil.copy2(wakeword_zip, target_zip)
            print(f"Copied wake word zip file to: {target_zip}")
    else:
        print(f"Wake word zip file not found at: {wakeword_zip}")
        
        # Check if it exists in the voice_samples directory
        alt_wakeword_zip = Path("voice_samples") / "Hey--Grok_en_windows_v3_0_0.zip"
        if os.path.exists(alt_wakeword_zip):
            target_zip = target_dir / alt_wakeword_zip.name
            if not os.path.exists(target_zip):
                shutil.copy2(alt_wakeword_zip, target_zip)
                print(f"Copied wake word zip file from alternate location to: {target_zip}")
    
    # Move ppn file if it exists
    if os.path.exists(wakeword_ppn):
        target_ppn = target_dir / wakeword_ppn.name
        if not os.path.exists(target_ppn):
            shutil.copy2(wakeword_ppn, target_ppn)
            print(f"Copied wake word ppn file to: {target_ppn}")
    else:
        print(f"Wake word ppn file not found at: {wakeword_ppn}")
    
    # Extract zip file if it exists in the target directory
    target_zip = target_dir / "Hey--Grok_en_windows_v3_0_0.zip"
    if os.path.exists(target_zip) and not os.path.exists(target_dir / "Hey--Grok_en_windows_v3_0_0.ppn"):
        try:
            with zipfile.ZipFile(target_zip, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            print(f"Extracted wake word file to: {target_dir}")
        except Exception as e:
            print(f"Error extracting wake word file: {e}")

def organize_voice_model():
    """Move voice model to models/voice directory"""
    # Define paths
    source_file = Path("voice_model.pkl")
    target_dir = Path("models/voice")
    
    # Ensure target directory exists
    ensure_directory(target_dir)
    
    # Move voice model if it exists
    if os.path.exists(source_file):
        target_file = target_dir / source_file.name
        if not os.path.exists(target_file):
            shutil.copy2(source_file, target_file)
            print(f"Copied voice model to: {target_file}")
    else:
        print(f"Voice model not found at: {source_file}")

def update_code_references():
    """Update code references to point to the new model locations"""
    # Update speech.py
    speech_py = Path("grokvis/speech.py")
    if os.path.exists(speech_py):
        with open(speech_py, 'r') as f:
            content = f.read()
        
        # Update voice model path
        content = content.replace("joblib.load('voice_model.pkl')", "joblib.load('models/voice/voice_model.pkl')")
        content = content.replace("joblib.dump(model, 'voice_model.pkl')", "joblib.dump(model, 'models/voice/voice_model.pkl')")
        
        # Update wake word path references
        content = content.replace(
            "wake_word_handle = pvporcupine.create(",
            "wake_word_handle = pvporcupine.create(model_path='models/wakeword/Hey--Grok_en_windows_v3_0_0.ppn',"
        )
        
        with open(speech_py, 'w') as f:
            f.write(content)
        print(f"Updated code references in: {speech_py}")

if __name__ == "__main__":
    print("Organizing model files...")
    organize_wakeword_files()
    organize_voice_model()
    update_code_references()
    print("Done organizing model files.")