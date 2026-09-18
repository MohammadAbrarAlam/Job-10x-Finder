from __future__ import annotations

from pathlib import Path


def is_allowed_extension(filename: str, allowed: set[str]) -> bool:
    suffix = Path(filename).suffix.lower().lstrip(".")
    return suffix in {item.lower() for item in allowed}


def is_safe_filename(filename: str) -> bool:
    return ".." not in filename and Path(filename).name == filename
