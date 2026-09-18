from __future__ import annotations


class CareerAdvisorAgent:
    """Career guidance and cover-letter helper."""

    def generate_cover_letter(self, profile: dict, job: dict) -> str:
        return (
            f"Dear Hiring Manager,\n\nI am excited to apply for the {job.get('title', 'role')} position at {job.get('company', 'your company')}. "
            f"My background in {', '.join(profile.get('skills', [])[:3]) or 'software engineering'} aligns with this opportunity. "
            "I look forward to discussing how I can contribute to your team.\n\nSincerely,\n{profile.get('candidate_name', 'Candidate')}"
        )

    def recommend_strategy(self, profile: dict, job: dict) -> str:
        return "Tailor your resume to the role requirements, emphasize measurable impact, and prepare a concise portfolio example."
