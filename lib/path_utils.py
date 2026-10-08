import os
import sys
from pathlib import Path


def canonical_path(path: str) -> str:
    """
    Return a canonical absolute path using the filesystem's
    actual capitalization for each path component.

    Useful on case-insensitive, case-preserving filesystems
    such as the common default macOS setup.
    """

    path = os.path.abspath(
        os.path.expanduser(path)
    )

    parts = Path(path).parts

    if not parts:
        return path

    current = parts[0]

    for part in parts[1:]:
        try:
            entries = os.listdir(current)
        except OSError:
            current = os.path.join(
                current,
                part,
            )
            continue

        actual_name = next(
            (
                entry
                for entry in entries
                if entry.casefold() == part.casefold()
            ),
            part,
        )

        current = os.path.join(
            current,
            actual_name,
        )

    return os.path.realpath(current)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python3 path_utils.py <path>",
            file=sys.stderr,
        )
        raise SystemExit(1)

    print(canonical_path(sys.argv[1]))