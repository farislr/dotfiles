# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load
# Use powerlevel10k theme
ZSH_THEME="powerlevel10k/powerlevel10k"

# Which plugins would you like to load?
plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh

# User configuration

# Preferred editor
export EDITOR='nvim'

# Aliases
alias vim='nvim'
alias v='nvim'
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'

# >>> DOTFILES MANAGED SECTION START >>>
# This section is managed by dotfiles installer
# Add your custom configurations below this section
# >>> DOTFILES MANAGED SECTION END >>>
