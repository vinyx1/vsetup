#!/bin/zsh

ROOT="$1"
CONFIG_DIR="$ROOT/.vsetup"
TEMPLATES="$HOME/vsetup/templates"

if [[ -z "$ROOT" ]]; then
    echo "init_repo: missing root directory"
    exit 1
fi

if [[ -d "$CONFIG_DIR" ]]; then
    echo "vsetup already initialized here."
    exit 0
fi

mkdir -p "$CONFIG_DIR/scripts"

cp "$TEMPLATES/aliases.sh" "$CONFIG_DIR/aliases.sh"
cp "$TEMPLATES/keybindings.json" "$CONFIG_DIR/keybindings.json"
cp "$TEMPLATES/sample_script.sh" "$CONFIG_DIR/scripts/sample_script.sh"

echo "created the dir .vsetup in:"
echo "$ROOT"