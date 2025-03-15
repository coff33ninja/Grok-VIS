# Troubleshooting Guide for Grok-VIS

## Issues Fixed

1. **Wake Word File Location**
   - The wake word file `Hey--Grok_en_windows_v3_0_0.zip` was moved to the correct location in `voice_samples/Default/`
   - The file was successfully extracted

2. **Audio Recording**
   - The audio system is working correctly
   - Both speech_recognition and sounddevice tests passed
   - Test recordings were saved in `voice_samples/test/`

## Remaining Issues

1. **Voice Training**
   - The voice training process is failing to record samples
   - This might be due to microphone access issues or configuration problems

## How to Run the Application

1. **Run the main script**:
   ```
   python main.py
   ```

2. **Choose a persona**:
   - When prompted, say "Alfred" or "Beatrice"

3. **Voice Training**:
   - The system will ask you to say 10 phrases
   - Speak clearly into your microphone after each prompt

4. **Wake Word Detection**:
   - Once training is complete, the system will listen for the wake word "Hey Grok"
   - After saying the wake word, you can give commands

## Troubleshooting Steps

If you encounter issues:

1. **Check Microphone Access**:
   - Ensure your application has permission to access the microphone
   - Check Windows privacy settings for microphone access

2. **Run Audio Diagnostics**:
   ```
   python tests\check_audio.py
   ```

3. **Verify Wake Word File**:
   ```
   python tests\extract_wakeword.py
   ```

4. **Check Log Files**:
   - Look for error messages in `grokvis_errors.log`
   - Check `error_diagnosis.log` for additional information

5. **Reset Persona**:
   ```
   python reset_persona.py
   ```
   This will allow you to choose a new persona the next time you run the application.

## Common Issues and Solutions

1. **"Sorry, I couldn't record that"**:
   - Ensure your microphone is connected and working
   - Check if other applications can access your microphone
   - Try using a different microphone

2. **"Sorry, wake word detection failed"**:
   - Ensure the wake word file is correctly extracted
   - Check if the Picovoice access key is valid
   - Try reinstalling the pvporcupine package

3. **"Voice model trained" but no response to commands**:
   - The wake word detection might not be working
   - Try speaking louder or in a quieter environment
   - Check if the dashboard is running at http://localhost:5000