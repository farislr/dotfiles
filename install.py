#!/usr/bin/env python3
"""
Dotfiles Installation Script

Usage:
    python3 install.py

This script will guide you through installing and configuring your dotfiles.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from installer import main

if __name__ == "__main__":
    main()
