#!/usr/bin/env python3

import re
import sys
from pathlib import Path


ALIASES_FILE = (
    Path.home()
    / "vsetup/config/.vsetup_aliases"
)


def make_names(root: Path):
    dir_name = root.name

    var_name = re.sub(
        r"[^A-Z0-9_]",
        "_",
        dir_name.upper(),
    )

    func_name = re.sub(
        r"[^a-z0-9_]",
        "_",
        dir_name.lower(),
    )

    return var_name, func_name


def make_alias_block(root: Path) -> str:
    repo_aliases = root / ".vsetup/aliases.sh"

    var_name, func_name = make_names(root)

    start_marker = (
        f"# ---------- vsetup:repo:start {root} ----------"
    )

    end_marker = (
        f"# ---------- vsetup:repo:end {root} ----------"
    )

    return f"""{start_marker}

{var_name}_DIR="{root}"
{var_name}_ALIASES="{repo_aliases}"

load_{func_name}_aliases() {{
    if [[ "$PWD" == "${var_name}_DIR" || "$PWD" == "${var_name}_DIR/"* ]]; then
        source "${var_name}_ALIASES"
    fi
}}

load_{func_name}_aliases

{end_marker}
"""


def register_aliases(root: Path):
    ALIASES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not ALIASES_FILE.exists():
        ALIASES_FILE.write_text(
            "",
            encoding="utf-8",
        )

    text = ALIASES_FILE.read_text(
        encoding="utf-8"
    )

    start_marker = (
        f"# ---------- vsetup:repo:start {root} ----------"
    )

    if start_marker in text:
        print("Aliases already registered.")
        return

    block = make_alias_block(root).strip()

    if text.strip():
        new_text = (
            text.strip()
            + "\n\n"
            + block
            + "\n"
        )
    else:
        new_text = block + "\n"

    ALIASES_FILE.write_text(
        new_text,
        encoding="utf-8",
    )

    print("Registered aliases for:")
    print(root)
    
def main():
    if len(sys.argv) != 2:
        print(
            "Usage: register_aliases.py <repo>",
            file=sys.stderr,
        )
        raise SystemExit(1)

    root = Path(sys.argv[1])

    register_aliases(root)


if __name__ == "__main__":
    main()