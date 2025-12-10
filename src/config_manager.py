"""Configuration file management and symlinking."""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class ConfigManager:
    """Manages configuration file deployment and symlinking."""
    
    def __init__(self, dotfiles_root: Path):
        self.dotfiles_root = Path(dotfiles_root)
        self.configs_dir = self.dotfiles_root / "configs"
        self.profiles_dir = self.dotfiles_root / "profiles"
    
    def load_profile(self, profile_name: str) -> Dict:
        """Load a profile YAML file."""
        profile_path = self.profiles_dir / profile_name
        
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {profile_path}")
        
        with open(profile_path, "r") as f:
            return yaml.safe_load(f)
    
    def merge_profiles(self, base_profile: str, additional_profiles: List[str]) -> Dict:
        """
        Merge multiple profiles together.
        Later profiles override earlier ones.
        """
        merged = self.load_profile(base_profile)
        
        for profile_name in additional_profiles:
            try:
                additional = self.load_profile(profile_name)
                
                # Deep merge overrides
                if "overrides" in additional:
                    if "overrides" not in merged:
                        merged["overrides"] = {}
                    merged["overrides"].update(additional["overrides"])
                
                # Merge other fields
                for key, value in additional.items():
                    if key != "overrides":
                        if isinstance(value, dict) and key in merged:
                            merged[key].update(value)
                        else:
                            merged[key] = value
            
            except FileNotFoundError:
                print(f"Warning: Profile {profile_name} not found, skipping")
        
        return merged
    
    def create_symlink(self, source: Path, target: Path, force: bool = False) -> bool:
        """
        Create a symlink from source to target.
        
        Args:
            source: Path to the actual config file/directory
            target: Path where symlink should be created
            force: If True, remove existing target before creating symlink
        
        Returns:
            True if successful, False otherwise
        """
        try:
            target = Path(target).expanduser()
            source = source.resolve()
            
            # Check if source exists
            if not source.exists():
                print(f"Error: Source does not exist: {source}")
                return False
            
            # Handle existing target
            if target.exists() or target.is_symlink():
                if target.is_symlink() and target.resolve() == source:
                    print(f"Symlink already exists: {target} -> {source}")
                    return True
                
                if not force:
                    print(f"Error: Target already exists: {target}")
                    return False
                
                # Remove existing
                if target.is_symlink():
                    target.unlink()
                elif target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            
            # Create parent directory if needed
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Create symlink
            target.symlink_to(source)
            print(f"✓ Created symlink: {target} -> {source}")
            return True
        
        except Exception as e:
            print(f"Error creating symlink: {e}")
            return False
    
    def _is_file_path(self, source: Path) -> bool:
        """
        Determine if source should be treated as file or directory.

        Detection rules:
        1. If source exists: check if it's a file
        2. If doesn't exist: check if it has file extension
        3. Check for common dotfiles without extensions
        4. Fallback: treat as directory

        Args:
            source: Path to evaluate

        Returns:
            True if should be treated as file, False for directory
        """
        if source.exists():
            return source.is_file()

        # Check for common file patterns
        if source.suffix:  # Has extension like .zshrc, .gitconfig
            return True

        # Common dotfiles without extensions
        dotfile_names = {'.zshrc', '.zprofile', '.bashrc', '.bash_profile',
                        '.vimrc', '.tmux.conf', '.gitconfig', '.gitignore_global'}
        if source.name in dotfile_names:
            return True

        return False  # Default to directory

    def deploy_configs(self, profile: Dict, force: bool = False) -> Dict[str, bool]:
        """
        Deploy all configurations based on profile.
        Handles both directory and individual file symlinks.

        Args:
            profile: Loaded profile dictionary
            force: If True, overwrite existing configs

        Returns:
            Dict of config_name -> success status
        """
        config_paths = profile.get("config_paths", {})
        results = {}

        for config_name, target_path in config_paths.items():
            source = self.configs_dir / config_name

            if not source.exists():
                # Determine type for better error message
                is_file = self._is_file_path(source)
                item_type = "file" if is_file else "directory"
                print(f"Warning: Config {item_type} not found: {source}")
                results[config_name] = False
                continue

            success = self.create_symlink(source, target_path, force=force)
            results[config_name] = success

        return results
    
    def check_conflicts(self, profile: Dict) -> List[Dict[str, str]]:
        """
        Check for existing configs that would conflict.
        Distinguishes between file and directory conflicts.

        Returns:
            List of conflicts with details
        """
        conflicts = []
        config_paths = profile.get("config_paths", {})

        for config_name, target_path in config_paths.items():
            target = Path(target_path).expanduser()

            if target.exists() or target.is_symlink():
                # Check if it's already our symlink
                if target.is_symlink():
                    source = self.configs_dir / config_name
                    if source.exists() and target.resolve() == source.resolve():
                        continue  # Already linked correctly

                # Determine actual type based on what exists
                if target.is_symlink():
                    item_type = "symlink"
                elif target.is_dir():
                    item_type = "directory"
                else:
                    item_type = "file"

                conflicts.append({
                    "name": config_name,
                    "path": str(target),
                    "type": item_type,
                    "is_symlink": target.is_symlink()
                })

        return conflicts
    
    def apply_overrides(self, config_name: str, overrides: Dict) -> bool:
        """
        Apply profile-specific overrides to a config file.
        This is a placeholder - actual implementation depends on config format.
        """
        # TODO: Implement config-specific override logic
        # For now, just log what would be overridden
        print(f"Overrides for {config_name}: {overrides}")
        return True


if __name__ == "__main__":
    # Test config manager
    dotfiles_root = Path(__file__).parent.parent
    manager = ConfigManager(dotfiles_root)
    
    # Test profile loading
    try:
        profile = manager.load_profile("macos.yml")
        print("Loaded macOS profile:")
        print(f"  OS: {profile.get('os')}")
        print(f"  Package Manager: {profile.get('package_manager')}")
        print(f"  Config Paths: {list(profile.get('config_paths', {}).keys())}")
        
        # Test conflict detection
        conflicts = manager.check_conflicts(profile)
        if conflicts:
            print(f"\nFound {len(conflicts)} conflicts:")
            for conflict in conflicts:
                print(f"  - {conflict['name']}: {conflict['path']}")
        else:
            print("\nNo conflicts found")
    
    except Exception as e:
        print(f"Error: {e}")
