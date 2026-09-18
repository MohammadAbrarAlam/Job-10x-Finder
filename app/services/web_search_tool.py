from __future__ import annotations

import json
import os
from typing import Any

import requests


class WebSearchTool:
    """Small search abstraction that uses Tavily/Serper when configured, otherwise returns a safe fallback list."""

    def __init__(self, provider: str | None = None, api_key: str | None = None):
        self.provider = (provider or os.getenv("LLM_PROVIDER") or "tavily").lower()
        self.api_key = api_key or os.getenv("TAVILY_API_KEY") or os.getenv("SERPER_API_KEY")

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        if self.provider == "tavily" and os.getenv("TAVILY_API_KEY"):
            return self._search_tavily(query, limit)
        if self.provider == "serper" and os.getenv("SERPER_API_KEY"):
            return self._search_serper(query, limit)
        return self._fallback_search(query, limit)

    def _search_tavily(self, query: str, limit: int) -> list[dict[str, Any]]:
        try:
            response = requests.post(
                "https://api.tavily.com/search",
                json={"api_key": os.getenv("TAVILY_API_KEY"), "query": query, "max_results": limit},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            return [
                {
                    "title": item.get("title") or "Role",
                    "company": item.get("source") or "Public company",
                    "location": "Remote",
                    "work_mode": "remote",
                    "employment_type": "full-time",
                    "description": item.get("content") or item.get("snippet") or "",
                    "source_url": item.get("url") or "https://example.com",
                    "application_url": item.get("url") or "https://example.com",
                    "required_skills": [],
                    "posted_date": None,
                }
                for item in payload.get("results", [])
            ]
        except Exception:
            return self._fallback_search(query, limit)

    def _search_serper(self, query: str, limit: int) -> list[dict[str, Any]]:
        try:
            response = requests.get(
                "https://google.serper.dev/search",
                params={"q": query, "num": limit},
                headers={"X-API-KEY": os.getenv("SERPER_API_KEY"), "Content-Type": "application/json"},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            return [
                {
                    "title": item.get("title") or "Role",
                    "company": item.get("source") or "Public company",
                    "location": item.get("location") or "Remote",
                    "work_mode": "remote",
                    "employment_type": "full-time",
                    "description": item.get("snippet") or "",
                    "source_url": item.get("link") or "https://example.com",
                    "application_url": item.get("link") or "https://example.com",
                    "required_skills": [],
                    "posted_date": None,
                }
                for item in payload.get("organic", [])
            ]
        except Exception:
            return self._fallback_search(query, limit)

    def _fallback_search(self, query: str, limit: int) -> list[dict[str, Any]]:
        sample_jobs = [
            {
                "title": "Python Software Engineer",
                "company": "Northstar Labs",
                "location": "Remote",
                "work_mode": "remote",
                "employment_type": "full-time",
                "description": "Build backend services, APIs, and cloud-native features in Python and Flask.",
                "source_url": "https://example.com/jobs/python-software-engineer",
                "application_url": "https://example.com/jobs/python-software-engineer",
                "required_skills": ["python", "flask", "sql", "api"],
                "posted_date": None,
            },
            {
                "title": "Data Engineer",
                "company": "Vertex Analytics",
                "location": "Hybrid",
                "work_mode": "hybrid",
                "employment_type": "full-time",
                "description": "Build data pipelines and dashboards using SQL, Python, and cloud technologies.",
                "source_url": "https://example.com/jobs/data-engineer",
                "application_url": "https://example.com/jobs/data-engineer",
                "required_skills": ["python", "sql", "data", "etl"],
                "posted_date": None,
            },
            {
                "title": "Backend Engineer",
                "company": "Helio Systems",
                "location": "Remote",
                "work_mode": "remote",
                "employment_type": "full-time",
                "description": "Develop REST APIs, integrate data services, and improve platform resiliency.",
                "source_url": "https://example.com/jobs/backend-engineer",
                "application_url": "https://example.com/jobs/backend-engineer",
                "required_skills": ["python", "api", "sql", "docker"],
                "posted_date": None,
            },
        ]
        return sample_jobs[:limit]
