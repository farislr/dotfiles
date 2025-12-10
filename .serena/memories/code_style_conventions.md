# Code Style and Conventions

## Python Style
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Module-level docstrings with usage examples
- **Type Hints**: Not currently used (could be added for improvement)
- **Imports**: Standard library → third-party → local modules
- **Line Length**: ~80-100 characters (informal, no strict enforcement)

## Module Structure
Each module follows pattern:
```python
"""Module docstring with purpose"""
import statements
class definitions
if __name__ == "__main__":
    # Standalone testing code
```

## Naming Conventions
- **Managers**: BackupManager, ConfigManager (responsibility pattern)
- **Detectors**: DeviceDetector (active noun pattern)
- **Installers**: ToolInstaller, DotfilesInstaller (action pattern)
- **Variables**: descriptive names (dotfiles_root, config_mgr, backup_mgr)

## File Organization
- **src/**: Python modules (modular, independently testable)
- **configs/**: Configuration files (organized by tool)
- **profiles/**: YAML profile definitions (OS + user)
- **scripts/**: Shell scripts for system operations
- **backups/**: Timestamped backup directories (gitignored)

## Error Handling
- Validate system support early (check_system_support)
- User confirmation at critical steps
- Detailed error messages via rich.Console
- Preserve existing configs before changes
