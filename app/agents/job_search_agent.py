from __future__ import annotations

from typing import Any


class JobSearchAgent:
    """Search-agent wrapper for query building and retrieval orchestration."""

    def __init__(self, search_service: Any | None = None):
        self.search_service = search_service

    def build_queries(self, profile: dict[str, Any], filters: dict[str, Any]) -> list[str]:
        title = (profile.get("preferred_roles") or [filters.get("job_title", "software engineer")])[0]
        location = filters.get("preferred_place") or profile.get("location") or "remote"
        return [
            f'{title} {location} {filters.get("employment_type", "full-time")} jobs',
            f'{title} remote {filters.get("skills", "python")} engineer',
        ]

    def search(self, profile: dict[str, Any], filters: dict[str, Any]) -> list[dict[str, Any]]:
        if self.search_service is None:
            return []
        return self.search_service.search(profile, filters)
