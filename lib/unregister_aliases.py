#!/usr/bin/env python3

import re
import sys
from pathlib import Path


ALIASES_FILE = (
    Path.home()
    / "vsetup/config/.vsetup_aliases"
)

START_RE = re.compile(
    r"^# ---------- vsetup:repo:start (.+) ----------$"
)

END_RE = re.compile(
    r"^# ---------- vsetup:repo:end (.+) ----------$"
)


def parse_alias_blocks(text: str):
    """
    Parse .vsetup_aliases into a list of:

        (repo_path, block_text)

    Raises an error if the marker structure is malformed.
    """

    lines = text.splitlines(keepends=True)

    blocks = []

    current_repo = None
    current_lines = []

    for line in lines:
        stripped = line.rstrip("\n")

        start_match = START_RE.match(stripped)
        end_match = END_RE.match(stripped)

        # ---------------- Start marker ----------------

        if start_match:
            if current_repo is not None:
                raise ValueError(
                    f"Found nested alias block while parsing {current_repo}"
                )

            current_repo = start_match.group(1)
            current_lines = [line]
            continue

        # ---------------- End marker ----------------

        if end_match:
            if current_repo is None:
                raise ValueError(
                    "Found alias end marker without matching start marker"
                )

            end_repo = end_match.group(1)

            if end_repo != current_repo:
                raise ValueError(
                    f"Alias marker mismatch:\n"
                    f"start: {current_repo}\n"
                    f"end:   {end_repo}"
                )

            current_lines.append(line)

            blocks.append(
                (
                    current_repo,
                    "".join(current_lines),
                )
            )

            current_repo = None
            current_lines = []

            continue

        # ---------------- Inside block ----------------

        if current_repo is not None:
            current_lines.append(line)

    if current_repo is not None:
        raise ValueError(
            f"Alias block for {current_repo} has no end marker"
        )

    return blocks


def unregister_aliases(root: str):
    if not ALIASES_FILE.exists():
        print("Alias registry does not exist.")
        return

    text = ALIASES_FILE.read_text(
        encoding="utf-8"
    )

    blocks = parse_alias_blocks(text)

    remaining = [
        (repo, block)
        for repo, block in blocks
        if repo != root
    ]

    if len(remaining) == len(blocks):
        print("No aliases registered for:")
        print(f"  {root}")
        return

    # Canonical formatting:
    # exactly one blank line between blocks,
    # exactly one newline at EOF.
    new_text = "\n\n".join(
        block.strip()
        for _, block in remaining
    )

    if new_text:
        new_text += "\n"

    ALIASES_FILE.write_text(
        new_text,
        encoding="utf-8",
    )

    print("Unregistered aliases for:")
    print(f"  {root}")

def main():
    if len(sys.argv) != 2:
        print(
            "Usage: unregister_aliases.py <repo>",
            file=sys.stderr,
        )
        raise SystemExit(1)

    unregister_aliases(sys.argv[1])


if __name__ == "__main__":
    main()