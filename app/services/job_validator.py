from __future__ import annotations


class JobValidator:
    @staticmethod
    def validate(jobs: list[dict]) -> list[dict]:
        valid = []
        for job in jobs:
            url = (job.get("source_url") or job.get("application_url") or "").lower()
            if not url:
                continue
            if "payment" in (job.get("description") or "").lower():
                job["reliability_status"] = "Suspicious"
                continue
            if "bank" in (job.get("description") or "").lower() or "wire transfer" in (job.get("description") or "").lower():
                job["reliability_status"] = "Suspicious"
                continue
            job.setdefault("reliability_status", "Verified")
            valid.append(job)
        return valid
