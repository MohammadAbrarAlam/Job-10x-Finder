from __future__ import annotations

from typing import Any


class ResumeAnalyzerAgent:
    """Structured resume analysis wrapper."""

    def __init__(self, llm_client: Any | None = None):
        self.llm_client = llm_client

    def analyze(self, text: str) -> dict[str, Any]:
        normalized = text.strip()
        lower = normalized.lower()
        skill_keywords = [
            "python",
            "flask",
            "sql",
            "javascript",
            "react",
            "aws",
            "docker",
            "kubernetes",
            "machine learning",
            "ai",
            "data analysis",
            "sqlalchemy",
            "rest api",
        ]
        found = sorted({skill for skill in skill_keywords if skill in lower})
        return {
            "candidate_name": "Unknown",
            "email": None,
            "phone": None,
            "location": "Unknown",
            "education": [],
            "experience_years": 0,
            "skills": found,
            "projects": [],
            "certifications": [],
            "job_titles": ["Software Engineer"],
            "preferred_roles": ["Software Engineer"],
        }
