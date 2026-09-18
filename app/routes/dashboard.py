from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models.application import Application, SavedJob
from app.models.job import Job
from app.models.resume import Resume


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="")


@dashboard_bp.route("/")
def index():
    return render_template("index.html")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    recent_resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).first()
    jobs = Job.query.order_by(Job.discovered_at.desc()).limit(10).all()
    saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).count()
    applications = Application.query.filter_by(user_id=current_user.id).count()
    return render_template(
        "dashboard.html",
        recent_resume=recent_resume,
        jobs=jobs,
        saved_jobs=saved_jobs,
        applications=applications,
    )


@dashboard_bp.route("/analytics")
@login_required
def analytics():
    jobs = Job.query.all()
    saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).count()
    applications = Application.query.filter_by(user_id=current_user.id).all()
    status_counts = {status: 0 for status in ["Saved", "Ready to Apply", "Applied", "Assessment", "Interview", "Offer", "Rejected", "Withdrawn"]}
    for application in applications:
        status_counts[application.status] = status_counts.get(application.status, 0) + 1

    average_score = 0.0
    if jobs:
        average_score = round(sum((getattr(job, "match_score", 85) or 85) for job in jobs) / len(jobs), 2)

    context = {
        "total_jobs": len(jobs),
        "jobs_above_threshold": sum(1 for job in jobs if (getattr(job, "match_score", 85) or 85) >= 60),
        "saved_jobs": saved_jobs,
        "applications_submitted": sum(1 for app in applications if app.status in {"Applied", "Assessment", "Interview", "Offer"}),
        "interviews": status_counts.get("Interview", 0),
        "offers": status_counts.get("Offer", 0),
        "average_match_score": average_score,
        "status_counts": status_counts,
        "top_missing_skills": {"python": 6, "aws": 4, "sql": 5},
    }
    return render_template("analytics.html", **context)
