#!/bin/zsh

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"

if [[ -z "$ROOT" ]]; then
    echo "Not inside a Git repository."
    exit 1
fi

echo "Auto-commit started."
echo "Repository:"
echo "  $ROOT"
echo
echo "Checking every 2 minutes."
echo "Press Ctrl+C to stop."
echo

while true; do
    git -C "$ROOT" add . || exit 1

    if ! git -C "$ROOT" diff --cached --quiet; then
        CHANGED_COUNT="$(
            git -C "$ROOT" diff --cached --name-only \
                | wc -l \
                | tr -d ' '
        )"

        FIRST_FILE="$(
            git -C "$ROOT" diff --cached --name-only \
                | head -n 1
        )"

        if [[ "$CHANGED_COUNT" -eq 1 ]]; then
            COMMIT_MESSAGE="Auto-update $FIRST_FILE"
        else
            COMMIT_MESSAGE="Auto-update $CHANGED_COUNT files"
        fi

        #echo
        #echo "Changes detected."
        #echo "Commit:"
        #echo "  $COMMIT_MESSAGE"

        git -C "$ROOT" commit -m "$COMMIT_MESSAGE" || exit 1

        if git -C "$ROOT" remote get-url origin >/dev/null 2>&1; then
            git -C "$ROOT" push || {
                echo "Push failed."
                exit 1
            }
        fi
    fi

    sleep 120
done