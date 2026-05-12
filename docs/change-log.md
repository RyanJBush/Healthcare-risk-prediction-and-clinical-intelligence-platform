# Cerberus Change Log

## 2026-05-12 — Portfolio honesty and preview renovation

### Synthetic-data and PHI disclaimers
- Updated `README.md` with a top-level disclaimer that Cerberus uses synthetic data only, contains no PHI, and is a student portfolio demo.
- Reinforced synthetic-context language in `docs/resume-bullets.md` and `docs/screenshots/README.md`.

### “Not for clinical use” placement
- Standardized explicit “Not for clinical use” messaging in the top-level README and portfolio preview page.
- Added concise safety framing in screenshot documentation so captured artifacts remain aligned with non-clinical intent.

### Preview and UX improvements
- Refined `docs/preview/index.html` with a clean white/teal visual system, mobile-friendly cards, and a clear Features → Model → Risk Score pipeline.
- Added practical local demo commands (`make demo-train-small`, `make demo-fairness`, `make demo-predict`) to simplify synthetic-data walkthroughs.
