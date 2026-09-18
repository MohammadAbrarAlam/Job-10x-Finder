from __future__ import annotations

from urllib.parse import quote_plus

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.models.application import Application, SavedJob
from app.models.job import Job
from app.models.job_match import JobMatch
from app.models.resume import Resume
from app.services.matching_service import MatchingService
from app.services.search_service import SearchService
from extensions import db

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")


def _job_board_url(job_data: dict) -> str:
    query = " ".join(
        value for value in (job_data.get("title"), job_data.get("company"), job_data.get("location")) if value
    )
    return f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(query or 'jobs')}"


@jobs_bp.route("/search", methods=["GET", "POST"])
@login_required
def search_jobs():
    if request.method == "POST":
        latest_resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).first()
        profile = latest_resume.candidate_profile_json if latest_resume and latest_resume.candidate_profile_json else {
            "skills": ["python", "sql", "flask"],
            "preferred_roles": ["software engineer"],
            "location": "remote",
        }

        filters = {
            "job_title": request.form.get("job_title") or (profile.get("preferred_roles") or ["software engineer"])[0],
            "preferred_place": request.form.get("preferred_place") or profile.get("location") or "remote",
            "skills": request.form.get("skills") or ", ".join(profile.get("skills", [])[:5]),
            "min_match": request.form.get("min_match") or 60,
            "max_results": request.form.get("max_results") or 10,
            "employment_type": request.form.get("employment_type") or "full-time",
            "work_mode": request.form.get("work_mode") or "remote",
        }

        search_service = SearchService()
        jobs_data = search_service.search(profile, filters)
        for job_data in jobs_data:
            match_result = MatchingService.calculate(profile, job_data)
            application_url = (
                job_data.get("application_url")
                or job_data.get("apply_url")
                or job_data.get("job_url")
                or job_data.get("source_url")
                or _job_board_url(job_data)
            )
            source_url = job_data.get("source_url") or application_url
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
                    application_url=application_url,
                    reliability_status=job_data.get("reliability_status") or "Verified",
                    is_active=True,
                )
                db.session.add(job)
                db.session.commit()

            job_match = JobMatch(
                user_id=current_user.id,
                resume_id=latest_resume.id if latest_resume else 1,
                job_id=job.id,
                overall_score=match_result["overall_score"],
                skill_score=match_result["skill_score"],
                role_score=match_result["role_score"],
                experience_score=match_result["experience_score"],
                education_score=match_result["education_score"],
                project_score=match_result["project_score"],
                location_score=match_result["location_score"],
                matched_skills_json=match_result["matched_skills"],
                missing_skills_json=match_result["missing_skills"],
                explanation=match_result["explanation"],
            )
            existing_match = JobMatch.query.filter_by(user_id=current_user.id, job_id=job.id).first()
            if not existing_match:
                db.session.add(job_match)
                db.session.commit()

        flash("Relevant jobs discovered from the resume profile and public search sources.", "success")
        return redirect(url_for("jobs.results"))
    return render_template("jobs/search.html")


@jobs_bp.route("/results")
@login_required
def results():
    jobs = Job.query.order_by(Job.id.desc()).all()
    for job in jobs:
        latest_match = JobMatch.query.filter_by(job_id=job.id, user_id=current_user.id).order_by(JobMatch.created_at.desc()).first()
        if latest_match:
            job.match_score = latest_match.overall_score
            job.matched_skills = latest_match.matched_skills_json or []
            job.missing_skills = latest_match.missing_skills_json or []
    return render_template("jobs/results.html", jobs=jobs)


@jobs_bp.route("/<int:job_id>")
@login_required
def job_detail(job_id: int):
    job = Job.query.get_or_404(job_id)
    match = JobMatch.query.filter_by(job_id=job.id, user_id=current_user.id).order_by(JobMatch.created_at.desc()).first()
    return render_template("jobs/details.html", job=job, match=match)


@jobs_bp.route("/<int:job_id>/save", methods=["POST"])
@login_required
def save_job(job_id: int):
    job = Job.query.get_or_404(job_id)
    existing = SavedJob.query.filter_by(user_id=current_user.id, job_id=job.id).first()
    if not existing:
        saved = SavedJob(user_id=current_user.id, job_id=job.id)
        db.session.add(saved)
        db.session.commit()
        flash("Job saved successfully.", "success")
    else:
        flash("This job is already saved.", "info")
    return redirect(url_for("jobs.results"))


@jobs_bp.route("/<int:job_id>/reject", methods=["POST"])
@login_required
def reject_job(job_id: int):
    job = Job.query.get_or_404(job_id)
    flash(f"Job rejected: {job.title}", "warning")
    return redirect(url_for("jobs.results"))


@jobs_bp.route("/<int:job_id>/cover-letter", methods=["POST"])
@login_required
def cover_letter(job_id: int):
    job = Job.query.get_or_404(job_id)
    flash(f"Cover letter requested for {job.title}.", "success")
    return redirect(url_for("jobs.job_detail", job_id=job.id))


@jobs_bp.route("/<int:job_id>/apply")
@login_required
def apply_job(job_id: int):
    job = Job.query.get_or_404(job_id)
    application = Application.query.filter_by(user_id=current_user.id, job_id=job.id).first()
    if not application:
        application = Application(user_id=current_user.id, job_id=job.id, status="Ready to Apply")
        db.session.add(application)
        db.session.commit()
    flash(f"Opening application page for {job.company}.", "info")
    return redirect(job.application_url or job.source_url)
