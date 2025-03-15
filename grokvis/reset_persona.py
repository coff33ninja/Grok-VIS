"""
Simple utility to reset the persona choice for GrokVIS.
Run this script to delete the persona_config.txt file and force GrokVIS to ask for a persona choice again.
"""
import os
import sys

def reset_persona():
    """Delete the persona_config.txt file if it exists."""
    if os.path.exists('persona_config.txt'):
        try:
            os.remove('persona_config.txt')
            print("Persona choice reset successfully. GrokVIS will ask for a persona choice on next run.")
        except Exception as e:
            print(f"Error resetting persona choice: {e}")
    else:
        print("No persona choice found. GrokVIS will ask for a persona choice on next run.")

if __name__ == "__main__":
    reset_persona()