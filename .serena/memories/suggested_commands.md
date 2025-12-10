# Suggested Commands

## Installation and Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run the interactive installer
python3 install.py

# Test individual modules (standalone)
python3 src/device_detector.py
python3 src/backup.py
python3 src/config_manager.py
python3 src/tool_installer.py
```

## Development Testing
```bash
# No formal test suite - run modules directly
python3 -m src.device_detector
python3 -m src.backup
python3 -m src.config_manager

# Check Python syntax
python3 -m py_compile src/*.py
```

## Git Workflow
```bash
# Check status and branch
git status
git branch

# Commit configuration changes
git add configs/
git commit -m "Update: describe changes"
git push origin main
```

## macOS Utilities (Darwin)
```bash
# List files with details
ls -la

# Search for files
find . -name "*.py" -type f
mdfind -name "filename"  # Spotlight search

# Search in files
grep -r "pattern" src/
ag "pattern" src/  # if silver-searcher installed

# Change directory
cd ~/dotfiles

# View file contents
cat filename
less filename
head -20 filename
tail -20 filename
```

## Package Management
```bash
# macOS (Homebrew)
brew install neovim kitty zsh
brew list
brew update && brew upgrade

# Ubuntu/Debian (APT)
sudo apt update && sudo apt install neovim kitty zsh
apt list --installed

# Arch/Manjaro (Pacman)
sudo pacman -S neovim kitty zsh
pacman -Q
```

## Backup Management
```bash
# List backups
ls -l backups/

# Restore from backup
cp -r backups/YYYY-MM-DD_HH-MM-SS/nvim ~/.config/
```
