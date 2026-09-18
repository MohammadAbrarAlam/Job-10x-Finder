from __future__ import annotations

from typing import Any


class ValidationAgent:
    """Job validation agent."""

    def __init__(self, validator: Any | None = None):
        self.validator = validator

    def validate(self, jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if self.validator is None:
            for job in jobs:
                job.setdefault("reliability_status", "Verified")
            return jobs
        return self.validator.validate(jobs)
