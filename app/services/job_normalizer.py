from __future__ import annotations

from datetime import datetime
from urllib.parse import quote_plus


class JobNormalizer:
    @staticmethod
    def normalize(job: dict) -> dict:
        normalized = dict(job)
        normalized["title"] = (normalized.get("title") or "Unknown role").strip()
        normalized["company"] = (normalized.get("company") or "Unknown company").strip()
        normalized["location"] = normalized.get("location") or "Remote"
        normalized["work_mode"] = normalized.get("work_mode") or "remote"
        normalized["employment_type"] = normalized.get("employment_type") or "full-time"
        fallback_url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(normalized['title'])}"
        application_url = (
            normalized.get("application_url")
            or normalized.get("apply_url")
            or normalized.get("job_url")
            or normalized.get("source_url")
            or fallback_url
        )
        normalized["application_url"] = application_url
        normalized["source_url"] = normalized.get("source_url") or application_url
        normalized["discovered_at"] = datetime.utcnow()
        normalized["reliability_status"] = normalized.get("reliability_status") or "Needs Review"
        return normalized
