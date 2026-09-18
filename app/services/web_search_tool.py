from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import quote_plus, urlparse

import requests


class WebSearchTool:
    """Small search abstraction that uses Tavily/Serper when configured, otherwise returns a safe fallback list."""

    PLATFORMS = {
        "LinkedIn": "linkedin.com/jobs",
        "Indeed": "indeed.com/viewjob",
        "Workday": "myworkdayjobs.com",
        "Naukri": "naukri.com/job-listings",
        "Glassdoor": "glassdoor.com/Job",
        "ZipRecruiter": "ziprecruiter.com/jobs",
        "Wellfound": "wellfound.com/jobs",
    }

    def __init__(self, provider: str | None = None, api_key: str | None = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER") or "tavily").lower()
        self.api_key = api_key or os.getenv("TAVILY_API_KEY") or os.getenv("SERPER_API_KEY")

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        if self.provider == "tavily" and os.getenv("TAVILY_API_KEY"):
            searcher = self._search_tavily
        elif self.provider == "serper" and os.getenv("SERPER_API_KEY"):
            searcher = self._search_serper
        else:
            return self._fallback_search(query, limit)

        per_platform = max(1, (limit + len(self.PLATFORMS) - 1) // len(self.PLATFORMS))
        jobs = []
        for platform, domain in self.PLATFORMS.items():
            jobs.extend(searcher(f"site:{domain} {query}", per_platform, platform))

        unique_jobs = {}
        for job in jobs:
            url = job.get("application_url") or job.get("source_url")
            if url and url not in unique_jobs:
                unique_jobs[url] = job
        return list(unique_jobs.values())[:limit] or self._fallback_search(query, limit)

    def _search_tavily(self, query: str, limit: int, platform: str = "Public listing") -> list[dict[str, Any]]:
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": os.getenv("TAVILY_API_KEY"), "query": query, "max_results": limit},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            return [self._normalize_result(item, query, platform, "tavily") for item in payload.get("results", [])]
        except Exception:
            return []

    def _search_serper(self, query: str, limit: int, platform: str = "Public listing") -> list[dict[str, Any]]:
        try:
            response = requests.get(
                "https://google.serper.dev/search",
                params={"q": query, "num": limit},
                headers={"X-API-KEY": os.getenv("SERPER_API_KEY"), "Content-Type": "application/json"},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            return [self._normalize_result(item, query, platform, "serper") for item in payload.get("organic", [])]
        except Exception:
            return []

    @staticmethod
    def _normalize_result(item: dict[str, Any], query: str, platform: str, provider: str) -> dict[str, Any]:
        result_url = item.get("url") if provider == "tavily" else item.get("link")
        result_url = result_url or WebSearchTool._job_board_url(query)
        return {
            "title": item.get("title") or "Role",
            "company": item.get("source") or platform,
            "source_name": platform or WebSearchTool._source_name(result_url),
            "location": item.get("location") or "Remote",
            "work_mode": "remote",
            "employment_type": "full-time",
            "description": item.get("content") or item.get("snippet") or "",
            "source_url": result_url,
            "application_url": item.get("application_url") or item.get("apply_url") or item.get("job_url") or result_url,
            "required_skills": [],
            "posted_date": None,
        }

    @staticmethod
    def _source_name(url: str) -> str:
        hostname = urlparse(url).netloc.lower().removeprefix("www.")
        return hostname.split(".")[0].title() or "Public listing"

    def _fallback_search(self, query: str, limit: int) -> list[dict[str, Any]]:
        fallback_url = self._job_board_url(query)
        sample_jobs = [
            {
                "title": "Python Software Engineer",
                "company": "Northstar Labs",
                "source_name": "LinkedIn search",
                "location": "Remote",
                "work_mode": "remote",
                "employment_type": "full-time",
                "description": "Build backend services, APIs, and cloud-native features in Python and Flask.",
                "source_url": fallback_url,
                "application_url": fallback_url,
                "required_skills": ["python", "flask", "sql", "api"],
                "posted_date": None,
            },
            {
                "title": "Data Engineer",
                "company": "Vertex Analytics",
                "source_name": "LinkedIn search",
                "location": "Hybrid",
                "work_mode": "hybrid",
                "employment_type": "full-time",
                "description": "Build data pipelines and dashboards using SQL, Python, and cloud technologies.",
                "source_url": fallback_url,
                "application_url": fallback_url,
                "required_skills": ["python", "sql", "data", "etl"],
                "posted_date": None,
            },
            {
                "title": "Backend Engineer",
                "company": "Helio Systems",
                "source_name": "LinkedIn search",
                "location": "Remote",
                "work_mode": "remote",
                "employment_type": "full-time",
                "description": "Develop REST APIs, integrate data services, and improve platform resiliency.",
                "source_url": fallback_url,
                "application_url": fallback_url,
                "required_skills": ["python", "api", "sql", "docker"],
                "posted_date": None,
            },
        ]
        return sample_jobs[:limit]

    @staticmethod
    def _job_board_url(query: str) -> str:
        return f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(query)}"
