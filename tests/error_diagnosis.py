"""
Utility script for diagnosing errors in Grok-VIS.
This script helps identify common issues and provides suggestions for fixing them.
"""
import sys
import os
import importlib
import platform
import logging
import traceback

# Add the parent directory to the path so we can import the grokvis package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('error_diagnosis.log')
    ]
)

def check_python_version():
    """Check if the Python version is compatible with Grok-VIS."""
    python_version = platform.python_version()
    logging.info(f"Python version: {python_version}")
    
    # Check if the Python version is at least 3.8
    major, minor, _ = map(int, python_version.split('.'))
    if major < 3 or (major == 3 and minor < 8):
        logging.error("Python version is too old. Grok-VIS requires Python 3.8 or newer.")
        return False
    
    return True

def check_system_info():
    """Check system information."""
    logging.info(f"Operating System: {platform.system()} {platform.release()}")
    logging.info(f"Machine: {platform.machine()}")
    logging.info(f"Processor: {platform.processor()}")
    
    # Check if the system is compatible with Grok-VIS
    if platform.system() not in ['Windows', 'Linux', 'Darwin']:
        logging.warning("Unsupported operating system. Grok-VIS is designed for Windows, Linux, and macOS.")

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'joblib',
        'numpy',
        'sentence_transformers',
        'spacy',
        'pynvml',
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
            logging.info(f"✅ {package} is installed")
        except ImportError:
            logging.error(f"❌ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        logging.error(f"Missing dependencies: {', '.join(missing_packages)}")
        logging.info("To install missing dependencies, run: pip install -r requirements.txt")
        return False
    
    return True

def check_spacy_model():
    """Check if the spaCy model is installed."""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        logging.info("✅ spaCy model 'en_core_web_sm' is installed")
        return True
    except ImportError:
        logging.error("❌ spaCy is NOT installed")
        return False
    except OSError:
        logging.error("❌ spaCy model 'en_core_web_sm' is NOT installed")
        logging.info("To install the spaCy model, run: python -m spacy download en_core_web_sm")
        return False

def check_grokvis_imports():
    """Check if the Grok-VIS package can be imported."""
    try:
        import grokvis
        logging.info("✅ grokvis package can be imported")
        
        # Check if core modules can be imported
        from grokvis import core
        logging.info("✅ grokvis.core module can be imported")
        
        return True
    except ImportError as e:
        logging.error(f"❌ Failed to import grokvis: {e}")
        return False
    except Exception as e:
        logging.error(f"❌ Error importing grokvis: {e}")
        traceback.print_exc()
        return False

def check_file_permissions():
    """Check if the necessary files have the correct permissions."""
    try:
        # Check if the main.py file exists and is readable
        if os.path.isfile('../main.py'):
            with open('../main.py', 'r') as f:
                f.read(1)  # Try to read one byte
            logging.info("✅ main.py is readable")
        else:
            logging.error("❌ main.py does not exist")
            
        # Check if the grokvis directory exists and is readable
        if os.path.isdir('../grokvis'):
            os.listdir('../grokvis')
            logging.info("✅ grokvis directory is readable")
        else:
            logging.error("❌ grokvis directory does not exist")
            
        # Check if the requirements.txt file exists and is readable
        if os.path.isfile('../requirements.txt'):
            with open('../requirements.txt', 'r') as f:
                f.read(1)  # Try to read one byte
            logging.info("✅ requirements.txt is readable")
        else:
            logging.error("❌ requirements.txt does not exist")
            
        return True
    except PermissionError as e:
        logging.error(f"❌ Permission error: {e}")
        return False
    except Exception as e:
        logging.error(f"❌ Error checking file permissions: {e}")
        return False

def check_log_files():
    """Check if log files exist and are writable."""
    try:
        # Check if the grokvis_errors.log file is writable
        with open('../grokvis_errors.log', 'a') as f:
            f.write('')
        logging.info("✅ grokvis_errors.log is writable")
        
        return True
    except FileNotFoundError:
        # This is okay, the file will be created when needed
        logging.info("✅ grokvis_errors.log does not exist yet, but will be created when needed")
        return True
    except PermissionError as e:
        logging.error(f"❌ Permission error: {e}")
        return False
    except Exception as e:
        logging.error(f"❌ Error checking log files: {e}")
        return False

def run_diagnosis():
    """Run all diagnostic checks."""
    logging.info("Starting Grok-VIS error diagnosis...")
    
    # Check Python version
    python_version_ok = check_python_version()
    
    # Check system information
    check_system_info()
    
    # Check dependencies
    dependencies_ok = check_dependencies()
    
    # Check spaCy model
    spacy_model_ok = check_spacy_model()
    
    # Check Grok-VIS imports
    grokvis_imports_ok = check_grokvis_imports()
    
    # Check file permissions
    file_permissions_ok = check_file_permissions()
    
    # Check log files
    log_files_ok = check_log_files()
    
    # Print summary
    logging.info("\n=== Diagnosis Summary ===")
    logging.info(f"Python Version: {'✅ OK' if python_version_ok else '❌ ERROR'}")
    logging.info(f"Dependencies: {'✅ OK' if dependencies_ok else '❌ ERROR'}")
    logging.info(f"spaCy Model: {'✅ OK' if spacy_model_ok else '❌ ERROR'}")
    logging.info(f"Grok-VIS Imports: {'✅ OK' if grokvis_imports_ok else '❌ ERROR'}")
    logging.info(f"File Permissions: {'✅ OK' if file_permissions_ok else '❌ ERROR'}")
    logging.info(f"Log Files: {'✅ OK' if log_files_ok else '❌ ERROR'}")
    
    # Overall status
    all_ok = (python_version_ok and dependencies_ok and spacy_model_ok and 
              grokvis_imports_ok and file_permissions_ok and log_files_ok)
    
    if all_ok:
        logging.info("\n✅ All checks passed! Grok-VIS should work correctly.")
    else:
        logging.error("\n❌ Some checks failed. Please fix the issues above.")
        
    logging.info("\nFor more detailed information, see the error_diagnosis.log file.")

if __name__ == '__main__':
    run_diagnosis()