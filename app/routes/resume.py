from __future__ import annotations

import uuid
from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.models.resume import Resume
from app.services.resume_parser import ResumeParser
from app.services.search_service import SearchService
from extensions import db

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")


@resume_bp.route("/upload", methods=["POST"])
@login_required
def upload_resume():
    if "resume_file" not in request.files:
        flash("No resume file was uploaded.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    file = request.files["resume_file"]
    if file.filename == "":
        flash("Please choose a valid file.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    extension = Path(file.filename).suffix.lower().lstrip(".")
    allowed = {"pdf", "docx", "txt"}
    if extension not in allowed:
        flash("Unsupported file type. Use PDF, DOCX, or TXT.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    if file.content_length and file.content_length > 5 * 1024 * 1024:
        flash("Resume file exceeds the 5 MB limit.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    upload_dir = Path("uploads") / "resumes"
    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    file_path = upload_dir / filename
    file.save(file_path)

    text = ResumeParser.read_resume_text(str(file_path))
    profile = ResumeParser.extract_candidate_profile(text)

    resume = Resume(
        user_id=current_user.id,
        original_filename=file.filename,
        stored_filename=filename,
        extracted_text=text,
        candidate_profile_json=profile,
    )
    db.session.add(resume)
    db.session.commit()

    filters = {
        "job_title": (profile.get("preferred_roles") or ["software engineer"])[0],
        "preferred_place": profile.get("location") or "remote",
        "min_match": 0,
        "max_results": 20,
    }
    recommendations = SearchService().save_matches(profile, filters, current_user.id, resume.id)
    flash(f"Resume uploaded. {recommendations} matching jobs are ready.", "success")
    return redirect(url_for("jobs.results"))


@resume_bp.route("/<int:resume_id>")
@login_required
def resume_detail(resume_id: int):
    resume = Resume.query.filter_by(id=resume_id, user_id=current_user.id).first_or_404()
    return render_template("resume/details.html", resume=resume)
