#!/bin/zsh

ROOT="$1"

if [[ -z "$ROOT" ]]; then
    echo "uncreate_vsetup_in: missing root directory"
    exit 1
fi

VSETUP_DIR="$ROOT/.vsetup"

if [[ ! -d "$VSETUP_DIR" ]]; then
    echo "No .vsetup directory found in:"
    echo "  $ROOT"
    exit 0
fi

rm -rf "$VSETUP_DIR"

echo "Removed:"
echo "  $VSETUP_DIR"