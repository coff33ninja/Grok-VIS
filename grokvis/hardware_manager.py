"""Hardware detection and management module.
Detects available hardware (NVIDIA, Intel, AMD) and configures the application accordingly.
"""

import os
import logging
import platform
import subprocess
from typing import Dict, Optional, Tuple, List

# Configure logging
logger = logging.getLogger(__name__)

class HardwareManager:
    """Manages hardware detection and configuration for optimal performance."""
    
    def __init__(self):
        """Initialize the hardware manager."""
        self.hardware_info = {
            "platform": platform.system(),
            "cpu": {
                "vendor": None,
                "model": None,
                "cores": None,
                "threads": None
            },
            "gpu": {
                "available": False,
                "vendor": None,
                "model": None,
                "vram": None
            }
        }
        self.detect_hardware()
        
    def detect_hardware(self) -> Dict:
        """Detect available hardware and update hardware_info."""
        self._detect_cpu()
        self._detect_gpu()
        logger.info(f"Hardware detection complete: {self.get_summary()}")
        return self.hardware_info
    
    def _detect_cpu(self) -> None:
        """Detect CPU information."""
        try:
            import cpuinfo
            info = cpuinfo.get_cpu_info()
            
            # Extract CPU vendor (Intel, AMD, etc.)
            brand = info.get('brand_raw', '')
            if 'intel' in brand.lower():
                self.hardware_info['cpu']['vendor'] = 'Intel'
            elif 'amd' in brand.lower():
                self.hardware_info['cpu']['vendor'] = 'AMD'
            else:
                self.hardware_info['cpu']['vendor'] = 'Unknown'
                
            self.hardware_info['cpu']['model'] = brand
            self.hardware_info['cpu']['cores'] = info.get('count', 0)
            self.hardware_info['cpu']['threads'] = os.cpu_count()
            
        except ImportError:
            logger.warning("cpuinfo module not available, using platform module for basic CPU info")
            self._detect_cpu_fallback()
    
    def _detect_cpu_fallback(self) -> None:
        """Fallback method for CPU detection using platform module."""
        try:
            import platform
            
            # Basic platform detection
            processor = platform.processor()
            if 'intel' in processor.lower():
                self.hardware_info['cpu']['vendor'] = 'Intel'
            elif 'amd' in processor.lower():
                self.hardware_info['cpu']['vendor'] = 'AMD'
            else:
                self.hardware_info['cpu']['vendor'] = 'Unknown'
                
            self.hardware_info['cpu']['model'] = processor
            self.hardware_info['cpu']['threads'] = os.cpu_count()
            self.hardware_info['cpu']['cores'] = os.cpu_count() // 2 if os.cpu_count() else None
            
        except Exception as e:
            logger.error(f"Error in CPU fallback detection: {e}")
            self.hardware_info['cpu']['vendor'] = 'Unknown'
    
    def _detect_gpu(self) -> None:
        """Detect GPU information with fallbacks for different vendors."""
        # Try NVIDIA first (using pynvml)
        if self._detect_nvidia_gpu():
            return
            
        # Try AMD GPU detection
        if self._detect_amd_gpu():
            return
            
        # Try Intel GPU detection
        if self._detect_intel_gpu():
            return
            
        # If no specific GPU detected, try generic detection
        self._detect_gpu_fallback()
    
    def _detect_nvidia_gpu(self) -> bool:
        """Detect NVIDIA GPU using pynvml."""
        try:
            import pynvml
            pynvml.nvmlInit()
            
            # Get the number of NVIDIA devices
            device_count = pynvml.nvmlDeviceGetCount()
            
            if device_count > 0:
                # Get the first device (can be extended to handle multiple GPUs)
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                name = pynvml.nvmlDeviceGetName(handle)
                memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                
                self.hardware_info['gpu']['available'] = True
                self.hardware_info['gpu']['vendor'] = 'NVIDIA'
                self.hardware_info['gpu']['model'] = name
                self.hardware_info['gpu']['vram'] = memory_info.total / (1024 ** 3)  # Convert to GB
                
                pynvml.nvmlShutdown()
                return True
                
        except (ImportError, Exception) as e:
            logger.debug(f"NVIDIA GPU detection failed: {e}")
            
        return False
    
    def _detect_amd_gpu(self) -> bool:
        """Detect AMD GPU."""
        # For Windows, try using Windows Management Instrumentation (WMI)
        if platform.system() == 'Windows':
            try:
                import wmi
                w = wmi.WMI()
                for gpu in w.Win32_VideoController():
                    if 'amd' in gpu.Name.lower() or 'radeon' in gpu.Name.lower():
                        self.hardware_info['gpu']['available'] = True
                        self.hardware_info['gpu']['vendor'] = 'AMD'
                        self.hardware_info['gpu']['model'] = gpu.Name
                        # WMI doesn't provide VRAM info directly
                        self.hardware_info['gpu']['vram'] = None
                        return True
            except ImportError:
                logger.debug("WMI module not available for AMD GPU detection on Windows")
        
        # For Linux, try using lspci
        elif platform.system() == 'Linux':
            try:
                output = subprocess.check_output(['lspci'], text=True)
                for line in output.splitlines():
                    if 'amd' in line.lower() or 'radeon' in line.lower() or 'advanced micro devices' in line.lower():
                        if 'vga' in line.lower() or 'display' in line.lower() or '3d' in line.lower():
                            self.hardware_info['gpu']['available'] = True
                            self.hardware_info['gpu']['vendor'] = 'AMD'
                            self.hardware_info['gpu']['model'] = line.split(':')[-1].strip()
                            self.hardware_info['gpu']['vram'] = None
                            return True
            except (subprocess.SubprocessError, Exception) as e:
                logger.debug(f"Error detecting AMD GPU on Linux: {e}")
                
        return False
    
    def _detect_intel_gpu(self) -> bool:
        """Detect Intel integrated GPU."""
        # For Windows, try using WMI
        if platform.system() == 'Windows':
            try:
                import wmi
                w = wmi.WMI()
                for gpu in w.Win32_VideoController():
                    if 'intel' in gpu.Name.lower() and ('hd graphics' in gpu.Name.lower() or 'uhd graphics' in gpu.Name.lower() or 'iris' in gpu.Name.lower()):
                        self.hardware_info['gpu']['available'] = True
                        self.hardware_info['gpu']['vendor'] = 'Intel'
                        self.hardware_info['gpu']['model'] = gpu.Name
                        self.hardware_info['gpu']['vram'] = None
                        return True
            except ImportError:
                logger.debug("WMI module not available for Intel GPU detection on Windows")
        
        # For Linux, try using lspci
        elif platform.system() == 'Linux':
            try:
                output = subprocess.check_output(['lspci'], text=True)
                for line in output.splitlines():
                    if 'intel' in line.lower() and ('vga' in line.lower() or 'display' in line.lower()):
                        self.hardware_info['gpu']['available'] = True
                        self.hardware_info['gpu']['vendor'] = 'Intel'
                        self.hardware_info['gpu']['model'] = line.split(':')[-1].strip()
                        self.hardware_info['gpu']['vram'] = None
                        return True
            except (subprocess.SubprocessError, Exception) as e:
                logger.debug(f"Error detecting Intel GPU on Linux: {e}")
                
        return False
    
    def _detect_gpu_fallback(self) -> None:
        """Generic GPU detection fallback."""
        # For Windows, try using WMI for any GPU
        if platform.system() == 'Windows':
            try:
                import wmi
                w = wmi.WMI()
                for gpu in w.Win32_VideoController():
                    self.hardware_info['gpu']['available'] = True
                    self.hardware_info['gpu']['vendor'] = 'Unknown'
                    self.hardware_info['gpu']['model'] = gpu.Name
                    self.hardware_info['gpu']['vram'] = None
                    return
            except ImportError:
                logger.debug("WMI module not available for generic GPU detection")
        
        # For Linux, try using lspci for any GPU
        elif platform.system() == 'Linux':
            try:
                output = subprocess.check_output(['lspci'], text=True)
                for line in output.splitlines():
                    if 'vga' in line.lower() or 'display' in line.lower() or '3d' in line.lower():
                        self.hardware_info['gpu']['available'] = True
                        self.hardware_info['gpu']['vendor'] = 'Unknown'
                        self.hardware_info['gpu']['model'] = line.split(':')[-1].strip()
                        self.hardware_info['gpu']['vram'] = None
                        return
            except (subprocess.SubprocessError, Exception) as e:
                logger.debug(f"Error in generic GPU detection on Linux: {e}")
        
        # If we get here, no GPU was detected
        self.hardware_info['gpu']['available'] = False
        self.hardware_info['gpu']['vendor'] = None
        self.hardware_info['gpu']['model'] = None
        self.hardware_info['gpu']['vram'] = None
    
    def get_optimal_device(self) -> str:
        """
        Determine the optimal device for AI operations.
        
        Returns:
            str: 'cuda' for NVIDIA GPU, 'mps' for Apple Silicon, 'directml' for AMD/Intel on Windows, or 'cpu' as fallback
        """
        # Check for NVIDIA GPU first (CUDA)
        if self.hardware_info['gpu']['vendor'] == 'NVIDIA':
            try:
                import torch
                if torch.cuda.is_available():
                    return 'cuda'
            except ImportError:
                logger.debug("PyTorch not available to check CUDA support")
        
        # Check for Apple Silicon (MPS)
        if platform.system() == 'Darwin' and platform.processor() == 'arm':
            try:
                import torch
                if torch.backends.mps.is_available():
                    return 'mps'
            except (ImportError, AttributeError):
                logger.debug("PyTorch MPS support not available")
        
        # Check for DirectML support (AMD/Intel on Windows)
        if platform.system() == 'Windows' and self.hardware_info['gpu']['available']:
            try:
                import torch_directml
                return 'directml'
            except ImportError:
                logger.debug("torch_directml not available")
        
        # Fallback to CPU
        return 'cpu'
    
    def get_tts_config(self) -> Dict:
        """
        Get optimal TTS configuration based on available hardware.
        
        Returns:
            Dict: Configuration dictionary for TTS
        """
        device = self.get_optimal_device()
        
        # Base configuration
        config = {
            'model_name': "tts_models/en/ljspeech/tacotron2-DDC",
            'progress_bar': False,
            'gpu': False
        }
        
        # Adjust based on detected hardware
        if device == 'cuda':
            # NVIDIA GPU available
            config['gpu'] = True
            # For high-end GPUs, we could use more complex models
            if self.hardware_info['gpu']['vram'] and self.hardware_info['gpu']['vram'] > 6:
                config['model_name'] = "tts_models/en/ljspeech/glow-tts"
        
        elif device == 'mps':
            # Apple Silicon
            config['gpu'] = True
        
        elif device == 'directml':
            # AMD/Intel GPU with DirectML
            config['gpu'] = True
            # DirectML might need special handling
            os.environ['PYTORCH_DIRECTML_BACKEND'] = '1'
        
        # For CPU, we stick with the base config (lightweight model)
        
        return config
    
    def get_summary(self) -> str:
        """Get a human-readable summary of detected hardware."""
        cpu_info = self.hardware_info['cpu']
        gpu_info = self.hardware_info['gpu']
        
        summary = f"Platform: {self.hardware_info['platform']}\n"
        summary += f"CPU: {cpu_info['vendor']} {cpu_info['model']} ({cpu_info['cores']} cores, {cpu_info['threads']} threads)\n"
        
        if gpu_info['available']:
            summary += f"GPU: {gpu_info['vendor']} {gpu_info['model']}"
            if gpu_info['vram']:
                summary += f" ({gpu_info['vram']:.2f} GB VRAM)"
        else:
            summary += "GPU: Not detected"
            
        summary += f"\nOptimal device: {self.get_optimal_device()}"
        
        return summary

# Create a singleton instance
_hardware_manager = None

def get_hardware_manager():
    """Get or create the hardware manager singleton."""
    global _hardware_manager
    if _hardware_manager is None:
        _hardware_manager = HardwareManager()
    return _hardware_manager