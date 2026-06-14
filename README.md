# Spreetail Shared Expenses

A full-featured shared expenses tracking and auditing web application. Built with a server-rendered modern stack: **FastAPI + PostgreSQL + SQLAlchemy 2.0 (async) + Alembic + Jinja2 + HTMX + Vanilla CSS**.

---

## 💻 Tech Stack

- **Core Framework**: FastAPI
- **Database**: PostgreSQL (with `asyncpg` driver)
- **ORM**: SQLAlchemy 2.0 (using async session management)
- **Migrations**: Alembic
- **Templating**: Jinja2 HTML templates
- **Frontend Interactivity**: HTMX (AJAX updates, dynamic form inputs, live search, and inline modal updates)
- **Styling**: Premium custom Vanilla CSS (monochrome financial layout, CSS variable design system, fully responsive)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- PostgreSQL server (or Docker installed to launch a containerized instance)

### 2. Launch PostgreSQL
If you do not have a local Postgres instance running, launch a containerized instance using Docker:
```bash
docker run --name spreetail-postgres -e POSTGRES_DB=spreetail -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
```

### 3. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file from the template:
```bash
cp .env.example .env
```
Ensure your `.env` contains the correct database URL and application secrets:
```ini
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/spreetail
SECRET_KEY=change-me-to-a-long-random-string
USD_INR_RATE=83.50
```

### 5. Run Database Migrations
Create the database tables using Alembic:
```bash
alembic upgrade head
```

### 6. Seed the Database
Initialize the database with demo currencies (INR, USD), historical exchange rates, a demo group ("Flat Expenses"), and mock users (Ipsita, Rohan, Aisha):
```bash
python seed.py
```

### 7. Run the Web Server
Launch the development server:
```bash
uvicorn app.main:app --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📂 Project Structure

```text
spreetail/
├── alembic/                 # Alembic migration environment and script history
├── app/
│   ├── auth/                # Sign up, Sign in, Cookie Sessions
│   ├── balances/            # Debt minimization algorithm, Net positions
│   ├── expenses/            # Expense creation, Splits logic
│   ├── groups/              # Group Creation, Member tracking, temporal gating
│   ├── importer/            # CSV parsing pipeline, 13 anomaly rules
│   ├── payments/            # Recording settlements between members
│   ├── database.py          # SQLAlchemy engine, get_db dependency
│   ├── deps.py              # Current user authentication dependencies
│   ├── main.py              # FastAPI main setup, exception handlers
│   └── models.py            # Unified schema models
├── static/                  # Stylesheets and static assets
├── templates/               # Jinja2 HTML layout pages and fragments
├── seed.py                  # Database seeding script
├── requirements.txt         # Pinned packages list
└── README.md
```

---

## 🧪 Verification & Testing
To verify that all files compile and dependencies resolve without issues:
```bash
python -c "from app.models import *; from app.auth.service import *; print('Imports successful')"
```
To run the automated authentication flow tests:
```bash
python scratch/test_auth.py
```
*(Note: Requires the uvicorn server to be running on port 8000)*
