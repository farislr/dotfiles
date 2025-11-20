"""Tool installation management for different package managers."""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Dict
import requests


class ToolInstaller:
    """Handles installation of tools across different package managers."""
    
    def __init__(self, package_manager: str, os_type: str):
        self.package_manager = package_manager
        self.os_type = os_type
        self.dotfiles_root = Path(__file__).parent.parent
    
    def run_command(self, command: List[str], check: bool = True) -> tuple[bool, str]:
        """
        Run a shell command and return success status and output.
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr
    
    def install_package(self, package: str) -> bool:
        """Install a single package using the system package manager."""
        print(f"Installing {package}...")
        
        if self.package_manager == "brew":
            success, output = self.run_command(["brew", "install", package])
        
        elif self.package_manager == "apt":
            success, output = self.run_command(
                ["sudo", "apt", "install", "-y", package]
            )
        
        elif self.package_manager == "pacman":
            success, output = self.run_command(
                ["sudo", "pacman", "-S", "--noconfirm", package]
            )
        
        else:
            print(f"Unsupported package manager: {self.package_manager}")
            return False
        
        if success:
            print(f"✓ Installed: {package}")
        else:
            print(f"✗ Failed to install {package}: {output}")
        
        return success
    
    def install_packages(self, packages: List[str]) -> Dict[str, bool]:
        """Install multiple packages."""
        results = {}
        
        for package in packages:
            results[package] = self.install_package(package)
        
        return results
    
    def install_oh_my_zsh(self) -> bool:
        """Install Oh My Zsh."""
        oh_my_zsh_dir = Path.home() / ".oh-my-zsh"
        
        if oh_my_zsh_dir.exists():
            print("Oh My Zsh already installed")
            return True
        
        print("Installing Oh My Zsh...")
        
        # Download and run the installer
        install_script = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
        
        try:
            success, output = self.run_command([
                "sh", "-c",
                f'RUNZSH=no CHSH=no sh -c "$(curl -fsSL {install_script})"'
            ])
            
            if success:
                print("✓ Oh My Zsh installed")
            return success
        
        except Exception as e:
            print(f"✗ Failed to install Oh My Zsh: {e}")
            return False
    
    def install_oh_my_posh(self) -> bool:
        """Install Oh My Posh."""
        print("Installing Oh My Posh...")
        
        if self.package_manager == "brew":
            return self.install_package("oh-my-posh")
        
        elif self.package_manager in ["apt", "pacman"]:
            # Install via binary
            try:
                install_cmd = "curl -s https://ohmyposh.dev/install.sh | bash -s"
                success, output = self.run_command(["sh", "-c", install_cmd])
                
                if success:
                    print("✓ Oh My Posh installed")
                return success
            
            except Exception as e:
                print(f"✗ Failed to install Oh My Posh: {e}")
                return False
        
        return False
    
    def install_zsh_plugin(self, plugin: str) -> bool:
        """Install a zsh plugin for Oh My Zsh."""
        custom_plugins = Path.home() / ".oh-my-zsh/custom/plugins"
        
        # Map plugin names to their Git URLs
        plugin_urls = {
            "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions",
            "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting",
            "powerlevel10k": "https://github.com/romkatv/powerlevel10k"
        }
        
        if plugin not in plugin_urls:
            print(f"Unknown plugin: {plugin}")
            return False
        
        # Special handling for powerlevel10k (theme)
        if plugin == "powerlevel10k":
            target_dir = Path.home() / ".oh-my-zsh/custom/themes/powerlevel10k"
        else:
            target_dir = custom_plugins / plugin
        
        if target_dir.exists():
            print(f"Plugin {plugin} already installed")
            return True
        
        print(f"Installing {plugin}...")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
        success, output = self.run_command([
            "git", "clone", "--depth=1",
            plugin_urls[plugin],
            str(target_dir)
        ])
        
        if success:
            print(f"✓ Installed plugin: {plugin}")
        else:
            print(f"✗ Failed to install {plugin}: {output}")
        
        return success
    
    def install_opencode(self) -> bool:
        """
        Install OpenCode.
        Currently provides instructions as automatic download isn't reliable.
        """
        print("\n" + "=" * 60)
        print("OpenCode Installation")
        print("=" * 60)
        print("OpenCode needs to be installed manually:")
        print("1. Visit: https://opencode.ai")
        print("2. Download the appropriate version for your OS")
        print("3. Install the application")
        print("4. After installation, your OpenCode configs will be symlinked")
        print("=" * 60 + "\n")
        
        response = input("Have you installed OpenCode? (y/n): ").lower()
        return response == "y"
    
    def setup_neovim_lazyvim(self, config_source: Path) -> bool:
        """
        Setup LazyVim by copying configs to nvim config directory.
        """
        nvim_config = Path.home() / ".config/nvim"
        
        print("Setting up LazyVim configuration...")
        
        # The config_manager will handle symlinking
        # This function is for any additional setup if needed
        
        print("✓ LazyVim configuration will be symlinked by config manager")
        print("  Note: First launch of nvim will install plugins automatically")
        
        return True


if __name__ == "__main__":
    # Test tool installer
    from device_detector import DeviceDetector
    
    detector = DeviceDetector()
    installer = ToolInstaller(
        detector.package_manager,
        detector.os_type
    )
    
    print(f"Package Manager: {installer.package_manager}")
    print(f"OS: {installer.os_type}")
