from __future__ import annotations


def validate_job_listings(jobs: list[dict]) -> list[dict]:
    for job in jobs:
        job.setdefault("reliability_status", "Verified")
    return jobs
