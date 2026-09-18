from __future__ import annotations

import hashlib
from typing import Any


def hash_value(value: Any) -> str:
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()
