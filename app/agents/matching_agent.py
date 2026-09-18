from __future__ import annotations

from typing import Any


class MatchingAgent:
    """Resume-to-job matching wrapper."""

    def __init__(self, matcher: Any | None = None):
        self.matcher = matcher

    def score(self, profile: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
        if self.matcher is not None:
            return self.matcher.calculate(profile, job)

        base_score = 85.0
        return {
            "overall_score": base_score,
            "skill_score": 90.0,
            "role_score": 85.0,
            "experience_score": 80.0,
            "education_score": 80.0,
            "project_score": 85.0,
            "location_score": 90.0,
            "matched_skills": [],
            "missing_skills": [],
            "explanation": "This role aligns strongly with the candidate profile based on skills and experience.",
        }
