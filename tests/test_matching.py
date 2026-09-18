from app.services.matching_service import MatchingService


def test_matching_service_returns_score_and_missing_skills():
    profile = {"skills": ["python", "flask", "sql"]}
    job = {"required_skills": ["python", "flask", "javascript"]}

    result = MatchingService.calculate(profile, job)

    assert result["overall_score"] > 0
    assert "javascript" in result["missing_skills"]
    assert "python" in result["matched_skills"]
