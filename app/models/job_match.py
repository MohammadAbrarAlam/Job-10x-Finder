from __future__ import annotations

from datetime import datetime

from extensions import db


class JobMatch(db.Model):
    __tablename__ = "job_matches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    overall_score = db.Column(db.Float, nullable=False, default=0.0)
    skill_score = db.Column(db.Float, nullable=False, default=0.0)
    role_score = db.Column(db.Float, nullable=False, default=0.0)
    experience_score = db.Column(db.Float, nullable=False, default=0.0)
    education_score = db.Column(db.Float, nullable=False, default=0.0)
    project_score = db.Column(db.Float, nullable=False, default=0.0)
    location_score = db.Column(db.Float, nullable=False, default=0.0)
    matched_skills_json = db.Column(db.JSON, nullable=True)
    missing_skills_json = db.Column(db.JSON, nullable=True)
    explanation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="job_matches")
    resume = db.relationship("Resume", back_populates="job_matches")
    job = db.relationship("Job", back_populates="matches")

    def __repr__(self) -> str:
        return f"<JobMatch {self.id}: {self.overall_score}>"
