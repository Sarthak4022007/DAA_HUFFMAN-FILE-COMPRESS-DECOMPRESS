"""
utils.py

Small helper functions used by app.py and performance.py.
Kept separate so the algorithm files (huffman.py, baseline.py) stay
focused only on the DAA content.
"""

import os
import re


def format_bytes(num_bytes: int) -> str:
    """Human-readable byte size, e.g. 15234 -> '14.9 KB'."""
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{size:.2f} GB"


def safe_filename(filename: str) -> str:
    """Strip any path components and unsafe characters from a filename
    before it is used to build a path on the server."""
    filename = os.path.basename(filename)
    filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    return filename or "file"


def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)
