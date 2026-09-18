from __future__ import annotations

from typing import Any

from app.agents.career_advisor_agent import CareerAdvisorAgent
from app.agents.job_search_agent import JobSearchAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.resume_agent import ResumeAnalyzerAgent
from app.agents.tracking_agent import TrackingAgent
from app.agents.validation_agent import ValidationAgent


class CrewAIOrchestrator:
    """Minimal orchestration layer for the core reasoning workflow."""

    def __init__(self, search_service: Any | None = None, validator: Any | None = None, matcher: Any | None = None):
        self.resume_agent = ResumeAnalyzerAgent()
        self.search_agent = JobSearchAgent(search_service=search_service)
        self.validation_agent = ValidationAgent(validator=validator)
        self.matching_agent = MatchingAgent(matcher=matcher)
        self.career_agent = CareerAdvisorAgent()
        self.tracking_agent = TrackingAgent()

    def run(self, resume_text: str, profile: dict[str, Any], filters: dict[str, Any]) -> dict[str, Any]:
        resume_profile = self.resume_agent.analyze(resume_text)
        resume_profile.update(profile)
        queries = self.search_agent.build_queries(resume_profile, filters)
        jobs = self.search_agent.search(resume_profile, filters) if self.search_agent.search_service else []
        validated_jobs = self.validation_agent.validate(jobs)
        scored_jobs = []
        for job in validated_jobs:
            score = self.matching_agent.score(resume_profile, job)
            scored_jobs.append({**job, **score})
        return {
            "profile": resume_profile,
            "queries": queries,
            "jobs": scored_jobs,
            "career": {
                "cover_letter": self.career_agent.generate_cover_letter(resume_profile, scored_jobs[0] if scored_jobs else {}),
                "strategy": self.career_agent.recommend_strategy(resume_profile, scored_jobs[0] if scored_jobs else {}),
            },
        }
