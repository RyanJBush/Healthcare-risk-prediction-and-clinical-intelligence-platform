# Nova AI

Production-style monorepo for a healthcare risk prediction platform with explainable ML.

## Monorepo structure

- `backend/` FastAPI API, tiered ML scoring, clinician explanations, JWT RBAC
- `frontend/` React + Vite + Tailwind clinical dashboard
- `docs/` architecture notes
- `.github/workflows/ci.yml` CI for lint/test/build

## Quick start

```bash
make setup
make dev
```

Services:

- Backend API: `http://localhost:8000`
- Frontend app: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

## Backend endpoints (Phase 1)

- `GET /health`
- `POST /auth/login`
- `POST /api/patients`
- `GET /api/patients`
- `GET /api/patients/{id}`
- `PATCH /api/patients/{id}/review-status`
- `POST /api/patients/{id}/observations`
- `GET /api/patients/{id}/observations`
- `POST /api/predict`
- `POST /api/predict/tiered`
- `GET /api/predictions/{patient_id}`
- `GET /api/explanations/{patient_id}`
- `GET /api/triage/queue`
- `GET /api/metrics/summary`
- `GET /api/metrics/cohorts`
- `GET /api/model-cards`
- `GET /api/audit/logs`

## Demo credentials

- `clinician` / `clinician123`
- `admin` / `admin123`
- `analyst` / `analyst123`
- `viewer` / `viewer123`

## Quality

```bash
make lint
make test
```
