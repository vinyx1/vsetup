# lib/jsonc/__init__.py
from .parser import load_jsonc
from .inspect import (
    has_jsonc_content,
    find_last_significant_index,
)