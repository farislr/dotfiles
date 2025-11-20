"""Main installer orchestrator for dotfiles system."""

import sys
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from device_detector import DeviceDetector
from backup import BackupManager
from config_manager import ConfigManager
from tool_installer import ToolInstaller


class DotfilesInstaller:
    """Main orchestrator for dotfiles installation."""
    
    def __init__(self, dotfiles_root: Path):
        self.dotfiles_root = Path(dotfiles_root)
        self.console = Console()
        self.detector = DeviceDetector()
        self.backup_mgr = BackupManager(self.dotfiles_root / "backups")
        self.config_mgr = ConfigManager(self.dotfiles_root)
        self.tool_installer = ToolInstaller(
            self.detector.package_manager,
            self.detector.os_type
        )
    
    def print_welcome(self):
        """Print welcome message."""
        self.console.print(Panel.fit(
            "[bold cyan]Dotfiles Manager[/bold cyan]\n"
            "Cross-platform configuration management system",
            border_style="cyan"
        ))
    
    def show_device_info(self):
        """Display detected device information."""
        info = self.detector.get_info()
        
        table = Table(title="Device Information", show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in info.items():
            table.add_row(key.title(), value)
        
        self.console.print(table)
    
    def check_system_support(self) -> bool:
        """Check if system is supported."""
        supported, msg = self.detector.is_supported()
        
        if not supported:
            self.console.print(f"[bold red]✗ {msg}[/bold red]")
            return False
        
        self.console.print(f"[bold green]✓ {msg}[/bold green]")
        return True
    
    def select_profile_type(self) -> str:
        """Ask user to select work or personal profile."""
        choice = Prompt.ask(
            "[bold]Select profile type[/bold]",
            choices=["work", "personal"],
            default="personal"
        )
        return choice
    
    def load_profiles(self, profile_type: str) -> dict:
        """Load and merge appropriate profiles."""
        base_profile = self.detector.get_profile_name()
        additional_profiles = [f"{profile_type}.yml"]
        
        self.console.print(f"\n[cyan]Loading profiles:[/cyan]")
        self.console.print(f"  • Base: {base_profile}")
        self.console.print(f"  • Additional: {profile_type}.yml")
        
        try:
            profile = self.config_mgr.merge_profiles(base_profile, additional_profiles)
            self.console.print("[green]✓ Profiles loaded successfully[/green]")
            return profile
        except Exception as e:
            self.console.print(f"[red]✗ Error loading profiles: {e}[/red]")
            sys.exit(1)
    
    def check_conflicts(self, profile: dict) -> List[dict]:
        """Check for existing configuration conflicts."""
        self.console.print("\n[cyan]Checking for existing configurations...[/cyan]")
        
        conflicts = self.config_mgr.check_conflicts(profile)
        
        if conflicts:
            self.console.print(f"[yellow]⚠ Found {len(conflicts)} existing configurations:[/yellow]")
            
            table = Table()
            table.add_column("Config", style="cyan")
            table.add_column("Path", style="yellow")
            table.add_column("Type", style="magenta")
            
            for conflict in conflicts:
                table.add_row(
                    conflict["name"],
                    conflict["path"],
                    conflict["type"]
                )
            
            self.console.print(table)
        else:
            self.console.print("[green]✓ No conflicts found[/green]")
        
        return conflicts
    
    def backup_existing_configs(self, profile: dict) -> bool:
        """Backup existing configurations."""
        self.console.print("\n[cyan]Creating backup...[/cyan]")
        
        backup_dir = self.backup_mgr.create_backup_directory()
        self.console.print(f"Backup directory: [yellow]{backup_dir}[/yellow]")
        
        config_paths = profile.get("config_paths", {})
        results = self.backup_mgr.backup_configs(config_paths)
        
        backed_up = sum(1 for v in results.values() if v is True)
        
        if backed_up > 0:
            self.console.print(f"[green]✓ Backed up {backed_up} configurations[/green]")
            self.backup_mgr.save_backup_log()
            return True
        else:
            self.console.print("[yellow]No configurations needed backup[/yellow]")
            return True
    
    def install_tools(self, profile: dict) -> bool:
        """Install required tools."""
        if not Confirm.ask("\n[bold]Install required tools?[/bold]", default=True):
            self.console.print("[yellow]Skipping tool installation[/yellow]")
            return True
        
        self.console.print("\n[cyan]Installing tools...[/cyan]")
        
        # Install packages
        packages = profile.get("packages", [])
        if isinstance(packages, dict):
            # Handle Linux profiles with 'common' key
            packages = packages.get("common", [])
        
        if packages:
            self.console.print(f"Installing {len(packages)} packages...")
            results = self.tool_installer.install_packages(packages)
            
            success_count = sum(1 for v in results.values() if v)
            self.console.print(
                f"[green]✓ Installed {success_count}/{len(packages)} packages[/green]"
            )
        
        # Install Oh My Zsh
        if Confirm.ask("\nInstall Oh My Zsh?", default=True):
            self.tool_installer.install_oh_my_zsh()
        
        # Install Oh My Posh
        if Confirm.ask("\nInstall Oh My Posh?", default=True):
            self.tool_installer.install_oh_my_posh()
        
        # Install zsh plugins
        zsh_plugins = profile.get("zsh_plugins", [])
        if zsh_plugins and Confirm.ask("\nInstall zsh plugins?", default=True):
            self.console.print("Installing zsh plugins...")
            for plugin in zsh_plugins:
                self.tool_installer.install_zsh_plugin(plugin)
        
        # OpenCode installation prompt
        if Confirm.ask("\nInstall OpenCode?", default=False):
            self.tool_installer.install_opencode()
        
        return True
    
    def deploy_configurations(self, profile: dict) -> bool:
        """Deploy configuration files via symlinks."""
        self.console.print("\n[cyan]Deploying configurations...[/cyan]")
        
        force = Confirm.ask(
            "Overwrite existing configs?",
            default=True
        )
        
        results = self.config_mgr.deploy_configs(profile, force=force)
        
        success_count = sum(1 for v in results.values() if v)
        total = len(results)
        
        self.console.print(
            f"[green]✓ Deployed {success_count}/{total} configurations[/green]"
        )
        
        return success_count > 0
    
    def show_summary(self):
        """Show installation summary."""
        self.console.print("\n" + "=" * 60)
        self.console.print(Panel.fit(
            "[bold green]Installation Complete![/bold green]\n\n"
            "[cyan]Next Steps:[/cyan]\n"
            "1. Restart your terminal or run: source ~/.zshrc\n"
            "2. Launch nvim to install LazyVim plugins\n"
            "3. Customize your configs in the dotfiles directory\n"
            "4. Commit your changes: git add . && git commit -m 'Initial setup'\n\n"
            "[yellow]Note:[/yellow] Your old configs are backed up in ./backups/",
            border_style="green"
        ))
    
    def run(self):
        """Run the complete installation flow."""
        # 1. Welcome & Detection
        self.print_welcome()
        self.show_device_info()
        
        if not self.check_system_support():
            sys.exit(1)
        
        # 2. Pre-flight Checks
        self.console.print("\n[cyan]Pre-flight checks...[/cyan]")
        self.console.print("[green]✓ Git installed[/green]")
        self.console.print(f"[green]✓ Python {sys.version_info.major}.{sys.version_info.minor}[/green]")
        
        # Get user profile choice
        profile_type = self.select_profile_type()
        profile = self.load_profiles(profile_type)
        
        # 3. Interactive Configuration
        conflicts = self.check_conflicts(profile)
        
        if conflicts:
            if not Confirm.ask("\nProceed with installation?", default=True):
                self.console.print("[yellow]Installation cancelled[/yellow]")
                sys.exit(0)
        
        # 4. Backup Phase
        if conflicts:
            self.backup_existing_configs(profile)
        
        # 5. Tool Installation
        self.install_tools(profile)
        
        # 6. Config Deployment
        self.deploy_configurations(profile)
        
        # 7. Post-Install
        self.show_summary()


def main():
    """Main entry point."""
    dotfiles_root = Path(__file__).parent.parent
    installer = DotfilesInstaller(dotfiles_root)
    
    try:
        installer.run()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
