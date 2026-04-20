# Nova AI Architecture

- **Backend**: FastAPI + SQLAlchemy with JWT RBAC and PostgreSQL/SQLite
- **Risk Engine (Phase 1)**: Tiered multi-target scoring (`readmission`, `deterioration`, `adverse_event`) with thresholds, risk categories, confidence, baseline vs advanced scores, and clinician-readable explanation artifacts
- **Workflow (Phase 1)**: Triage queue, review status lifecycle (`new`, `reviewed`, `escalated`, `monitored`), reviewer assignment, and observation-triggered rescoring
- **Data (Phase 1)**: Time-series patient observations with missingness flags and masked patient identifiers
- **Trust/Compliance Scaffolding (Phase 1)**: Audit logs for key actions and model card registry endpoints
- **Frontend**: React + Vite + Tailwind + Recharts dashboard with KPI/cohort cards and triage views
- **Infra**: Docker Compose for local dev, GitHub Actions for CI
