# Spreetail Shared Expenses

FastAPI + PostgreSQL + SQLAlchemy (async) + Alembic + Jinja2 + HTMX.

## Setup Instructions

1. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and configure your database settings:
   ```bash
   cp .env.example .env
   ```

3. Run migrations to create the database schema:
   ```bash
   alembic upgrade head
   ```

4. Seed the database with initial currency and exchange rate records:
   ```bash
   python seed.py
   ```

5. Run the web server:
   ```bash
   uvicorn app.main:app --reload
   ```
