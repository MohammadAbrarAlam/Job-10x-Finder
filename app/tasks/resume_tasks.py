from __future__ import annotations


def extract_resume_text(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return ""
