import json
from pathlib import Path

# ---------------------------------------------------------
# JSONC parsing
# ---------------------------------------------------------

def strip_jsonc_comments(text: str) -> str:
    """
    Removes JSONC comments while preserving comment-like text
    inside quoted strings.

    Supports:
      - // line comments
      - /* block comments */

    Examples:
        "https://example.com"      -> preserved
        "/* not a comment */"      -> preserved
        // actual comment          -> removed
        /* actual comment */       -> removed
    """

    result = []

    in_string = False
    escaped = False
    in_block_comment = False
    i = 0

    while i < len(text):
        char = text[i]

        # ---------------- Block comment ----------------

        if in_block_comment:
            # End of /* ... */ comment
            if (
                char == "*"
                and i + 1 < len(text)
                and text[i + 1] == "/"
            ):
                in_block_comment = False
                i += 2
            else:
                # Preserve newlines so error line numbers remain useful.
                if char == "\n":
                    result.append("\n")

                i += 1

            continue

        # ---------------- JSON string ----------------

        if in_string:
            result.append(char)

            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False

            i += 1
            continue

        # ---------------- Normal text ----------------

        # Starting a string
        if char == '"':
            in_string = True
            result.append(char)
            i += 1
            continue

        # Starting a // line comment
        if (
            char == "/"
            and i + 1 < len(text)
            and text[i + 1] == "/"
        ):
            i += 2

            # Skip until newline
            while i < len(text) and text[i] != "\n":
                i += 1

            # Preserve newline
            if i < len(text):
                result.append("\n")
                i += 1

            continue

        # Starting a /* block comment */
        if (
            char == "/"
            and i + 1 < len(text)
            and text[i + 1] == "*"
        ):
            in_block_comment = True
            i += 2
            continue

        result.append(char)
        i += 1

    return "".join(result)


def strip_trailing_commas(text: str) -> str:
    """
    Removes commas immediately before } or ],
    while preserving commas inside strings.
    """

    result = []

    in_string = False
    escaped = False
    i = 0

    while i < len(text):
        char = text[i]

        if in_string:
            result.append(char)

            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False

            i += 1
            continue

        if char == '"':
            in_string = True
            result.append(char)
            i += 1
            continue

        if char == ",":
            # Look ahead past whitespace
            j = i + 1

            while j < len(text) and text[j].isspace():
                j += 1

            # Trailing comma
            if j < len(text) and text[j] in "]}":
                i += 1
                continue

        result.append(char)
        i += 1

    return "".join(result)


def load_jsonc(path: Path):
    """
    Load a vsetup keybindings JSONC file.

    Supports:
      - // comments
      - trailing commas
      - empty/comment-only files
    """

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ValueError(
            f"Could not read keybindings file {path}: {e}"
        ) from e

    text = strip_jsonc_comments(text)
    text = strip_trailing_commas(text)


    # Take care of case when the text is empty
    if not text.strip():
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid keybindings JSON in {path}\n"
            f"Line {e.lineno}, column {e.colno}: {e.msg}"
        ) from e

    if not isinstance(data, list):
        raise ValueError(
            f"{path}: keybindings file must contain a top-level JSON array"
        )

    return data