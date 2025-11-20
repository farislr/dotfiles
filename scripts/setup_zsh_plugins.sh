#!/usr/bin/env bash
# Setup zsh plugins manually if needed

set -e

CUSTOM_DIR="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

echo "Setting up zsh plugins..."

# zsh-autosuggestions
if [ ! -d "$CUSTOM_DIR/plugins/zsh-autosuggestions" ]; then
    echo "Installing zsh-autosuggestions..."
    git clone https://github.com/zsh-users/zsh-autosuggestions "$CUSTOM_DIR/plugins/zsh-autosuggestions"
fi

# zsh-syntax-highlighting
if [ ! -d "$CUSTOM_DIR/plugins/zsh-syntax-highlighting" ]; then
    echo "Installing zsh-syntax-highlighting..."
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$CUSTOM_DIR/plugins/zsh-syntax-highlighting"
fi

# powerlevel10k
if [ ! -d "$CUSTOM_DIR/themes/powerlevel10k" ]; then
    echo "Installing powerlevel10k..."
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$CUSTOM_DIR/themes/powerlevel10k"
fi

echo "✓ All zsh plugins installed"
