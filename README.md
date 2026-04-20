# Nova AI Monorepo

Production-style scaffold for a healthcare risk prediction platform.

## Stack
- **Backend**: FastAPI + SQLAlchemy
- **Frontend**: React + Vite + TypeScript
- **Database**: PostgreSQL (SQLite default for local quickstart)
- **ML/Explainability**: Scikit-learn logistic regression + SHAP
- **Platform**: Docker Compose + GitHub Actions CI

## Repository layout
```
.
├── backend/
├── frontend/
├── docs/
├── .github/workflows/
├── docker-compose.yml
├── Makefile
└── README.md
```

## Key API endpoints
- `GET /health`
- `GET /api/v1/patients`
- `POST /api/v1/patients`
- `POST /api/v1/patients/ingest`
- `POST /api/v1/predictions`
- `GET /api/v1/explanations/{patient_id}`

## Frontend dashboard pages
- `Dashboard`: KPI cards + at-risk list
- `Patients`: searchable/filterable patient table view
- `Patient Detail`: risk score and SHAP contributions per patient
- `Risk Analysis`: comparative explainability workspace

## Backend capabilities
- Patient ingestion (single + batch)
- Feature engineering pipeline (`pulse_pressure`, `metabolic_risk_index`)
- ML risk prediction via logistic regression
- Risk categorization (`low`, `medium`, `high`)
- SHAP explainability on prediction outputs
- Structured logging for ingest and prediction operations

## Local development
### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker + Docker Compose

### Run with Docker
```bash
make docker-up
```

### Run services locally
```bash
make install
make dev-backend
# in another shell
make dev-frontend
```

### Test backend
```bash
make test
```

## Example patient payload
```json
{
  "external_id": "P-1001",
  "age": 68,
  "sex": "male",
  "systolic_bp": 152,
  "diastolic_bp": 88,
  "cholesterol": 245,
  "bmi": 32.5,
  "hba1c": 7.4
}
```

## Docs
See `docs/architecture.md` for architecture and production hardening checklist.
