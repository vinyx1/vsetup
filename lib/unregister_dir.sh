#!/bin/zsh

ROOT="$1"
REGISTRY="$HOME/vsetup/dir/registry"

if [[ -z "$ROOT" ]]; then
    echo "unregister_dir: missing root directory"
    exit 1
fi

if [[ ! -f "$REGISTRY" ]]; then
    echo "Directory registry does not exist."
    exit 0
fi

TEMP_FILE="${REGISTRY}.tmp"

awk -v root="$ROOT" '
    $0 != root {
        print
    }
' "$REGISTRY" > "$TEMP_FILE"

mv "$TEMP_FILE" "$REGISTRY"

echo "Unregistered directory:"
echo "  $ROOT"