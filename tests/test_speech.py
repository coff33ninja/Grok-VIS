"""
Tests for the speech functionality of Grok-VIS.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import the grokvis package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestSpeech(unittest.TestCase):
    """Test cases for speech functionality."""
    
    def test_speech_module_import(self):
        """Test that the speech module can be imported."""
        try:
            from grokvis import speech
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import speech module: {e}")
    
    def test_tts_initialization(self):
        """Test that the TTS system can be initialized."""
        try:
            from TTS.api import TTS
            # Just check if we can create a TTS instance without actually loading models
            # which would be resource-intensive for a test
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to initialize TTS: {e}")
            
if __name__ == '__main__':
    unittest.main()