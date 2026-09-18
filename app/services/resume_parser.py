from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


class ResumeParser:
    @staticmethod
    def read_resume_text(file_path: str) -> str:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            reader = PdfReader(str(path))
            pages = []
            for page in reader.pages:
                text = page.extract_text() or ""
                pages.append(text)
            return "\n".join(pages)

        if suffix == ".docx":
            doc = Document(str(path))
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)

        if suffix == ".txt":
            return path.read_text(encoding="utf-8", errors="ignore")

        raise ValueError(f"Unsupported resume format: {suffix}")

    @staticmethod
    def extract_skills(text: str) -> list[str]:
        keywords = [
            "python",
            "flask",
            "django",
            "javascript",
            "react",
            "node",
            "sql",
            "postgres",
            "mysql",
            "mongodb",
            "aws",
            "docker",
            "kubernetes",
            "machine learning",
            "ai",
            "data analysis",
            "tableau",
            "power bi",
            "excel",
            "pandas",
            "scikit-learn",
            "pytorch",
            "tensorflow",
            "rest api",
        ]
        lower_text = text.lower()
        found = []
        for keyword in keywords:
            if keyword in lower_text:
                found.append(keyword)
        return sorted(set(found))

    @staticmethod
    def extract_candidate_profile(text: str) -> dict:
        skills = ResumeParser.extract_skills(text)
        email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        name_match = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text)
        location_match = re.search(r"(?:Location|Based in|City|State|Country)[:\s]+([A-Za-z ,.-]+)", text, re.I)

        return {
            "candidate_name": name_match.group(1).strip() if name_match else "Unknown",
            "email": email_match.group(0) if email_match else None,
            "phone": None,
            "location": location_match.group(1).strip() if location_match else "Unknown",
            "education": [],
            "experience_years": 0,
            "skills": skills,
            "projects": [],
            "certifications": [],
            "job_titles": ["Software Engineer"],
            "preferred_roles": ["Software Engineer"],
        }
