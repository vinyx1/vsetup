# lib/jsonc/inspect.py

from .parser import strip_jsonc_comments

def has_jsonc_content(text: str) -> bool:
    """
    Return True if the text contains anything other than
    comments and whitespace.
    """

    cleaned = strip_jsonc_comments(text)

    return bool(cleaned.strip())

def find_last_significant_index(text: str):
    """
    Find the index of the last non-whitespace, non-comment character.

    Supports:
      - // line comments
      - /* block comments */
      - quoted strings
      - escaped characters inside strings
    """

    opening = text.find("[")

    if opening == -1:
        return None

    i = opening + 1

    in_string = False
    escaped = False
    in_line_comment = False
    in_block_comment = False

    last_index = None

    while i < len(text):
        char = text[i]

        # ---------------- Line comment ----------------

        if in_line_comment:
            if char == "\n":
                in_line_comment = False

            i += 1
            continue

        # ---------------- Block comment ----------------

        if in_block_comment:
            if (
                char == "*"
                and i + 1 < len(text)
                and text[i + 1] == "/"
            ):
                in_block_comment = False
                i += 2
            else:
                i += 1

            continue

        # ---------------- String ----------------

        if in_string:
            last_index = i

            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False

            i += 1
            continue

        # ---------------- Normal text ----------------

        if char == '"':
            in_string = True
            last_index = i
            i += 1
            continue

        # Start of // comment
        if (
            char == "/"
            and i + 1 < len(text)
            and text[i + 1] == "/"
        ):
            in_line_comment = True
            i += 2
            continue

        # Start of /* comment
        if (
            char == "/"
            and i + 1 < len(text)
            and text[i + 1] == "*"
        ):
            in_block_comment = True
            i += 2
            continue

        # Ignore whitespace
        if not char.isspace():
            last_index = i

        i += 1

    return last_index