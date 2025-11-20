"""
Dotfiles Management System

A cross-platform dotfiles manager with device detection and automated installation.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .device_detector import DeviceDetector
from .backup import BackupManager
from .config_manager import ConfigManager
from .tool_installer import ToolInstaller
from .installer import DotfilesInstaller

__all__ = [
    "DeviceDetector",
    "BackupManager",
    "ConfigManager",
    "ToolInstaller",
    "DotfilesInstaller",
]
