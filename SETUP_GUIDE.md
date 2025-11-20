# Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Add Your Configs

Before running the installer, populate your configuration directories:

#### LazyVim
```bash
# If you have existing LazyVim config
cp -r ~/.config/nvim/* configs/lazyvim/

# Or create new config files
# See configs/lazyvim/README.md for structure
```

#### Kitty
```bash
# Copy existing config (already has a sample!)
# Edit configs/kitty/kitty.conf to customize
```

#### Zsh
```bash
# The sample .zshrc is ready to use!
# Customize configs/zsh/.zshrc to your liking
```

#### OpenCode
```bash
# If you have existing OpenCode config
# macOS:
cp ~/Library/Application\ Support/OpenCode/* configs/opencode/

# Linux:
cp ~/.config/OpenCode/* configs/opencode/
```

### Step 2: Customize Profiles

Edit work/personal settings:

```bash
# Edit your Git identity
nano profiles/work.yml      # Work email and name
nano profiles/personal.yml  # Personal email and name
```

### Step 3: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 4: Run the Installer

```bash
python3 install.py
```

The installer will:
1. ✅ Detect your system
2. ✅ Ask work or personal profile
3. ✅ Show any conflicts
4. ✅ Create backups
5. ✅ Install tools (optional)
6. ✅ Deploy configs via symlinks

### Step 5: Restart Terminal

```bash
# Reload zsh
source ~/.zshrc

# Or restart your terminal completely
```

### Step 6: Launch Apps

```bash
# Launch nvim to install LazyVim plugins
nvim

# First launch will auto-install plugins
# Be patient, this takes a few minutes!
```

## 📝 Next Steps

### Commit Your Setup
```bash
git add .
git commit -m "Initial dotfiles setup"
git push origin main
```

### Setup on Another Device
```bash
git clone https://github.com/yourusername/dotfiles.git ~/dotfiles
cd ~/dotfiles
pip3 install -r requirements.txt
python3 install.py
```

### Update Configs
```bash
# Edit files in configs/
# Changes are immediately active (symlinks!)
# Commit when happy:
git add .
git commit -m "Update kitty colorscheme"
git push
```

## 🔧 Customization Examples

### Add a New Tool
1. Create `configs/newtool/` directory
2. Add files: `configs/newtool/config.conf`
3. Edit profile:
   ```yaml
   # profiles/macos.yml
   config_paths:
     newtool: ~/.config/newtool
   ```
4. Run: `python3 install.py`

### Change Package List
```yaml
# profiles/macos.yml
packages:
  - neovim
  - kitty
  - your-new-tool
```

### Add Custom Aliases
```bash
# configs/zsh/.zshrc
alias myproject="cd ~/projects/myproject"
alias gs="git status"
```

## 🛡️ Safety Features

- **Auto Backup**: Every run backs up existing configs
- **Timestamp**: Backups in `backups/YYYY-MM-DD_HH-MM-SS/`
- **Restore**: Just copy from backups back to home
- **No Overwrites**: Prompts before replacing files

## ⚡ Pro Tips

1. **Use Serena**: 
   ```bash
   # In Claude Code
   /sc:load
   ```

2. **Test Before Deploy**:
   ```bash
   # Edit configs locally
   # Test manually
   # Then run installer
   ```

3. **Keep Secrets Out**:
   - Never commit API keys
   - Use environment variables
   - `.gitignore` protects you

4. **Branch for Experiments**:
   ```bash
   git checkout -b test-theme
   # make changes
   # test
   # merge if good
   ```

## 🆘 Common Issues

### "Module not found"
```bash
cd ~/dotfiles
pip3 install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x install.py
python3 install.py
```

### "Already exists"
- Installer detected conflicts
- Choose backup option when prompted
- Or manually remove old configs

### Restore Everything
```bash
# Find your backup
ls backups/

# Restore all
cp -r backups/YYYY-MM-DD_HH-MM-SS/* ~/
```

---

**Need help?** Check the main README.md for full documentation!
