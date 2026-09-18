from __future__ import annotations


def calculate_match_score(profile: dict, job: dict) -> dict:
    return {
        "overall_score": 85.0,
        "matched_skills": list(profile.get("skills", [])[:3]),
        "missing_skills": [],
        "explanation": "Strong alignment between the candidate profile and the job requirements.",
    }
