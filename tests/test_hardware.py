"""
Test hardware detection functionality.
"""
import sys
import os
import unittest

# Add the parent directory to the path so we can import the grokvis package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grokvis.hardware_manager import get_hardware_manager

class TestHardwareDetection(unittest.TestCase):
    """Test hardware detection functionality."""
    
    def test_hardware_detection(self):
        """Test that hardware detection works."""
        hw_manager = get_hardware_manager()
        
        # Check that hardware info is populated
        self.assertIsNotNone(hw_manager.hardware_info)
        self.assertIsNotNone(hw_manager.hardware_info['platform'])
        
        # Check CPU info
        self.assertIsNotNone(hw_manager.hardware_info['cpu']['vendor'])
        self.assertIsNotNone(hw_manager.hardware_info['cpu']['threads'])
        
        # Print hardware summary for debugging
        print("\nHardware Detection Results:")
        print(hw_manager.get_summary())
        
        # Check that optimal device is determined
        optimal_device = hw_manager.get_optimal_device()
        self.assertIn(optimal_device, ['cuda', 'mps', 'directml', 'cpu'])
        
        # Check TTS config
        tts_config = hw_manager.get_tts_config()
        self.assertIsNotNone(tts_config)
        self.assertIn('model_name', tts_config)
        self.assertIn('gpu', tts_config)
        
        print(f"\nTTS Configuration: {tts_config}")

if __name__ == '__main__':
    unittest.main()