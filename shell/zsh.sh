VSETUP_EXEC="$HOME/vsetup/bin/vsetup-exec"
VSETUP_ALIASES="$HOME/vsetup/config/.vsetup_aliases"

vsetup() {
    "$VSETUP_EXEC" "$@"
    local status=$?

    if [[ $status -eq 0 && -f "$VSETUP_ALIASES" ]]; then
        source "$VSETUP_ALIASES"
    fi

    return $status
}

## Load existing aliases when zsh starts
# not required since i don't use folder specific aliases outside of vscode, usually. add it back if i do.
#if [[ -f "$VSETUP_ALIASES" ]]; then
#    source "$VSETUP_ALIASES"
#fi