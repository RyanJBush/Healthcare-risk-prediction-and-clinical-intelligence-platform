# Resume Bullets — Cerberus (Synthetic Healthcare ML Portfolio)

- Built a healthcare-inspired ML portfolio application (FastAPI + React + PostgreSQL) that scores **synthetic** patient-like records for readmission-style and deterioration-style risk targets.
- Implemented a tiered inference workflow that applies a lightweight heuristic first, then escalates low-confidence cases to scikit-learn models.
- Added model explainability outputs with SHAP-style factor contributions and reason codes to make risk scores easier to interpret during demos.
- Created model-registry and training-run APIs to track versioned artifacts, metrics, and scoring provenance.
- Developed a compact synthetic-data training workflow (`make demo-train-small`) for quick portfolio demonstrations.
- Authored fairness-slice and drift-analysis workflows on synthetic cohorts to showcase responsible-ML evaluation patterns.
- Integrated JWT auth, role-based access controls, and audit-style logging to simulate multi-user review operations.
- Containerized backend, frontend, and database services with Docker Compose + Make commands for consistent local setup.
- Documented explicit safety framing across project materials: synthetic data only, no PHI, and **not for clinical use**.
