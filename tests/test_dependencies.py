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
        
        # Map package names to their import names
        package_import_map = {
            'scikit-learn': 'sklearn',
            'beautifulsoup4': 'bs4',
            'pillow': 'PIL',
            'opencv-python': 'cv2',
            'speech_recognition': 'speech_recognition'
        }
        
        missing_packages = []
        for package in required_packages:
            try:
                # Use the import name if it's in the map, otherwise use the package name
                import_name = package_import_map.get(package, package)
                importlib.import_module(import_name)
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