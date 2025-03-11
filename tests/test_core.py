"""
Tests for the core functionality of Grok-VIS.
"""
import unittest
import sys
import os

# Add the parent directory to the path so we can import the grokvis package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCore(unittest.TestCase):
    """Test cases for core functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Any setup code goes here
        pass
        
    def tearDown(self):
        """Tear down test fixtures."""
        # Any cleanup code goes here
        pass
    
    def test_imports(self):
        """Test that all required modules can be imported."""
        try:
            import grokvis
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import grokvis: {e}")
            
    def test_module_structure(self):
        """Test that the module structure is correct."""
        try:
            from grokvis import __init__
            from grokvis import core
            from grokvis import commands
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")
            
if __name__ == '__main__':
    unittest.main()