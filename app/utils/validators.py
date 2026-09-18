from __future__ import annotations

from flask import request


def validate_required_fields(data: dict, required: list[str]) -> list[str]:
    missing = []
    for field in required:
        value = data.get(field)
        if value is None or str(value).strip() == "":
            missing.append(field)
    return missing


def ensure_safe_job_url(url: str | None) -> str | None:
    if not url:
        return None
    if not url.startswith(("http://", "https://")):
        return None
    return url
