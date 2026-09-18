from __future__ import annotations

from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/search-status/<task_id>")
def search_status(task_id: str):
    return jsonify({"task_id": task_id, "status": "queued", "message": "This endpoint is ready for async task tracking."})
