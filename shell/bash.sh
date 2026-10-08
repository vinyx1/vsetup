# =========================================================
# vsetup Bash integration
#
# Responsibilities:
#   1. Provide the `vsetup` shell function
#   2. Load/unload repo-specific aliases
#   3. Detect when we enter/leave an auto-commit repo
#   4. Tell that repo's control.sh what happened
# =========================================================


# ---------------------------------------------------------
# Global vsetup paths
# ---------------------------------------------------------

VSETUP_EXEC="$HOME/vsetup/bin/vsetup-exec"
VSETUP_ALIASES="$HOME/vsetup/config/.vsetup_aliases"


# ---------------------------------------------------------
# Main vsetup command
#
# Runs the actual vsetup executable.
# If the command succeeds, reload aliases in case the command
# added/removed/changed repo aliases.
# ---------------------------------------------------------

vsetup() {
    "$VSETUP_EXEC" "$@"
    local status=$?

    if [[ $status -eq 0 ]]; then
        load_vsetup_aliases
    fi

    return $status
}


# ---------------------------------------------------------
# Remove aliases loaded by vsetup
#
# Each repo's aliases.sh should define:
#
#   VSETUP_ALIAS_NAMES=(build run test ...)
#
# so we know exactly which aliases to unload.
# ---------------------------------------------------------

clear_vsetup_aliases() {
    if [[ ${#VSETUP_ALIAS_NAMES[@]} -gt 0 ]]; then
        for name in "${VSETUP_ALIAS_NAMES[@]}"; do
            unalias "$name" 2>/dev/null
        done
    fi

    unset VSETUP_ALIAS_NAMES
}


# ---------------------------------------------------------
# Reload aliases for the current directory
#
# .vsetup_aliases decides which repo alias file should be
# sourced based on the current working directory.
# ---------------------------------------------------------

load_vsetup_aliases() {
    clear_vsetup_aliases

    if [[ -f "$VSETUP_ALIASES" ]]; then
        source "$VSETUP_ALIASES"
    fi
}


# =========================================================
# Auto-commit integration
# =========================================================


# ---------------------------------------------------------
# Remember which auto-commit repo this shell was previously in
#
# This lets us detect:
#
#   repo A -> outside
#   repo A -> repo B
#
# so we can tell the old repo that this shell has left.
# ---------------------------------------------------------

VSETUP_ACTIVE_AUTO_COMMIT_REPO=""


# ---------------------------------------------------------
# Find the nearest parent directory containing:
#
#   .vsetup/auto-commit/control.sh
#
# This allows auto-commit to work from subdirectories too.
#
# Example:
#
#   repo/src/components/
#
# still resolves back to:
#
#   repo/
# ---------------------------------------------------------

vsetup_find_auto_commit_repo() {
    local dir="$PWD"

    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/.vsetup/auto-commit/control.sh" ]]; then
            echo "$dir"
            return 0
        fi

        dir="$(dirname "$dir")"
    done

    return 1
}


# ---------------------------------------------------------
# Update auto-commit state for this shell
#
# This runs before every Bash prompt.
#
# If we left a repo:
#
#   control.sh leave <shell-pid>
#
# If we are inside a repo:
#
#   control.sh enter <shell-pid>
#
# control.sh itself decides whether auto-commit is enabled.
# ---------------------------------------------------------

vsetup_update_auto_commit() {
    local current_repo=""
    local old_control=""
    local current_control=""

    current_repo="$(vsetup_find_auto_commit_repo 2>/dev/null)"


    # -----------------------------------------------------
    # We left the previous repo
    # -----------------------------------------------------

    if [[ -n "$VSETUP_ACTIVE_AUTO_COMMIT_REPO" &&
          "$VSETUP_ACTIVE_AUTO_COMMIT_REPO" != "$current_repo" ]]; then

        old_control="$VSETUP_ACTIVE_AUTO_COMMIT_REPO/.vsetup/auto-commit/control.sh"

        if [[ -f "$old_control" ]]; then
            zsh "$old_control" leave "$$" >/dev/null 2>&1
        fi
    fi


    # -----------------------------------------------------
    # We are currently inside an auto-commit repo
    #
    # We call enter regardless of ENABLED=true/false.
    # control.sh owns that decision.
    # -----------------------------------------------------

    if [[ -n "$current_repo" ]]; then
        current_control="$current_repo/.vsetup/auto-commit/control.sh"

        if [[ -f "$current_control" ]]; then
            zsh "$current_control" enter "$$" >/dev/null 2>&1
        fi
    fi


    # Remember where we are for the next prompt.
    VSETUP_ACTIVE_AUTO_COMMIT_REPO="$current_repo"
}


# ---------------------------------------------------------
# Everything vsetup needs to update before each prompt
# ---------------------------------------------------------

vsetup_prompt_update() {
    load_vsetup_aliases
    vsetup_update_auto_commit
}


# =========================================================
# Initial setup when Bash starts
# =========================================================

# Load aliases immediately.
load_vsetup_aliases

# Detect whether this shell started inside an auto-commit repo.
vsetup_update_auto_commit


# =========================================================
# Prompt hook
#
# Bash runs this before showing every prompt.
#
# This means things like:
#
#   cd repo
#   cd ..
#   cd another-repo
#
# automatically update aliases and auto-commit state.
# =========================================================

PROMPT_COMMAND="vsetup_prompt_update${PROMPT_COMMAND:+;$PROMPT_COMMAND}"