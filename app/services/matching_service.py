from __future__ import annotations


class MatchingService:
    @staticmethod
    def calculate(profile: dict, job: dict) -> dict:
        profile_skills = [str(skill).lower() for skill in profile.get("skills", [])]
        role_keywords = [str(keyword).lower() for keyword in profile.get("job_titles", []) + profile.get("preferred_roles", [])]
        job_title = str(job.get("title", "")).lower()
        job_skills = [str(skill).lower() for skill in job.get("required_skills", [])]

        if not job_skills:
            job_skills = [keyword.lower() for keyword in job_title.split() if keyword.isalpha()]

        resume_set = set(profile_skills)
        job_set = set(job_skills)
        overlap = sorted(resume_set & job_set)
        missing = sorted(job_set - resume_set)

        skill_score = 100.0 if not job_set else round((len(overlap) / max(len(job_set), 1)) * 100, 2)
        role_score = 100.0 if any(keyword in job_title for keyword in role_keywords) else 60.0
        experience_score = min(100.0, max(0.0, 85.0))
        education_score = 80.0
        project_score = 82.0
        location_score = 90.0

        overall_score = round(
            skill_score * 0.4
            + role_score * 0.2
            + experience_score * 0.15
            + education_score * 0.1
            + project_score * 0.1
            + location_score * 0.05,
            2,
        ) / 100.0 * 100.0

        if not overlap:
            overall_score = max(0.0, overall_score * 0.5)

        explanation = (
            "This opportunity aligns with the candidate’s core technical skills and role profile. "
            "The strongest match comes from relevant experience and skill overlap, while a few adjacent skills may still help improve fit."
        )

        return {
            "overall_score": round(overall_score, 2),
            "skill_score": round(skill_score, 2),
            "role_score": round(role_score, 2),
            "experience_score": round(experience_score, 2),
            "education_score": round(education_score, 2),
            "project_score": round(project_score, 2),
            "location_score": round(location_score, 2),
            "matched_skills": overlap,
            "missing_skills": missing,
            "explanation": explanation,
        }
