from __future__ import annotations


class CoverLetterService:
    @staticmethod
    def build_cover_letter(candidate_profile: dict, job: dict) -> str:
        name = candidate_profile.get("candidate_name", "Candidate")
        role = job.get("title", "the role")
        company = job.get("company", "the company")
        skills = ", ".join(candidate_profile.get("skills", [])[:4]) or "relevant skills"

        return (
            f"Dear Hiring Manager,\n\n"
            f"I am writing to express my interest in the {role} position at {company}. "
            f"My experience and background in {skills} align well with the opportunity, and I am confident that I can contribute meaningfully to your team. "
            "I would welcome the chance to discuss my qualifications and how I can support the organization’s goals.\n\n"
            f"Sincerely,\n{name}"
        )
