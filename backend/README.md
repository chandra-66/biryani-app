# Biryani App Backend

This project implements a FastAPI-based backend for a biryani ordering platform with authentication, restaurant management, cart, orders, payments, and review workflows.

## Stack
- Python 3.12+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL (primary) / SQLite (tests and local dev fallback)
- Alembic migrations
- JWT auth with Argon2 password hashing

## Quick start

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Copy environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
4. Run the API:
   ```bash
   cd backend && uvicorn app.main:app --reload
   ```
5. Open docs at http://localhost:8000/docs

## Database migration

```bash
cd backend
alembic upgrade head
```

## Testing

```bash
cd backend
pytest -q
```
