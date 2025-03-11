# Grok-VIS Tests Documentation

This document provides an overview of the testing framework for the Grok-VIS project, including descriptions of test files, test cases, and instructions for running tests.

## Overview

The Grok-VIS testing framework consists of several test files that verify different aspects of the project:

- Core functionality tests
- Dependency verification tests
- Speech functionality tests

Additionally, utility scripts are provided to:
- Run all tests
- Check individual dependencies
- Run specific test files

## Test Files

### 1. `test_core.py`

Tests the core functionality of the Grok-VIS system.

**Test Cases:**
- `test_imports`: Verifies that the main Grok-VIS package can be imported
- `test_module_structure`: Checks that the module structure is correct and all essential modules can be imported

**Purpose:**  
Ensures that the basic structure of the Grok-VIS project is intact and that the core modules are accessible.

### 2. `test_dependencies.py`

Verifies that all required dependencies are installed and accessible.

**Test Cases:**
- `test_required_packages`: Checks if all packages listed in requirements.txt can be imported
- `test_spacy_model`: Verifies that the spaCy English language model is installed and can be loaded

**Purpose:**  
Identifies missing or incorrectly installed dependencies that might cause runtime errors.

### 3. `test_speech.py`

Tests the speech functionality components of Grok-VIS.

**Test Cases:**
- `test_speech_module_import`: Verifies that the speech module can be imported
- `test_tts_initialization`: Checks if the Text-to-Speech system can be initialized

**Purpose:**  
Ensures that the speech recognition and synthesis components are properly set up.

### 4. `test_errors.py`

Tests the error handling capabilities of Grok-VIS.

**Test Cases:**
- `test_logging_setup`: Verifies that logging is set up correctly
- `test_error_logging`: Checks if errors are properly logged
- `test_exception_handling`: Tests that exceptions are properly handled
- `test_missing_dependency_error`: Tests how the system handles missing dependencies

**Purpose:**  
Ensures that the system can properly handle and log errors, making it easier to diagnose and fix issues.

## Utility Scripts

### 1. `run_tests.py`

A Python script that discovers and runs all test files in the tests directory.

**Usage:**
```python
python tests/run_tests.py
```

**Purpose:**  
Provides a convenient way to run all tests at once and get a summary of the results.

### 2. `check_dependency.py`

A utility script to check if a specific dependency is installed.

**Usage:**
```python
python tests/check_dependency.py <package_name>
```

**Example:**
```python
python tests/check_dependency.py joblib
```

**Purpose:**  
Allows for checking individual dependencies to troubleshoot installation issues.

### 3. `error_diagnosis.py`

A comprehensive diagnostic tool that checks the entire Grok-VIS installation for issues.

**Usage:**
```python
python tests/error_diagnosis.py
```

**Purpose:**  
Provides detailed information about the system, dependencies, and potential issues to help diagnose and fix problems.

## Batch Files

Several batch files are provided to simplify running tests and managing dependencies:

### 1. `run_tests.bat`

Runs all tests in the tests directory.

**Usage:**
```
run_tests.bat
```

### 2. `check_dependencies.bat`

Checks if all required dependencies are installed.

**Usage:**
```
check_dependencies.bat
```

### 3. `install_dependencies.bat`

Installs all required dependencies from requirements.txt.

**Usage:**
```
install_dependencies.bat
```

### 4. `run_specific_test.bat`

Runs a specific test file.

**Usage:**
```
run_specific_test.bat <test_file_name>
```

**Example:**
```
run_specific_test.bat test_core
```
or
```
run_specific_test.bat dependencies
```
(The "test_" prefix is optional, and the ".py" extension is also optional)

### 5. `diagnose_errors.bat`

Runs a comprehensive error diagnosis to identify issues with the Grok-VIS installation.

**Usage:**
```
diagnose_errors.bat
```

**Purpose:**
Provides detailed information about the system, dependencies, and potential issues to help diagnose and fix problems.

## Running Tests

### Running All Tests

To run all tests:

1. Open a command prompt
2. Navigate to the Grok-VIS project directory
3. Run the batch file:
   ```
   run_tests.bat
   ```

### Running Specific Tests

To run a specific test file:

1. Open a command prompt
2. Navigate to the Grok-VIS project directory
3. Run the batch file with the test name:
   ```
   run_specific_test.bat test_core
   ```

### Checking Dependencies

To check if all dependencies are installed:

1. Open a command prompt
2. Navigate to the Grok-VIS project directory
3. Run the batch file:
   ```
   check_dependencies.bat
   ```

### Installing Dependencies

To install all required dependencies:

1. Open a command prompt
2. Navigate to the Grok-VIS project directory
3. Run the batch file:
   ```
   install_dependencies.bat
   ```

## Troubleshooting

If you encounter issues with the tests:

1. **Run Error Diagnosis**: Run `diagnose_errors.bat` to get a comprehensive analysis of your Grok-VIS installation
2. **Missing Dependencies**: Run `install_dependencies.bat` to install all required dependencies
3. **Python Path Issues**: Ensure that the correct Python environment is activated
4. **spaCy Model Missing**: Run `python -m spacy download en_core_web_sm` to install the required language model
5. **Test Failures**: Check the error messages for specific issues and fix them accordingly
6. **Check Error Logs**: Review the `grokvis_errors.log` and `error_diagnosis.log` files for detailed error information

## Adding New Tests

To add a new test file:

1. Create a new Python file in the tests directory with a name starting with "test_"
2. Import the unittest module and any required modules
3. Create a test class that inherits from unittest.TestCase
4. Add test methods that start with "test_"
5. Run the tests using the provided batch files

Example:
```python
import unittest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestNewFeature(unittest.TestCase):
    def test_new_functionality(self):
        # Test code here
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
```