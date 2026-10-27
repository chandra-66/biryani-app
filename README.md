# Biryani App

A full-stack biryani ordering application with a React + TypeScript frontend, FastAPI backend, PostgreSQL database, and Cloudinary image storage.

## Architecture

- Frontend: React + Vite + Tailwind CSS
- Backend: Python + FastAPI + SQLAlchemy + Alembic
- Database: PostgreSQL
- Deployment: Vercel (frontend), Render (backend), Neon/Supabase (database)
- Monitoring: Sentry
- Image hosting: Cloudinary

## Local development

1. Create project environment variables:
   ```bash
   cp .env.example .env
   ```
2. Start PostgreSQL and local services:
   ```bash
   docker compose up -d db
   ```
3. Backend:
   ```bash
   cd backend
   python -m venv .venv
   . .venv/Scripts/activate
   pip install -r requirements.txt
   python -m alembic upgrade head
   uvicorn app.main:app --reload
   ```
4. Frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
5. Open the customer storefront at http://localhost:5173 and the shop owner dashboard at http://localhost:5173/restaurant.html. API docs are at http://localhost:8000/docs.

## Storefront demo

The customer storefront and the shop owner's separate order dashboard are served by Vite from the project root. Incoming order notifications and accept/reject/preparation/completion controls appear only in the owner dashboard. The standalone demo shares orders between both pages using browser storage, so run `npm run dev` from `frontend` and open both pages on the same origin; do not open the HTML files directly. Demo orders are stored in that browser and are not yet connected to the backend or protected by owner authentication.

## Deployment

- Frontend: deploy the `frontend` app on Vercel
- Backend: deploy the `backend` app on Render
- Database: provision PostgreSQL on Neon or Supabase and set DATABASE_URL
- Images: configure Cloudinary credentials
- Monitoring: wire Sentry in both frontend and backend

## CI/CD

GitHub Actions runs linting, tests, build validation, and migration checks whenever code is pushed.

## Security

- keep secrets in environment variables
- never commit `.env` files
- restrict CORS origins and validate payment webhook signatures
- enforce server-side auth and authorization

## Backup and recovery

- verify provider-level backups for PostgreSQL
- test restore procedures regularly
- keep database snapshots before major migrations
