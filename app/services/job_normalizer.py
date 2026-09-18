from __future__ import annotations

from datetime import datetime


class JobNormalizer:
    @staticmethod
    def normalize(job: dict) -> dict:
        normalized = dict(job)
        normalized["title"] = (normalized.get("title") or "Unknown role").strip()
        normalized["company"] = (normalized.get("company") or "Unknown company").strip()
        normalized["location"] = normalized.get("location") or "Remote"
        normalized["work_mode"] = normalized.get("work_mode") or "remote"
        normalized["employment_type"] = normalized.get("employment_type") or "full-time"
        normalized["source_url"] = normalized.get("source_url") or normalized.get("application_url") or "https://example.com"
        normalized["application_url"] = normalized.get("application_url") or normalized.get("source_url") or "https://example.com"
        normalized["discovered_at"] = datetime.utcnow()
        normalized["reliability_status"] = normalized.get("reliability_status") or "Needs Review"
        return normalized
