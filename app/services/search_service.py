from __future__ import annotations

from typing import Any

from app.services.matching_service import MatchingService
from app.services.web_search_tool import WebSearchTool
from app.models.job import Job
from app.models.job_match import JobMatch
from extensions import db


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

    def save_matches(self, profile: dict[str, Any], filters: dict[str, Any], user_id: int, resume_id: int) -> int:
        saved_count = 0
        for job_data in self.search(profile, filters):
            score = MatchingService.calculate(profile, job_data)
            source_url = job_data.get("source_url") or job_data.get("application_url")
            job = Job.query.filter_by(source_url=source_url).first()
            if not job:
                job = Job(
                    title=job_data.get("title") or "Role",
                    company=job_data.get("company") or "Unknown",
                    location=job_data.get("location") or "Remote",
                    work_mode=job_data.get("work_mode") or "remote",
                    employment_type=job_data.get("employment_type") or "full-time",
                    description=job_data.get("description") or "",
                    required_skills_json=job_data.get("required_skills") or profile.get("skills", [])[:5],
                    source_name=job_data.get("source_name") or job_data.get("company") or "Public listing",
                    source_url=source_url,
                    application_url=(
                        job_data.get("application_url")
                        or job_data.get("apply_url")
                        or job_data.get("job_url")
                        or source_url
                    ),
                    reliability_status=job_data.get("reliability_status") or "Needs Review",
                    is_active=True,
                )
                db.session.add(job)
                db.session.flush()

            existing_match = JobMatch.query.filter_by(user_id=user_id, job_id=job.id).first()
            if not existing_match:
                db.session.add(JobMatch(
                    user_id=user_id,
                    resume_id=resume_id,
                    job_id=job.id,
                    overall_score=score["overall_score"],
                    skill_score=score["skill_score"],
                    role_score=score["role_score"],
                    experience_score=score["experience_score"],
                    education_score=score["education_score"],
                    project_score=score["project_score"],
                    location_score=score["location_score"],
                    matched_skills_json=score["matched_skills"],
                    missing_skills_json=score["missing_skills"],
                    explanation=score["explanation"],
                ))
                saved_count += 1

        db.session.commit()
        return saved_count
