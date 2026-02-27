# Student Feedback Management System

Flask-based web application for collecting student course feedback and enabling admins to review submissions and logs.

## Features
- Student registration and login with hashed passwords.
- Course feedback submission with duplicate-prevention per student/course.
- Admin registration and login.
- Admin feedback dashboard with search.
- In-app log viewing and log download.

## Project Structure
- `app.py`: Flask application entrypoint and blueprint registration.
- `routes/`: Route handlers for student, feedback, and admin workflows.
- `models/`: Data-access and domain logic for students, admins, feedback, DB, and logging.
- `utils/`: Shared decorators/utilities (auth and file helpers).
- `templates/`: Jinja templates for all pages.
- `logs/`: Runtime log files (created automatically).

## Requirements
- Python 3.10+ (3.12 tested in this repo).
- MySQL server with required schema/tables:
  - `student`
  - `admins`
  - `courses`
  - `feedback`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration
Create `.env` in project root:

```env
SECRET_KEY=your_secret_key
```

Database credentials are currently provided in `models/database.py` defaults. For production, move them to environment variables.

## Run Locally

```bash
python app.py
```

App runs on:
- `http://127.0.0.1:5000` (default local)
- or on `$PORT` when deployed.

## Main URLs
- `/` home page
- `/student/register`
- `/student/login`
- `/feedback/submit_feedback`
- `/admin/register`
- `/admin/login`
- `/admin/view_feedback`
- `/admin/logs`

## Deployment
`Procfile` uses:

```bash
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

If deploying with this `Procfile`, ensure a `wsgi.py` exposing `app` exists, or change command to point to `app:app`.

## Logging
- App logs are written to `logs/app.log`.
- Admin can view logs from `/admin/logs` and download via `/admin/download_logs`.

## Notes
- This project uses simple server-rendered templates and session auth.
- Passwords are hashed with Werkzeug security helpers.
- Keep `.env` out of version control (already ignored).
