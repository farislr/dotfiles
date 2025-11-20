# LazyVim Configuration

Place your LazyVim configuration files here.

## Structure

```
lazyvim/
├── init.lua              # Main init file
├── lua/
│   ├── config/           # LazyVim configuration
│   │   ├── autocmds.lua
│   │   ├── keymaps.lua
│   │   ├── lazy.lua
│   │   └── options.lua
│   └── plugins/          # Your plugin configurations
│       └── example.lua
└── README.md
```

## Quick Start

1. Copy your existing LazyVim config here
2. Run the installer: `python3 install.py`
3. Your config will be symlinked to `~/.config/nvim`
4. Open nvim and plugins will install automatically

## Resources

- LazyVim Docs: https://www.lazyvim.org
- Lazy.nvim: https://github.com/folke/lazy.nvim
