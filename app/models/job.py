from __future__ import annotations

from datetime import datetime

from extensions import db


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(255), nullable=True, index=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    work_mode = db.Column(db.String(50), nullable=True)
    employment_type = db.Column(db.String(50), nullable=True)
    minimum_experience = db.Column(db.String(50), nullable=True)
    maximum_experience = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    required_skills_json = db.Column(db.JSON, nullable=True)
    salary = db.Column(db.String(255), nullable=True)
    posted_date = db.Column(db.DateTime, nullable=True)
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    source_name = db.Column(db.String(150), nullable=True)
    source_url = db.Column(db.String(500), nullable=False)
    application_url = db.Column(db.String(500), nullable=True)
    reliability_status = db.Column(db.String(50), default="Needs Review")
    is_active = db.Column(db.Boolean, default=True)

    saved_jobs = db.relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan")
    matches = db.relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Job {self.company}: {self.title}>"
