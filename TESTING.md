# Grok-VIS Testing Documentation

This document provides detailed information about the testing framework for the Grok-VIS project, including how to run tests, add new tests, and troubleshoot common issues.

## Table of Contents

1. [Testing Framework Overview](#testing-framework-overview)
2. [Test Files](#test-files)
3. [Batch Files](#batch-files)
4. [Running Tests](#running-tests)
5. [Error Handling and Diagnosis](#error-handling-and-diagnosis)
6. [Troubleshooting](#troubleshooting)
7. [Adding New Tests](#adding-new-tests)
8. [Continuous Integration](#continuous-integration)

## Testing Framework Overview

The Grok-VIS testing framework is designed to ensure that all components of the system work correctly and that all dependencies are properly installed. The framework consists of:

- **Unit Tests**: Test individual components and functions
- **Dependency Tests**: Verify that all required packages are installed
- **Integration Tests**: Test the interaction between different components

The tests are organized in the `tests` directory and can be run individually or all at once using the provided batch files.

## Test Files

### Core Tests (`test_core.py`)

Tests the core functionality of the Grok-VIS system.

**Test Cases:**
- `test_imports`: Verifies that the main Grok-VIS package can be imported
- `test_module_structure`: Checks that the module structure is correct and all essential modules can be imported

**Purpose:**  
Ensures that the basic structure of the Grok-VIS project is intact and that the core modules are accessible.

### Dependency Tests (`test_dependencies.py`)

Verifies that all required dependencies are installed and accessible.

**Test Cases:**
- `test_required_packages`: Checks if all packages listed in requirements.txt can be imported
- `test_spacy_model`: Verifies that the spaCy English language model is installed and can be loaded

**Purpose:**  
Identifies missing or incorrectly installed dependencies that might cause runtime errors.

### Speech Tests (`test_speech.py`)

Tests the speech functionality components of Grok-VIS.

**Test Cases:**
- `test_speech_module_import`: Verifies that the speech module can be imported
- `test_tts_initialization`: Checks if the Text-to-Speech system can be initialized

**Purpose:**  
Ensures that the speech recognition and synthesis components are properly set up.

### Error Handling Tests (`test_errors.py`)

Tests the error handling capabilities of Grok-VIS.

**Test Cases:**
- `test_logging_setup`: Verifies that logging is set up correctly
- `test_error_logging`: Checks if errors are properly logged
- `test_exception_handling`: Tests that exceptions are properly handled
- `test_missing_dependency_error`: Tests how the system handles missing dependencies

**Purpose:**  
Ensures that the system can properly handle and log errors, making it easier to diagnose and fix issues.

## Batch Files

### `run_tests.bat`

Runs all tests in the tests directory.

**Usage:**
```
run_tests.bat
```

**What it does:**
1. Checks if Python is available in the PATH
2. Runs all tests using the `run_tests.py` script
3. Displays the test results

### `check_dependencies.bat`

Checks if all required dependencies are installed.

**Usage:**
```
check_dependencies.bat
```

**What it does:**
1. Checks if Python is available in the PATH
2. Iterates through a list of required dependencies
3. Uses the `check_dependency.py` script to check each dependency
4. Displays a summary of missing dependencies

### `install_dependencies.bat`

Installs all required dependencies from requirements.txt.

**Usage:**
```
install_dependencies.bat
```

**What it does:**
1. Checks if Python is available in the PATH
2. Installs all dependencies listed in requirements.txt
3. Installs the spaCy English language model
4. Runs the dependency check to verify that all dependencies are installed

### `run_specific_test.bat`

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

**What it does:**
1. Checks if Python is available in the PATH
2. Runs the specified test file
3. Displays the test results

### `diagnose_errors.bat`

Runs a comprehensive error diagnosis to identify issues with the Grok-VIS installation.

**Usage:**
```
diagnose_errors.bat
```

**What it does:**
1. Checks if Python is available in the PATH
2. Runs the error diagnosis script
3. Displays detailed information about the system, dependencies, and potential issues
4. Creates a log file with the diagnosis results

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

### Diagnosing Errors

To run a comprehensive error diagnosis:

1. Open a command prompt
2. Navigate to the Grok-VIS project directory
3. Run the batch file:
   ```
   diagnose_errors.bat
   ```
4. Review the output and the error_diagnosis.log file for detailed information

## Error Handling and Diagnosis

Grok-VIS includes a comprehensive error handling and diagnosis system to help identify and fix issues.

### Error Handling

The error handling system in Grok-VIS is designed to:

1. **Catch and Log Errors**: All errors are caught and logged to the `grokvis_errors.log` file
2. **Provide Helpful Error Messages**: Error messages include detailed information about what went wrong
3. **Gracefully Handle Exceptions**: The system can recover from many types of errors without crashing

### Error Diagnosis

The error diagnosis system helps identify issues with the Grok-VIS installation:

1. **System Information**: Checks the operating system, Python version, and hardware
2. **Dependency Verification**: Ensures all required packages are installed
3. **File Permissions**: Verifies that all necessary files are readable and writable
4. **Import Testing**: Tests that all Grok-VIS modules can be imported
5. **Log File Checking**: Ensures that log files can be created and written to

### Using the Error Diagnosis Tool

The `error_diagnosis.py` script provides a comprehensive analysis of your Grok-VIS installation:

```
python tests/error_diagnosis.py
```

Or use the batch file:

```
diagnose_errors.bat
```

The script will:
1. Check your Python version
2. Display system information
3. Verify all dependencies
4. Check the spaCy model
5. Test Grok-VIS imports
6. Check file permissions
7. Verify log files
8. Provide a summary of any issues found

### Error Logs

Grok-VIS logs errors to the following files:

- `grokvis_errors.log`: Contains errors from the main application
- `error_diagnosis.log`: Contains detailed information from the error diagnosis tool

These logs can be helpful when troubleshooting issues.

## Troubleshooting

### Common Issues

#### Missing Dependencies

**Symptoms:**
- Tests fail with `ImportError` or `ModuleNotFoundError`
- The application crashes when trying to import a module

**Solution:**
1. Run `diagnose_errors.bat` to identify the specific missing dependencies
2. Run `install_dependencies.bat` to install all required dependencies
3. If specific dependencies still fail to install, try installing them manually:
   ```
   pip install <package_name>
   ```

#### Python Path Issues

**Symptoms:**
- Tests fail even though dependencies are installed
- The application cannot find modules that are installed

**Solution:**
1. Ensure that the correct Python environment is activated
2. Check the Python path:
   ```
   python -c "import sys; print(sys.path)"
   ```
3. Make sure the project directory is in the Python path

#### spaCy Model Missing

**Symptoms:**
- Tests fail with an error about the spaCy model
- The application crashes when trying to load the spaCy model

**Solution:**
1. Install the spaCy English language model:
   ```
   python -m spacy download en_core_web_sm
   ```
2. If that doesn't work, try installing it directly from the GitHub repository:
   ```
   pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
   ```

#### Test Failures

**Symptoms:**
- Tests fail with specific error messages
- The application works but tests don't pass

**Solution:**
1. Check the error messages for specific issues
2. Fix the issues in the code
3. Run the tests again to verify that the issues are fixed

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

### Best Practices for Writing Tests

1. **Test One Thing at a Time**: Each test method should test one specific aspect of the code
2. **Use Descriptive Names**: Test method names should describe what they're testing
3. **Use Setup and Teardown**: Use the `setUp` and `tearDown` methods to set up and clean up test fixtures
4. **Test Edge Cases**: Test boundary conditions and edge cases
5. **Keep Tests Independent**: Tests should not depend on each other
6. **Use Assertions**: Use the appropriate assertion methods for the type of test

## Continuous Integration

The Grok-VIS project does not currently have continuous integration set up, but it could be added in the future. Here's how it could be implemented:

1. **GitHub Actions**: Set up a GitHub Actions workflow to run tests on every push and pull request
2. **Travis CI**: Configure Travis CI to run tests on multiple Python versions
3. **Jenkins**: Set up a Jenkins pipeline to run tests and deploy the application

Example GitHub Actions workflow:
```yaml
name: Run Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        python -m spacy download en_core_web_sm
    - name: Run tests
      run: |
        python tests/run_tests.py
```

## Conclusion

The Grok-VIS testing framework provides a comprehensive way to ensure that the application works correctly and that all dependencies are properly installed. By following the instructions in this document, you can run tests, troubleshoot issues, and add new tests to the framework.