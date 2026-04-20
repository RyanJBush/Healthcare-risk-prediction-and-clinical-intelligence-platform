# Nova AI Architecture

## Monorepo layout
- `backend/`: FastAPI service for patients, predictions, feature engineering, and explanations.
- `frontend/`: React/Vite application for operations UI.
- `docs/`: Architecture and operational documents.
- `.github/workflows/`: CI definitions.

## Data flow
1. Patient data is ingested through `/api/v1/patients` and `/api/v1/patients/ingest`.
2. Feature engineering builds model-ready vectors (`pulse_pressure`, `metabolic_risk_index`).
3. Prediction endpoint scores risk probability and categorizes risk (`low`, `medium`, `high`).
4. Explanation endpoint returns SHAP feature contributions for the latest patient prediction.

## Current backend modules
- `services/feature_service.py`: deterministic feature transforms.
- `services/ml_service.py`: model training, inference, and SHAP explanations.
- `services/prediction_service.py`: orchestration + persistence.

## Production hardening checklist
- Move from synthetic training data to registry-backed production model artifacts.
- Add Alembic migrations and DB lifecycle strategy.
- Add authn/authz (OIDC/JWT + RBAC).
- Add observability (OpenTelemetry, metrics, logs).
- Add model quality monitoring and drift alerts.
