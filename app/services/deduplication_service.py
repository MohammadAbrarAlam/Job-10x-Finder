from __future__ import annotations


class DeduplicationService:
    @staticmethod
    def normalize_key(job: dict) -> str:
        company = (job.get("company") or "").strip().lower()
        title = (job.get("title") or "").strip().lower()
        location = (job.get("location") or "").strip().lower()
        source_url = (job.get("source_url") or job.get("application_url") or "").strip().lower()
        return f"{company}|{title}|{location}|{source_url}"

    @staticmethod
    def remove_duplicates(jobs: list[dict]) -> list[dict]:
        seen = set()
        unique = []
        for job in jobs:
            key = DeduplicationService.normalize_key(job)
            if key in seen:
                continue
            seen.add(key)
            unique.append(job)
        return unique
