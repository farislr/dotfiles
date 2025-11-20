# Dotfiles Manager

> Cross-platform dotfiles management system with device detection and automated installation

A powerful, Python-based dotfiles management system that makes it easy to maintain consistent development environments across multiple devices and operating systems.

## Features

- 🖥️ **Cross-Platform Support**: Works on macOS and Linux (Ubuntu/Arch)
- 🔍 **Automatic Device Detection**: Detects OS, distro, architecture, and package manager
- 📦 **Automated Tool Installation**: Installs required tools via brew, apt, or pacman
- 💾 **Safe Backups**: Automatic timestamped backups before any changes
- 🔗 **Symlink Management**: Efficient symlink-based config deployment
- 👔 **Profile System**: Separate work and personal configurations
- 🎨 **Interactive Setup**: User-friendly prompts guide you through installation
- 🛡️ **Conflict Detection**: Identifies existing configs before proceeding

## Supported Configurations

- **LazyVim** (Neovim distribution)
- **OpenCode** (AI-powered code editor)
- **Zsh** (with Oh-My-Zsh and Oh-My-Posh)
- **Kitty** (Terminal emulator)
- **Claude Code** (Already included!)

## Quick Start

### Prerequisites

- Git (required)
- Python 3.8+ (required)
- Internet connection

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/dotfiles.git ~/dotfiles
   cd ~/dotfiles
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the installer**:
   ```bash
   python3 install.py
   ```

4. **Follow the interactive prompts**:
   - Select work or personal profile
   - Review detected conflicts
   - Choose which tools to install
   - Confirm configuration deployment

## Directory Structure

```
dotfiles/
├── .serena/                    # Serena MCP configuration
│   └── project.yml
├── configs/                    # Your actual configuration files
│   ├── lazyvim/               # LazyVim/Neovim configs
│   ├── opencode/              # OpenCode configs
│   ├── zsh/                   # Zsh configs (.zshrc)
│   ├── kitty/                 # Kitty terminal configs
│   └── claude/                # Claude Code configs
├── profiles/                   # Device and user profiles
│   ├── macos.yml              # macOS-specific settings
│   ├── linux.yml              # Linux-specific settings
│   ├── work.yml               # Work profile overrides
│   └── personal.yml           # Personal profile overrides
├── scripts/                    # Shell scripts
│   └── setup_zsh_plugins.sh   # Zsh plugin installer
├── src/                        # Python modules
│   ├── device_detector.py     # OS/device detection
│   ├── backup.py              # Backup management
│   ├── config_manager.py      # Config deployment
│   ├── tool_installer.py      # Tool installation
│   └── installer.py           # Main orchestrator
├── backups/                    # Timestamped backups (gitignored)
├── install.py                  # Main entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## How It Works

### 1. Device Detection
The system automatically detects:
- Operating System (macOS/Linux)
- Linux Distribution (Ubuntu/Arch)
- Architecture (x86_64/arm64)
- Available package manager (brew/apt/pacman)

### 2. Profile Selection
Choose between:
- **Work Profile**: Work-specific Git config, aliases, and settings
- **Personal Profile**: Personal configurations

Profiles are merged with OS-specific settings for a tailored experience.

### 3. Backup System
Before making any changes:
- Creates timestamped backup directory: `backups/YYYY-MM-DD_HH-MM-SS/`
- Backs up all existing configurations
- Saves detailed backup log
- Never destructive without backup

### 4. Tool Installation
Optionally installs:
- Core tools (neovim, kitty, zsh, git)
- Oh-My-Zsh framework
- Oh-My-Posh prompt engine
- Zsh plugins (autosuggestions, syntax highlighting, powerlevel10k)
- OpenCode (with manual download guidance)

### 5. Configuration Deployment
Creates symlinks:
```
~/.config/nvim → /path/to/dotfiles/configs/lazyvim/
~/.config/kitty → /path/to/dotfiles/configs/kitty/
~/.zshrc → /path/to/dotfiles/configs/zsh/.zshrc
```

Changes in the dotfiles repo are immediately reflected in your environment!

## Customization

### Adding New Configurations

1. Create a directory in `configs/` for your new config
2. Add the config path to appropriate profile:
   ```yaml
   # profiles/macos.yml
   config_paths:
     myapp: ~/.config/myapp
   ```
3. Run `python3 install.py` to deploy

### Modifying Profiles

Edit profile files to customize:

**macOS-specific settings** (`profiles/macos.yml`):
```yaml
packages:
  - neovim
  - your-tool

overrides:
  kitty:
    font_size: 14
```

**Work vs Personal** (`profiles/work.yml`):
```yaml
git:
  user:
    name: "Work Name"
    email: "work@company.com"

zsh:
  aliases:
    work_proxy: "export https_proxy=..."
```

## Usage

### First Time Setup
```bash
# Install everything
python3 install.py
```

### Update Configurations
```bash
# Make changes to files in configs/
# Changes are immediately active (symlinks!)

# Commit your changes
git add .
git commit -m "Update kitty theme"
git push
```

### Setup on New Device
```bash
# Clone and install
git clone https://github.com/yourusername/dotfiles.git ~/dotfiles
cd ~/dotfiles
pip3 install -r requirements.txt
python3 install.py
```

### Restore from Backup
```bash
# Backups are in ./backups/ with timestamps
# To restore manually:
cp -r backups/YYYY-MM-DD_HH-MM-SS/nvim ~/.config/nvim
```

## Advanced Features

### Serena Integration

This repository is configured for use with [Serena MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/serena), providing:
- Semantic code understanding
- Project memory
- Cross-session persistence

Activate with:
```bash
# In Claude Code or compatible tool
/sc:load
```

### Profile Merging

Profiles are merged in order:
1. Base OS profile (macos.yml or linux.yml)
2. User profile (work.yml or personal.yml)

Later profiles override earlier ones.

### Package Manager Auto-Detection

Supports:
- **macOS**: Homebrew (brew)
- **Ubuntu/Debian**: APT (apt)
- **Arch/Manjaro**: Pacman (pacman)

## Troubleshooting

### Python Module Not Found
```bash
# Ensure you're in the dotfiles directory
cd ~/dotfiles

# Install dependencies
pip3 install -r requirements.txt
```

### Symlink Creation Failed
```bash
# Check permissions
ls -la ~/.config/

# Remove existing config manually if needed
rm -rf ~/.config/nvim

# Re-run installer
python3 install.py
```

### Oh-My-Zsh Already Installed
The installer detects existing installations and skips them. Your existing Oh-My-Zsh setup is preserved.

### Backups

All backups are in `backups/` with timestamps. To restore:
```bash
# List backups
ls -l backups/

# Restore specific config
cp -r backups/2024-11-19_10-30-00/nvim ~/.config/
```

## Contributing to Your Dotfiles

1. Make changes in the `configs/` directory
2. Test changes locally
3. Commit and push:
   ```bash
   git add configs/
   git commit -m "Update: describe your changes"
   git push origin main
   ```
4. Pull on other devices and run installer to sync

## Security Notes

- **Sensitive Data**: Never commit secrets, API keys, or passwords
- **Work/Personal Separation**: Use profile system to keep work configs separate
- **.gitignore**: Pre-configured to exclude sensitive files
- **Backups**: Old configs may contain sensitive data - manage backups carefully

## Platform-Specific Notes

### macOS
- Uses Homebrew for package management
- Configs for macOS-specific apps
- Optimized for macOS titlebar and system integration

### Linux
- Supports Ubuntu (apt) and Arch (pacman)
- Auto-detects distribution
- Handles distro-specific packages

## Resources

- [LazyVim Documentation](https://www.lazyvim.org/)
- [Oh My Zsh](https://ohmyz.sh/)
- [Oh My Posh](https://ohmyposh.dev/)
- [Kitty Terminal](https://sw.kovidgoyal.net/kitty/)
- [OpenCode](https://opencode.ai/)

## License

MIT License - Feel free to use and modify for your own dotfiles!

## Acknowledgments

- Powered by Python and modern package managers
- Inspired by the dotfiles community
- Built with Serena MCP integration

---

**Happy configuring!** 🚀
