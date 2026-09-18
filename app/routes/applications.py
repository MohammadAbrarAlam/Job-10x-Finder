from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app.models.application import Application
from app.models.job import Job
from extensions import db

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")


@applications_bp.route("")
@login_required
def tracker():
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template("applications/tracker.html", applications=applications)


@applications_bp.route("/<int:application_id>/status", methods=["POST"])
@login_required
def update_status(application_id: int):
    application = Application.query.filter_by(id=application_id, user_id=current_user.id).first_or_404()
    status = request.form.get("status")
    if status:
        application.status = status
        application.updated_at = db.func.now()
        db.session.commit()
        flash("Application status updated.", "success")
    return redirect(url_for("applications.tracker"))
