# Design Patterns and Guidelines

## Key Design Decisions

### 1. Symlinks Over Copying
**Rationale**: Changes in dotfiles repo are immediately reflected in user environment
**Implementation**: ConfigManager.create_symlink() creates symbolic links
**Benefit**: No need to re-run installer after config edits

### 2. Profile Merging System
**Pattern**: Base OS profile → User profile (later overrides earlier)
**Implementation**: ConfigManager.merge_profiles() with deep merge for "overrides" dict
**Use Case**: Work/personal separation with OS-specific defaults

### 3. Tier 1 Backups
**Pattern**: Always backup before any destructive operation
**Implementation**: BackupManager creates timestamped directories
**Safety**: Never modify user configs without preservation

### 4. Interactive Prompts
**Pattern**: User confirmation at each major step
**Implementation**: rich.Prompt.ask() for decisions
**Philosophy**: User control over installation process

### 5. Modular Design
**Pattern**: Each module independently testable via __main__
**Implementation**: All modules have if __name__ == "__main__" guard
**Benefit**: Easy to test individual components

## Critical Paths (Never Modify)

### Backup Directory Structure
- Format: backups/YYYY-MM-DD_HH-MM-SS/
- Breaking this affects restore operations
- Backup logs must maintain metadata format

### Profile Merge Order
- OS profile loaded first, user profile second
- Later profiles override earlier (expected behavior)
- "overrides" dict gets deep merge special handling

### Symlink Resolution Logic
- Source: configs/{tool}/ → Target: ~/.config/{tool}/ or ~/{tool}
- Users depend on this mapping
- Changing this breaks existing deployments

## Handle With Care

### YAML Profile Schema
- Changes affect ConfigManager.merge_profiles()
- config_paths, packages, overrides are expected keys
- Adding new keys requires merge logic updates

### DeviceDetector Supported Platforms
- Currently: macOS, Ubuntu, Arch
- Adding new platform requires tool_installer.py updates
- Package manager detection logic is platform-specific

### ToolInstaller Package Manager Commands
- Platform-specific: brew (macOS), apt (Ubuntu), pacman (Arch)
- Command changes must be tested on target platform
- Error handling for missing package managers

## Patterns to Follow

### Manager Pattern
Classes ending in "Manager" handle specific responsibilities:
- BackupManager: backup operations
- ConfigManager: profile and config operations

### Detector Pattern
Classes ending in "Detector" actively gather information:
- DeviceDetector: system information detection

### Installer Pattern
Classes ending in "Installer" perform installation actions:
- ToolInstaller: package installation
- DotfilesInstaller: overall orchestration

## Extension Points

### Adding New Tool Support
1. Create directory: configs/newtool/
2. Add to OS profile config_paths
3. Optionally add package to packages list
4. Run installer - automatic symlink creation

### Adding New Package Manager
1. Update DeviceDetector._detect_package_manager()
2. Add case in ToolInstaller.install_package()
3. Test on target platform

### Custom Profile Keys
1. Add key to YAML profiles
2. Update ConfigManager if special merge behavior needed
3. Document in CLAUDE.md or README.md
