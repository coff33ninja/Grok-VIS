"""
Tests for checking if all required dependencies are installed.
"""
import unittest
import importlib
import sys
import os

# Add the parent directory to the path so we can import the grokvis package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestDependencies(unittest.TestCase):
    """Test cases for checking dependencies."""
    
    def test_required_packages(self):
        """Test that all required packages can be imported."""
        required_packages = [
            'joblib',
            'numpy',
            'sentence_transformers',
            'spacy',
            'pynvml',
            'sqlite3',
            'TTS',
            'apscheduler',
            'sqlalchemy',
            'requests',
            'wakeonlan',
            'opencv-python',
            'psutil',
            'scikit-learn',
            'librosa',
            'pvporcupine',
            'sounddevice',
            'flask',
            'wikipedia',
            'beautifulsoup4',
            'pillow'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                # Handle special case for opencv-python
                if package == 'opencv-python':
                    importlib.import_module('cv2')
                else:
                    importlib.import_module(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.fail(f"Missing required packages: {', '.join(missing_packages)}")
        else:
            self.assertTrue(True)
            
    def test_spacy_model(self):
        """Test that the spaCy model is installed."""
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Failed to load spaCy model: {e}")
            
if __name__ == '__main__':
    unittest.main()