# 10xJobFinder

10xJobFinder is an AI-powered job search and resume matching app built with Flask, SQLite, and CrewAI. The platform helps candidates upload a resume, discover recent and relevant jobs, score the match against each vacancy, and track applications without submitting anything without explicit user confirmation.

## Features

- Resume upload for PDF, DOCX, and TXT files
- AI-powered extraction of resume details with structured candidate profiles
- Search for relevant jobs from public sources and official career pages
- Job validation and duplicate detection
- Deterministic resume-to-job scoring with explainable match feedback
- Work mode and employment filter support
- Saved jobs and application tracker
- Cover letter generation guidance and resume improvement suggestions
- Responsive dashboard and analytics

## Architecture

The project follows a modular Flask architecture with separated service, model, route, task, and agent layers. Core logic is split between deterministic Python services and CrewAI orchestration for reasoning and recommendations.

## Agents and responsibilities

- Resume Analyzer Agent: extracts structured candidate profile data from uploaded resumes
- Job Search Agent: creates search queries and pulls recent jobs from public sources
- Job Validation Agent: checks source reliability and filters suspicious listings
- Resume Matching Agent: calculates scores and identifies missing skills
- Career Advisor Agent: ranks jobs and creates cover-letter guidance
- Application Tracking Agent: manages saved jobs and application status tracking

## Folder structure

```text
10xJobFinder/
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Procfile
├── README.md
├── migrations/
├── instance/
│   └── jobfinder.db
├── uploads/
│   └── resumes/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── resume.py
│   │   ├── job.py
│   │   ├── job_match.py
│   │   └── application.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── resume.py
│   │   ├── jobs.py
│   │   ├── applications.py
│   │   └── api.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── crew.py
│   │   ├── resume_agent.py
│   │   ├── job_search_agent.py
│   │   ├── validation_agent.py
│   │   ├── matching_agent.py
│   │   ├── career_advisor_agent.py
│   │   └── tracking_agent.py
│   ├── tasks/
│   │   ├── resume_tasks.py
│   │   ├── search_tasks.py
│   │   ├── validation_tasks.py
│   │   └── matching_tasks.py
│   ├── services/
│   │   ├── resume_parser.py
│   │   ├── search_service.py
│   │   ├── job_normalizer.py
│   │   ├── job_validator.py
│   │   ├── matching_service.py
│   │   ├── deduplication_service.py
│   │   └── cover_letter_service.py
│   ├── utils/
│   │   ├── file_validation.py
│   │   ├── text_cleaner.py
│   │   ├── date_utils.py
│   │   ├── security.py
│   │   └── validators.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard.html
│   │   ├── resume/
│   │   │   └── details.html
│   │   ├── jobs/
│   │   │   ├── search.html
│   │   │   ├── results.html
│   │   ├── applications/
│   │   │   └── tracker.html
│   │   ├── analytics.html
│   │   └── errors/
│   │       ├── 404.html
│   │       └── 500.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   ├── main.js
│       │   ├── job-search.js
│       │   └── analytics.js
│       └── images/
├── tests/
│   ├── test_resume_parser.py
│   ├── test_matching.py
│   ├── test_routes.py
│   └── test_models.py
```

## Local installation

1. Clone the repository.
2. Create a Python 3.11+ virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy the environment template:

```bash
copy .env.example .env
```

5. Set the required API keys and configuration values in `.env`.

## API-key configuration

Set at least one supported LLM provider and one search provider:

- `GEMINI_API_KEY` with `LLM_PROVIDER=gemini`
- `OPENAI_API_KEY` with `LLM_PROVIDER=openai`
- `TAVILY_API_KEY` or `SERPER_API_KEY`

The app works as long as one supported provider is configured. It does not require hard-coded secrets.

## Database migration

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

If you are using the included SQLite setup, the app can also create tables automatically on first run.

## Running the application

```bash
set FLASK_APP=app.py
flask run
```

Or run the app directly:

```bash
python app.py
```

## Running tests

```bash
pytest -q
```

## Render deployment

This project is designed to deploy on Render using Gunicorn. Example configuration:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

Add environment variables in your Render service configuration and ensure the database directory is writable.

## Security limitations

This project does not bypass CAPTCHAs, authentication, or robots.txt restrictions. It only searches through legal public APIs and official company pages. Users are required to complete real application steps directly on the official company site.

## Ethical job-search guidelines

- Respect website terms and privacy boundaries
- Do not scrape login-protected or private content
- Never request payment or banking information from a job source
- Only use the official application page that the user chooses to open
- Prioritize transparent, legitimate, current opportunities

## Screenshots

Add screenshots here after the app is running locally.

## Future improvements

- Multi-language resume parsing
- LinkedIn and government job integrations with explicit approval
- Email-based follow-up automation
- Improved explainability and recommendations
- Advanced analytics and recruiter dashboards

## License

This project is intended for educational and internal use. Extend and adapt it according to your product requirements.
