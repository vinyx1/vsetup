#!/bin/zsh

ROOT="$1"
REGISTRY="$HOME/vsetup/dir/registry"

if [[ -z "$ROOT" ]]; then
    echo "register_repo: missing root directory"
    exit 1
fi

mkdir -p "$(dirname "$REGISTRY")"
touch "$REGISTRY"

if grep -Fxq "$ROOT" "$REGISTRY"; then
    echo "Repo already registered."
else
    echo "$ROOT" >> "$REGISTRY"

    echo "Registered repo:"
    echo "$ROOT"
fi