import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    database_url = os.getenv("DATABASE_URL", "sqlite:///instance/jobfinder.db")
    if database_url.startswith("sqlite:///"):
        relative_path = database_url.replace("sqlite:///", "", 1)
        if not Path(relative_path).is_absolute():
            database_url = f"sqlite:///{str((BASE_DIR / relative_path).resolve())}"
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))
    UPLOAD_FOLDER = BASE_DIR / "uploads" / "resumes"
    ALLOWED_EXTENSIONS = {ext.strip().lower() for ext in os.getenv("ALLOWED_RESUME_EXTENSIONS", "pdf,docx,txt").split(",") if ext.strip()}
    JOB_SEARCH_RESULT_LIMIT = int(os.getenv("JOB_SEARCH_RESULT_LIMIT", 20))
    MINIMUM_MATCH_SCORE = int(os.getenv("MINIMUM_MATCH_SCORE", 60))
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini/gemini-2.5-flash")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


config = Config()
