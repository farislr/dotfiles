# Codebase Structure

## Directory Layout
```
dotfiles/
├── src/                        # Python modules
│   ├── installer.py            # Main orchestrator (DotfilesInstaller)
│   ├── device_detector.py      # System detection (DeviceDetector)
│   ├── config_manager.py       # Profile merging & deployment (ConfigManager)
│   ├── backup.py               # Backup management (BackupManager)
│   ├── tool_installer.py       # Package installation (ToolInstaller)
│   ├── conflict_resolver.py    # Conflict handling
│   └── __init__.py             # Package initialization
├── configs/                     # Configuration files (symlink sources)
│   ├── lazyvim/                # Neovim configs
│   ├── opencode/               # OpenCode configs
│   ├── zsh/                    # Zsh configs (.zshrc)
│   ├── kitty/                  # Kitty terminal configs
│   └── claude/                 # Claude Code configs
├── profiles/                    # YAML profile definitions
│   ├── macos.yml               # macOS-specific settings
│   ├── linux.yml               # Linux-specific settings
│   ├── work.yml                # Work profile overrides
│   └── personal.yml            # Personal profile overrides
├── scripts/                     # Shell scripts
│   ├── setup_zsh_plugins.sh    # Zsh plugin installer
│   ├── install_brew_packages.sh
│   ├── install_apt_packages.sh
│   └── install_pacman_packages.sh
├── backups/                     # Timestamped backups (gitignored)
├── .serena/                     # Serena MCP configuration
│   └── project.yml
├── install.py                   # Main entry point
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
```

## Module Responsibilities

### installer.py (DotfilesInstaller)
- Main orchestrator coordinating all other modules
- Interactive CLI using rich library
- Sequential 7-phase execution
- Methods: run(), print_welcome(), show_device_info(), select_profile_type(), load_profiles(), check_conflicts(), backup_existing_configs(), install_tools(), deploy_configurations(), show_summary()

### device_detector.py (DeviceDetector)
- Single source of truth for system information
- Detects: OS type, Linux distro, architecture, package manager, hostname
- Validates system support before installation
- Returns profile filename to load (e.g., "macos.yml")

### config_manager.py (ConfigManager)
- Profile loading and merging logic (YAML → dict)
- Conflict detection (checks if target paths exist)
- Symlink creation from configs/ to home directory
- Profile merge order: OS profile → user profile

### backup.py (BackupManager)
- Creates timestamped backup directories: backups/YYYY-MM-DD_HH-MM-SS/
- Preserves directory structure and symlinks
- Generates backup logs with metadata
- Non-destructive - all changes backed up first

### tool_installer.py (ToolInstaller)
- Package installation via brew/apt/pacman
- Oh-My-Zsh and Oh-My-Posh installation
- Zsh plugin setup (git clone into custom directories)
- OpenCode installation guidance (manual download)
