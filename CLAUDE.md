# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a cross-platform dotfiles management system written in Python. It automates the deployment of configuration files (LazyVim, OpenCode, Zsh, Kitty, Claude Code) across macOS and Linux systems using a profile-based approach with automatic device detection, backup management, and symlink deployment.

## Essential Commands

### Installation and Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run the interactive installer
python3 install.py

# Test individual modules
python3 src/device_detector.py  # Test device detection
python3 src/backup.py           # Test backup system
python3 src/config_manager.py   # Test config manager
```

### Testing the System
```bash
# No formal test suite - run modules directly to test
# Each module has __main__ guard for standalone testing
python3 -m src.device_detector
python3 -m src.backup
```

## Architecture

### Core Data Flow

The installer follows a **7-phase orchestration pattern**:

```
DotfilesInstaller.run() orchestrates:
├─ 1. DeviceDetector → system info (OS, distro, arch, pkg manager)
├─ 2. Profile selection → user choice (work/personal)
├─ 3. ConfigManager.merge_profiles() → base OS + user profile
├─ 4. ConfigManager.check_conflicts() → detect existing configs
├─ 5. BackupManager.backup_configs() → timestamped backups
├─ 6. ToolInstaller.install_*() → install packages/plugins
└─ 7. ConfigManager.deploy_configs() → create symlinks
```

### Module Responsibilities

**src/installer.py** (`DotfilesInstaller`)
- Main orchestrator coordinating all other modules
- Interactive CLI using `rich` library for prompts and tables
- Sequential execution of installation phases
- User decision points between each phase

**src/device_detector.py** (`DeviceDetector`)
- Single source of truth for system information
- Detects: OS type, Linux distro, architecture, package manager, hostname
- Validates system support before installation proceeds
- Returns profile filename to load (e.g., "macos.yml")

**src/config_manager.py** (`ConfigManager`)
- Profile loading and merging logic (YAML → dict)
- Conflict detection (checks if target paths already exist)
- Symlink creation from `configs/` to home directory (supports both files and directories)
- Auto-detection of file vs directory based on extensions and dotfile naming patterns
- Profile merge order: OS profile → user profile (later overrides earlier)

**src/backup.py** (`BackupManager`)
- Creates timestamped backup directories: `backups/YYYY-MM-DD_HH-MM-SS/`
- Preserves directory structure and symlinks
- Generates backup logs with metadata
- Never destructive - all changes backed up first

**src/tool_installer.py** (`ToolInstaller`)
- Package installation via brew/apt/pacman
- Oh-My-Zsh and Oh-My-Posh installation
- Zsh plugin setup (git clone into custom directories)
- OpenCode installation guidance (manual download)

### Profile System

Profiles are YAML files defining OS-specific and user-specific configurations:

**Base OS Profiles** (`profiles/macos.yml`, `profiles/linux.yml`)
- Package lists per OS
- Package manager specification
- Default config paths (platform-specific)
- OS-specific overrides (e.g., different font sizes)

**User Profiles** (`profiles/work.yml`, `profiles/personal.yml`)
- Git user.name and user.email
- Custom aliases and environment variables
- Additional overrides merged on top of OS profile

**Profile Merging Logic** (src/config_manager.py:45-72)
```python
# Merge order: base_profile → additional_profiles
# Later profiles override earlier ones
# Special handling for "overrides" dict (deep merge)
```

### Configuration Deployment

**Symlink Strategy** (ConfigManager.create_symlink)

Supports both directory and individual file symlinks with automatic detection:

```
Directory symlinks:
  configs/lazyvim/ → ~/.config/nvim
  configs/kitty/   → ~/.config/kitty

Individual file symlinks:
  configs/.zshrc → ~/.zshrc
  configs/.gitconfig → ~/.gitconfig
```

**Auto-Detection Logic** (ConfigManager._is_file_path):
1. If source exists: Check if it's a file or directory
2. If source doesn't exist: Check for file extension (e.g., `.conf`, `.json`)
3. Check for common dotfile names (`.zshrc`, `.vimrc`, `.gitconfig`, etc.)
4. Default: Treat as directory

Changes to files in `configs/` are immediately reflected in the user's environment (benefit of symlinks).

### Key Design Decisions

1. **Symlinks over copying**: Changes in dotfiles repo are live immediately
2. **Profile merging**: Flexible override system for work/personal separation
3. **Tier 1 backups**: Automatic timestamped backups before any changes
4. **Interactive prompts**: User confirmation at each major step
5. **Modular design**: Each module testable independently via `__main__`

## Configuration Files

### Adding New Tool Support

**For directory configs:**
1. Create config directory: `configs/newtool/`
2. Add to OS profile:
   ```yaml
   # profiles/macos.yml
   config_paths:
     newtool: ~/.config/newtool
   ```

**For individual file configs:**
1. Create config file: `configs/.configfile` or `configs/tool/.configfile`
2. Add to OS profile:
   ```yaml
   # profiles/macos.yml
   config_paths:
     # Auto-detected as file (has dotfile name pattern)
     .zshrc: ~/.zshrc

     # Auto-detected as file (has extension)
     tool/.gitconfig: ~/.gitconfig

     # Directory symlink for comparison
     kitty: ~/.config/kitty
   ```

**Optional:** Add package to install:
   ```yaml
   packages:
     - newtool
   ```

### Modifying Installation Behavior

**Add new package manager support**: Edit `DeviceDetector._detect_package_manager()` and `ToolInstaller.install_package()`

**Change backup location**: Modify `BackupManager.__init__` timestamp format or root path

**Customize symlink behavior**: Edit `ConfigManager.create_symlink()` force/preserve logic

## Serena Integration

This project is configured for Serena MCP (`.serena/project.yml`). The project is Python-based for semantic code navigation.

When making changes:
- Use Serena's symbol-based tools for refactoring
- Maintain module independence (each module has `__init__` and `__main__`)
- Profile YAML structure is critical - changes affect merging logic

## Critical Paths

**Never modify**:
- Backup directory structure (breaking change for restore operations)
- Profile merge order (later profiles override earlier - this is expected behavior)
- Symlink resolution logic (users depend on configs/ → home mapping)

**Handle with care**:
- YAML profile schema (affects ConfigManager.merge_profiles)
- DeviceDetector supported platforms (affects installation flow)
- ToolInstaller package manager commands (platform-specific)
