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
import io

# Fix Windows encoding issues
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('error_diagnosis.log', encoding='utf-8')
    ]
)

def check_python_version():
    python_version = platform.python_version()
    logging.info(f"Python version: {python_version}")
    major, minor, _ = map(int, python_version.split('.'))
    return major >= 3 and minor >= 8

def check_system_info():
    logging.info(f"Operating System: {platform.system()} {platform.release()}")
    logging.info(f"Machine: {platform.machine()}")
    logging.info(f"Processor: {platform.processor()}")
    return platform.system() in ['Windows', 'Linux', 'Darwin']

def check_dependencies():
    required_packages = [
        'joblib', 'numpy', 'sentence_transformers', 'spacy', 'pynvml',
        'TTS', 'apscheduler', 'sqlalchemy', 'requests', 'wakeonlan',
        'opencv-python', 'psutil', 'sklearn', 'librosa', 'pvporcupine',
        'sounddevice', 'flask', 'wikipedia', 'bs4', 'PIL'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'opencv-python':
                importlib.import_module('cv2')
            else:
                importlib.import_module(package)
            logging.info(f"[✓] {package} is installed")
        except ImportError as e:
            logging.error(f"[✗] {package} is NOT installed: {str(e)}")
            missing_packages.append(package)
    
    if missing_packages:
        logging.error(f"Missing dependencies: {', '.join(missing_packages)}")
        logging.info("To install missing dependencies, run: pip install -r requirements.txt")
        return False
    return True

def check_spacy_model():
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        logging.info("[✓] spaCy model 'en_core_web_sm' is installed")
        return True
    except (ImportError, OSError) as e:
        logging.error(f"[✗] spaCy model check failed: {str(e)}")
        logging.info("To install: python -m spacy download en_core_web_sm")
        return False

def check_grokvis_imports():
    try:
        import grokvis
        from grokvis import core
        logging.info("[✓] grokvis package and core module can be imported")
        return True
    except ImportError as e:
        logging.error(f"[✗] Failed to import grokvis: {str(e)}")
        return False

def check_file_permissions():
    files_to_check = {
        '../main.py': "main.py",
        '../grokvis': "grokvis directory",
        '../requirements.txt': "requirements.txt"
    }
    
    all_good = True
    for path, name in files_to_check.items():
        try:
            if os.path.isdir(path):
                os.listdir(path)
                logging.info(f"[✓] {name} is readable")
            elif os.path.isfile(path):
                with open(path, 'r') as f:
                    f.read(1)
                logging.info(f"[✓] {name} is readable")
            else:
                logging.error(f"[✗] {name} does not exist")
                all_good = False
        except Exception as e:
            logging.error(f"[✗] {name} access error: {str(e)}")
            all_good = False
    return all_good

def check_log_files():
    log_file = '../grokvis_errors.log'
    try:
        with open(log_file, 'a') as f:
            f.write('')
        logging.info("[✓] grokvis_errors.log is writable")
        return True
    except Exception as e:
        logging.error(f"[✗] Log file error: {str(e)}")
        return False

def run_diagnosis():
    logging.info("Starting Grok-VIS error diagnosis...")
    
    results = {
        "Python Version": check_python_version(),
        "System Compatibility": check_system_info(),
        "Dependencies": check_dependencies(),
        "spaCy Model": check_spacy_model(),
        "Grok-VIS Imports": check_grokvis_imports(),
        "File Permissions": check_file_permissions(),
        "Log Files": check_log_files()
    }
    
    logging.info("\n=== Diagnosis Summary ===")
    for check, passed in results.items():
        logging.info(f"{check}: {'[✓] OK' if passed else '[✗] ERROR'}")
    
    if all(results.values()):
        logging.info("\n[✓] All checks passed! Grok-VIS should work correctly.")
    else:
        logging.error("\n[✗] Some checks failed. Please fix the issues above.")
    
    logging.info("\nSee error_diagnosis.log for detailed information.")

if __name__ == '__main__':
    run_diagnosis()