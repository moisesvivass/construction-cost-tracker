# CLAUDE.md

Guidance for Claude Code working in this repo.

## Commands

```bash
# Local dev
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The app is a Flask + SQLAlchemy + Flask-Login project. Entry point is `run.py` which calls `app/__init__.py:create_app`.

## Railway Memory Budget

This is a low-traffic portfolio demo. Memory hygiene matters because Railway bills per GB-minute.

Rules baked into `Procfile`:
- `--workers 1` — single gunicorn worker. The default (2 × CPU + 1) wastes RAM on a service with no real traffic.
- `--max-requests 500 --max-requests-jitter 50` — recycle the worker every ~500 requests so Flask-Limiter's in-memory storage, SQLAlchemy connection pools, and any short-lived allocations get reclaimed periodically. The jitter prevents synchronized restarts across deployments.

If you ever add an `APScheduler` or any other in-process long-running task, **revisit `--max-requests`** — worker recycles will kill it. For this Flask app, there's no such task, so the recycle is safe.

## Key Conventions

- Flask-Limiter is wired in `app/__init__.py` and applied per-endpoint in `app/routes.py`. Do not switch to `default_limits` — that would store every IP that hits any endpoint indefinitely.
- Auth via Flask-Login. User model in `app/models.py`.
- CSRF enabled via Flask-WTF on all forms.
