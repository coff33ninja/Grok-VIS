"""
Home automation functionality for GrokVIS.
Handles controlling smart devices and PC wake-on-LAN.
"""
import logging
import wakeonlan
import socket

# Import from core module
from grokvis.speech import speak

def wake_pc(mac_address="YOUR_PC_MAC"):
    """Wake a PC using Wake-on-LAN."""
    try:
        wakeonlan.send_magic_packet(mac_address)
        speak("PC waking up. Don't fry it.")
    except Exception as e:
        logging.error(f"Wake-on-LAN Error: {e}")
        speak("Sorry, I couldn't wake the PC.")

def control_device(device, action):
    """Simulate controlling a smart device."""
    try:
        speak(f"{action}ing the {device}. Need more?")
    except Exception as e:
        logging.error(f"Device Control Error: {e}")
        speak("Sorry, I couldn't control the device.")

def check_device_status(device):
    """Check if a device is online by attempting to connect to its IP."""
    try:
        # This is a placeholder - in a real implementation, you would use the device's actual IP
        device_ip = {
            "tv": "192.168.1.100",
            "lights": "192.168.1.101",
            "thermostat": "192.168.1.102"
        }.get(device.lower(), None)
        
        if not device_ip:
            speak(f"I don't know the IP address for {device}.")
            return False
            
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((device_ip, 80))
        sock.close()
        
        if result == 0:
            speak(f"The {device} is online and responding.")
            return True
        else:
            speak(f"The {device} appears to be offline.")
            return False
    except Exception as e:
        logging.error(f"Device Status Check Error: {e}")
        speak(f"Sorry, I couldn't check the status of {device}.")
        return False