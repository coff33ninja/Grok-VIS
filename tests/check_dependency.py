"""
Utility script to check if a specific dependency is installed.
"""
import importlib
import sys

def check_dependency(package_name):
    """
    Check if a specific package is installed.
    
    Args:
        package_name (str): The name of the package to check.
        
    Returns:
        bool: True if the package is installed, False otherwise.
    """
    try:
        # Handle special case for opencv-python
        if package_name == 'opencv-python':
            importlib.import_module('cv2')
        else:
            importlib.import_module(package_name)
        print(f"✅ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_dependency.py <package_name>")
        sys.exit(1)
        
    package_name = sys.argv[1]
    success = check_dependency(package_name)
    sys.exit(0 if success else 1)