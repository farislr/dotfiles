"""Device detection module for identifying OS, distro, and architecture."""

import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


class DeviceDetector:
    """Detects system information for configuration selection."""
    
    def __init__(self):
        self.os_type = self._detect_os()
        self.architecture = self._detect_architecture()
        self.distro = self._detect_distro() if self.os_type == "linux" else None
        self.package_manager = self._detect_package_manager()
        self.hostname = platform.node()
    
    def _detect_os(self) -> str:
        """Detect operating system."""
        system = platform.system().lower()
        if system == "darwin":
            return "macos"
        elif system == "linux":
            return "linux"
        else:
            raise RuntimeError(f"Unsupported OS: {system}")
    
    def _detect_architecture(self) -> str:
        """Detect system architecture."""
        machine = platform.machine().lower()
        if machine in ["x86_64", "amd64"]:
            return "x86_64"
        elif machine in ["arm64", "aarch64"]:
            return "arm64"
        else:
            return machine
    
    def _detect_distro(self) -> Optional[str]:
        """Detect Linux distribution."""
        if self.os_type != "linux":
            return None
        
        try:
            # Try reading /etc/os-release
            if Path("/etc/os-release").exists():
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("ID="):
                            distro = line.split("=")[1].strip().strip('"')
                            # Normalize distro names
                            if distro in ["ubuntu", "debian", "pop"]:
                                return "ubuntu"
                            elif distro in ["arch", "manjaro", "endeavouros"]:
                                return "arch"
            
            # Fallback: check for specific files
            if Path("/etc/arch-release").exists():
                return "arch"
            elif Path("/etc/debian_version").exists():
                return "ubuntu"
        except Exception as e:
            print(f"Warning: Could not detect distro: {e}")
        
        return None
    
    def _detect_package_manager(self) -> Optional[str]:
        """Detect available package manager."""
        if self.os_type == "macos":
            if self._command_exists("brew"):
                return "brew"
            return None
        
        elif self.os_type == "linux":
            if self.distro == "ubuntu" and self._command_exists("apt"):
                return "apt"
            elif self.distro == "arch" and self._command_exists("pacman"):
                return "pacman"
        
        return None
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run(
                ["which", command],
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_info(self) -> Dict[str, str]:
        """Get all device information as dictionary."""
        return {
            "os": self.os_type,
            "architecture": self.architecture,
            "distro": self.distro or "N/A",
            "package_manager": self.package_manager or "None",
            "hostname": self.hostname,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
    
    def is_supported(self) -> tuple[bool, str]:
        """Check if the current system is supported."""
        if self.os_type not in ["macos", "linux"]:
            return False, f"Unsupported OS: {self.os_type}"
        
        if self.os_type == "linux" and self.distro not in ["ubuntu", "arch"]:
            return False, f"Unsupported Linux distro: {self.distro}"
        
        if self.architecture not in ["x86_64", "arm64"]:
            return False, f"Unsupported architecture: {self.architecture}"
        
        if not self.package_manager:
            return False, "No supported package manager found"
        
        return True, "System is supported"
    
    def get_profile_name(self) -> str:
        """Get the profile filename to load."""
        return f"{self.os_type}.yml"


if __name__ == "__main__":
    # Test the detector
    detector = DeviceDetector()
    print("Device Information:")
    for key, value in detector.get_info().items():
        print(f"  {key}: {value}")
    
    supported, msg = detector.is_supported()
    print(f"\nSupported: {supported}")
    print(f"Message: {msg}")
    print(f"Profile: {detector.get_profile_name()}")
