from __future__ import annotations

from typing import Any

from app.services.matching_service import MatchingService
from app.services.web_search_tool import WebSearchTool


class SearchService:
    """Public job search and filtering service aligned to the resume profile."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.search_tool = WebSearchTool()

    def search(self, profile: dict[str, Any], filters: dict[str, Any]) -> list[dict[str, Any]]:
        role = (profile.get("preferred_roles") or [filters.get("job_title", "software engineer")])[0]
        location = filters.get("preferred_place") or profile.get("location") or "remote"
        skills = ", ".join(profile.get("skills", [])[:5]) or "python"
        query = f"{role} {skills} {location} jobs"

        raw_jobs = self.search_tool.search(query, limit=int(filters.get("max_results", 10) or 10))
        matched_jobs = []
        min_match = float(filters.get("min_match", 0) or 0)

        for job in raw_jobs:
            job_title = str(job.get("title") or "").lower()
            role_match = role.lower() in job_title or any(keyword.lower() in job_title for keyword in profile.get("job_titles", []))
            if not role_match and profile.get("preferred_roles"):
                continue
            score = MatchingService.calculate(profile, job)
            job["match_score"] = score["overall_score"]
            job["matched_skills"] = score["matched_skills"]
            job["missing_skills"] = score["missing_skills"]
            job["reliability_status"] = "Verified" if score["overall_score"] >= 50 else "Needs Review"
            job["required_skills"] = job.get("required_skills") or list(profile.get("skills", [])[:5])
            if score["overall_score"] >= min_match:
                matched_jobs.append(job)

        matched_jobs.sort(key=lambda item: float(item.get("match_score", 0) or 0), reverse=True)
        return matched_jobs
