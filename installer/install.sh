#!/bin/bash

ROOT="$HOME/vsetup"

# Make executable scripts executable
chmod +x "$ROOT/bin/"*

# ---------------- Bash ----------------

BASH_PROFILE="$HOME/.bash_profile"
BASH_MARKER="# ---------------- vsetup bash ----------------"
BASH_SNIPPET="$ROOT/installer/snippets/bash_profile"

touch "$BASH_PROFILE"

if grep -Fq "$BASH_MARKER" "$BASH_PROFILE"; then
    echo "vsetup is already configured in .bash_profile"
else
    echo >> "$BASH_PROFILE"
    cat "$BASH_SNIPPET" >> "$BASH_PROFILE"

    echo "Added vsetup to .bash_profile"
fi


# ---------------- Zsh ----------------

ZSHRC="$HOME/.zshrc"
ZSH_MARKER="# ---------------- vsetup zsh ----------------"
ZSH_SNIPPET="$ROOT/installer/snippets/zshrc"

touch "$ZSHRC"

if grep -Fq "$ZSH_MARKER" "$ZSHRC"; then
    echo "vsetup is already configured in .zshrc"
else
    echo >> "$ZSHRC"
    cat "$ZSH_SNIPPET" >> "$ZSHRC"

    echo "Added vsetup to .zshrc"
fi


echo
echo "vsetup installation complete."
echo "Open a new terminal, or run:"
echo "  source ~/.zshrc"
echo "  source ~/.bash_profile"