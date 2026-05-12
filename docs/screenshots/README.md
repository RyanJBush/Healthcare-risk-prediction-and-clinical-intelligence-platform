# Cerberus Screenshots — Portfolio Preview Assets

All screenshots in this folder are from a local demo using **synthetic data only**. They contain **no PHI** and are **not for clinical use**.

## Current files

- `01-dashboard.png` — Dashboard with synthetic cohort KPIs and status panels.
- `02-patient-detail.png` — Patient detail view with risk output and review metadata.
- `03-explanation.png` — Explainability card with top factors and reason codes.
- `04-triage-queue.png` — Queue-style prioritization for synthetic records.
- `05-risk-analysis.png` — Comparison and threshold exploration view.
- `06-fairness-report.png` — CLI fairness-slice output snapshot.
- `07-model-card.png` — Model card and limitation notes.
- `08-api-docs.png` — FastAPI Swagger documentation.

## Capture checklist for future updates

1. Start local stack (`make dev`) and seed demo data (`make demo-bootstrap`).
2. Keep all visible patient content synthetic and non-identifying.
3. Avoid wording that implies diagnosis, treatment planning, or hospital deployment.
4. Preserve filename numbering so links remain stable.
5. Add date captured and short context notes in PR descriptions.

## TODO (optional refresh)

- [ ] Recapture Dashboard after any major UI metric-card redesign.
- [ ] Recapture Risk Analysis if charts or threshold controls materially change.
- [ ] Add one mobile-width screenshot if responsive layout is significantly updated.
