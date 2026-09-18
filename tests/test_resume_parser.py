from app.services.resume_parser import ResumeParser


def test_extract_skills_detects_common_keywords():
    text = "Python Flask SQL REST API Docker AWS machine learning"
    skills = ResumeParser.extract_skills(text)
    assert "python" in skills
    assert "flask" in skills
    assert "sql" in skills


def test_extract_candidate_profile_has_expected_fields():
    profile = ResumeParser.extract_candidate_profile("John Doe\nSoftware Engineer\nLocation: Seattle, WA\npython flask sql")
    assert "candidate_name" in profile
    assert profile["location"] == "Seattle, WA"
    assert "python" in profile["skills"]
