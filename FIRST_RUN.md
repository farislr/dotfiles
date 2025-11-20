# 🎯 First Run Checklist

Follow these steps to get your dotfiles system up and running!

## ☑️ Pre-Installation Checklist

### 1. Review Current Setup
- [ ] I know where my current configs are located
- [ ] I have backups of important configs (just in case!)
- [ ] I'm ready to let the installer backup old configs

### 2. Prepare Your Configs

#### LazyVim/Neovim
- [ ] Copy existing nvim config: `cp -r ~/.config/nvim/* configs/lazyvim/`
- [ ] OR create new LazyVim config in `configs/lazyvim/`
- [ ] OR skip for now (use sample later)

#### Zsh
- [ ] Review `configs/zsh/.zshrc` (sample provided)
- [ ] Add your custom aliases and functions
- [ ] OR use as-is and customize later

#### Kitty
- [ ] Review `configs/kitty/kitty.conf` (Gruvbox theme provided)
- [ ] Adjust font, colors, etc.
- [ ] OR use as-is

#### OpenCode
- [ ] Will install manually (installer provides instructions)
- [ ] Can add config files later

### 3. Customize Profiles

#### Work Profile (`profiles/work.yml`)
```bash
nano profiles/work.yml
```
- [ ] Add work Git name
- [ ] Add work Git email
- [ ] Add any work-specific aliases

#### Personal Profile (`profiles/personal.yml`)
```bash
nano profiles/personal.yml
```
- [ ] Add personal Git name
- [ ] Add personal Git email
- [ ] Add any personal aliases

## 🚀 Installation Steps

### 1. Install Python Dependencies
```bash
cd ~/dotfiles
pip3 install -r requirements.txt
```
- [ ] Dependencies installed successfully

### 2. Test Device Detection (Optional)
```bash
python3 src/device_detector.py
```
- [ ] System detected correctly
- [ ] Package manager found

### 3. Run the Installer
```bash
python3 install.py
```

You'll be asked:
- [ ] Work or Personal profile? → Choose one
- [ ] Install tools? → Yes (recommended first time)
- [ ] Install Oh-My-Zsh? → Yes
- [ ] Install Oh-My-Posh? → Yes
- [ ] Install zsh plugins? → Yes
- [ ] Install OpenCode? → Follow manual instructions
- [ ] Overwrite existing configs? → Yes (backups created first!)

### 4. Wait for Installation
The installer will:
- Detect your system ✅
- Load profiles ✅
- Check for conflicts ✅
- Create backups ✅
- Install tools ✅
- Deploy configs ✅

This takes 5-10 minutes depending on internet speed.

## ✅ Post-Installation

### 1. Restart Terminal
```bash
# Close and reopen terminal
# OR
source ~/.zshrc
```
- [ ] New zsh theme loaded
- [ ] Aliases work

### 2. Test Neovim
```bash
nvim
```
- [ ] LazyVim loads
- [ ] Plugins install (wait for this!)
- [ ] No errors

### 3. Test Kitty
```bash
kitty
```
- [ ] New window opens
- [ ] Theme looks good
- [ ] Font is correct

### 4. Verify Symlinks
```bash
ls -la ~/.config/nvim
ls -la ~/.config/kitty
ls -la ~/.zshrc
```
- [ ] All point to dotfiles directory
- [ ] Symlinks are green/blue (working)

## 🎨 Customization

### Edit Configs
```bash
cd ~/dotfiles/configs

# Edit any config
nano zsh/.zshrc
nano kitty/kitty.conf

# Changes are immediately active (symlinks!)
# Test in new terminal window
```

### Commit Your Setup
```bash
git add .
git status  # Review what's being committed
git commit -m "Initial dotfiles setup for macOS"
git push origin main
```

## 🔧 If Something Goes Wrong

### Restore from Backup
```bash
# List backups
ls -l backups/

# Restore everything
cp -r backups/YYYY-MM-DD_HH-MM-SS/* ~/
```

### Remove Symlinks
```bash
# Remove and restore original
rm ~/.config/nvim  # Remove symlink
cp -r backups/latest/nvim ~/.config/nvim  # Restore original
```

### Re-run Installer
```bash
# Installer is idempotent - safe to run multiple times
python3 install.py
```

## 📝 Track Your Progress

### What's Working?
- [ ] Zsh with plugins
- [ ] Oh-My-Posh prompt
- [ ] Neovim/LazyVim
- [ ] Kitty terminal
- [ ] Claude Code
- [ ] OpenCode
- [ ] Git configured correctly

### What Needs Attention?
- [ ] ___________________
- [ ] ___________________
- [ ] ___________________

## 🎉 Success Criteria

You'll know it's working when:
- ✅ Terminal has new theme (powerlevel10k or oh-my-posh)
- ✅ `which nvim` shows neovim installed
- ✅ Neovim opens with LazyVim
- ✅ Aliases work (`ll`, `v`, etc.)
- ✅ Kitty looks themed and pretty
- ✅ Git shows correct user.name and user.email

## 🚀 Next Device Setup

When setting up another device:
```bash
# 1. Clone
git clone https://github.com/yourusername/dotfiles.git ~/dotfiles

# 2. Install deps
cd ~/dotfiles
pip3 install -r requirements.txt

# 3. Run installer
python3 install.py

# Done! 🎉
```

## 📚 Resources

- **Full docs**: README.md
- **Quick setup**: SETUP_GUIDE.md  
- **Summary**: PROJECT_SUMMARY.md
- **This checklist**: FIRST_RUN.md (you are here!)

---

**Start with step 1 above and check off items as you go!** ✨
