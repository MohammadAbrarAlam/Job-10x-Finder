from __future__ import annotations


class TrackingAgent:
    """Application tracking orchestration wrapper."""

    def __init__(self, repo=None):
        self.repo = repo

    def save_application(self, *args, **kwargs):
        return {"status": "saved"}
