# Project Overview

## Purpose
Cross-platform dotfiles management system for maintaining consistent development environments across macOS and Linux. Automates deployment of configuration files (LazyVim, OpenCode, Zsh, Kitty, Claude Code) using profile-based approach with device detection, backup management, and symlink deployment.

## Key Features
- **Cross-Platform**: macOS, Ubuntu/Arch Linux support
- **Device Detection**: Auto-detects OS, distro, architecture, package manager
- **Profile System**: Work/personal configurations with OS-specific overrides
- **Safe Backups**: Timestamped backups before changes
- **Symlink Management**: Live config updates via symlinks
- **Interactive CLI**: Rich library for user-friendly prompts and tables

## Supported Tools
- LazyVim (Neovim distribution)
- OpenCode (AI-powered editor)
- Zsh (with Oh-My-Zsh/Oh-My-Posh)
- Kitty (terminal emulator)
- Claude Code

## Architecture Pattern
7-phase orchestration:
1. Device detection → system info
2. Profile selection → user choice
3. Profile merging → base OS + user profile
4. Conflict detection → existing configs
5. Backup creation → timestamped preservation
6. Tool installation → packages/plugins
7. Config deployment → symlink creation
