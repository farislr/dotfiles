"""Backup management for existing configurations."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class BackupManager:
    """Manages backups of existing configuration files."""
    
    def __init__(self, backup_root: Path):
        self.backup_root = Path(backup_root)
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.backup_dir = self.backup_root / self.timestamp
        self.backup_log: List[Dict[str, str]] = []
    
    def create_backup_directory(self) -> Path:
        """Create timestamped backup directory."""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        return self.backup_dir
    
    def backup_file(self, source: Path, name: str = None) -> bool:
        """
        Backup a single file or directory.
        
        Args:
            source: Path to file/directory to backup
            name: Optional custom name for backup
        
        Returns:
            True if backup successful, False otherwise
        """
        if not source.exists():
            return False
        
        try:
            # Use custom name or original name
            backup_name = name or source.name
            destination = self.backup_dir / backup_name
            
            if source.is_file():
                # Backup file
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            elif source.is_dir():
                # Backup directory
                shutil.copytree(source, destination, symlinks=True)
            
            # Log the backup
            self.backup_log.append({
                "source": str(source),
                "destination": str(destination),
                "type": "directory" if source.is_dir() else "file",
                "timestamp": self.timestamp
            })
            
            return True
        
        except Exception as e:
            print(f"Error backing up {source}: {e}")
            return False
    
    def backup_configs(self, config_paths: Dict[str, str]) -> Dict[str, bool]:
        """
        Backup multiple configuration paths.
        
        Args:
            config_paths: Dict of name -> path mappings
        
        Returns:
            Dict of name -> success status
        """
        results = {}
        
        for name, path_str in config_paths.items():
            path = Path(path_str).expanduser()
            
            if path.exists():
                success = self.backup_file(path, name)
                results[name] = success
                
                if success:
                    print(f"✓ Backed up: {name} ({path})")
                else:
                    print(f"✗ Failed to backup: {name} ({path})")
            else:
                results[name] = None  # Doesn't exist, no backup needed
        
        return results
    
    def get_backup_summary(self) -> Dict:
        """Get summary of backup operation."""
        return {
            "backup_directory": str(self.backup_dir),
            "timestamp": self.timestamp,
            "items_backed_up": len(self.backup_log),
            "log": self.backup_log
        }
    
    def save_backup_log(self) -> None:
        """Save backup log to file."""
        log_file = self.backup_dir / "backup_log.txt"
        
        with open(log_file, "w") as f:
            f.write(f"Dotfiles Backup Log\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"=" * 60 + "\n\n")
            
            for entry in self.backup_log:
                f.write(f"Type: {entry['type']}\n")
                f.write(f"Source: {entry['source']}\n")
                f.write(f"Destination: {entry['destination']}\n")
                f.write(f"-" * 60 + "\n")
        
        print(f"\nBackup log saved to: {log_file}")


if __name__ == "__main__":
    # Test backup manager
    backup_mgr = BackupManager(Path("./backups"))
    backup_mgr.create_backup_directory()
    
    # Test with example configs
    test_configs = {
        "zshrc": "~/.zshrc",
        "nvim": "~/.config/nvim",
    }
    
    results = backup_mgr.backup_configs(test_configs)
    print("\nBackup Results:")
    for name, status in results.items():
        print(f"  {name}: {status}")
    
    summary = backup_mgr.get_backup_summary()
    print(f"\nBackup Summary:")
    print(f"  Directory: {summary['backup_directory']}")
    print(f"  Items: {summary['items_backed_up']}")
