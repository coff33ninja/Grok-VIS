import speech_recognition as sr
import sounddevice as sd
import numpy as np
import time
import os
from pathlib import Path

def check_microphone_devices():
    """List all available microphone devices"""
    print("\n=== Available Audio Devices ===")
    devices = sd.query_devices()
    
    print("\nAll devices:")
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']} (Channels In: {device['max_input_channels']}, Out: {device['max_output_channels']})")
    
    print("\nInput devices:")
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"{i}: {device['name']} (Channels: {device['max_input_channels']})")
    
    # Get default devices
    try:
        default_input = sd.query_devices(kind='input')
        print(f"\nDefault input device: {default_input['name']}")
    except Exception as e:
        print(f"\nError getting default input device: {e}")

def test_microphone_recording():
    """Test microphone recording using speech_recognition"""
    print("\n=== Testing Microphone with Speech Recognition ===")
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Microphone initialized successfully!")
            print("Recording 3 seconds of audio...")
            audio = r.record(source, duration=3)
            print("Recording completed successfully!")
            
            # Save the audio to a file
            output_dir = Path("voice_samples/test")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            wav_file = output_dir / f"test_recording_{int(time.time())}.wav"
            with open(wav_file, "wb") as f:
                f.write(audio.get_wav_data())
            print(f"Audio saved to {wav_file}")
            
            return True
    except Exception as e:
        print(f"Error during microphone recording: {e}")
        return False

def test_sounddevice_recording():
    """Test microphone recording using sounddevice"""
    print("\n=== Testing Microphone with SoundDevice ===")
    
    try:
        # Record 3 seconds of audio
        sample_rate = 16000
        duration = 3  # seconds
        print(f"Recording {duration} seconds of audio...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        print("Recording completed successfully!")
        
        # Save the audio to a file
        output_dir = Path("voice_samples/test")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        import scipy.io.wavfile as wav
        wav_file = output_dir / f"test_sd_recording_{int(time.time())}.wav"
        wav.write(wav_file, sample_rate, recording)
        print(f"Audio saved to {wav_file}")
        
        return True
    except Exception as e:
        print(f"Error during sounddevice recording: {e}")
        return False

if __name__ == "__main__":
    print("=== Audio System Diagnostic ===")
    
    # Check microphone devices
    check_microphone_devices()
    
    # Test recording with speech_recognition
    sr_success = test_microphone_recording()
    
    # Test recording with sounddevice
    sd_success = test_sounddevice_recording()
    
    # Summary
    print("\n=== Diagnostic Summary ===")
    print(f"Speech Recognition Test: {'✓ Passed' if sr_success else '✗ Failed'}")
    print(f"SoundDevice Test: {'✓ Passed' if sd_success else '✗ Failed'}")
    
    if sr_success and sd_success:
        print("\nAll audio tests passed! Your microphone is working correctly.")
    else:
        print("\nSome audio tests failed. Please check your microphone settings.")
        
    print("\nDone.")