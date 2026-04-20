import logging

import numpy as np
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.services.feature_service import FEATURE_ORDER

logger = logging.getLogger(__name__)


class MLService:
    _pipeline: Pipeline | None = None
    _background_data: np.ndarray | None = None
    model_version = "lr-v1"

    @classmethod
    def _train_if_needed(cls) -> None:
        if cls._pipeline is not None:
            return

        rng = np.random.default_rng(seed=42)
        n = 1200
        age = rng.integers(18, 90, size=n)
        systolic = rng.normal(130, 18, size=n)
        diastolic = rng.normal(80, 10, size=n)
        pulse_pressure = systolic - diastolic
        cholesterol = rng.normal(210, 35, size=n)
        bmi = rng.normal(29, 6, size=n)
        hba1c = rng.normal(6.1, 1.2, size=n)
        metabolic = (bmi * hba1c) / 10.0

        X = np.column_stack([age, systolic, diastolic, pulse_pressure, cholesterol, bmi, hba1c, metabolic])
        logit = (
            -9.0
            + 0.030 * age
            + 0.018 * systolic
            - 0.007 * diastolic
            + 0.014 * cholesterol
            + 0.050 * bmi
            + 0.55 * hba1c
            + 0.10 * metabolic
        )
        p = 1 / (1 + np.exp(-logit))
        y = (rng.random(n) < p).astype(int)

        pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, random_state=42)),
            ]
        )
        pipeline.fit(X, y)
        cls._pipeline = pipeline
        cls._background_data = X[:200]
        logger.info("ML pipeline trained with synthetic baseline data")

    @classmethod
    def predict(cls, feature_vector: dict[str, float]) -> tuple[float, str]:
        cls._train_if_needed()
        assert cls._pipeline is not None
        row = np.array([[feature_vector[name] for name in FEATURE_ORDER]], dtype=float)
        risk_score = float(cls._pipeline.predict_proba(row)[0, 1])
        return risk_score, cls.model_version

    @classmethod
    def explain(cls, feature_vector: dict[str, float]) -> tuple[float, list[float]]:
        cls._train_if_needed()
        assert cls._pipeline is not None
        assert cls._background_data is not None

        row = np.array([[feature_vector[name] for name in FEATURE_ORDER]], dtype=float)
        try:
            explainer = shap.Explainer(cls._pipeline.predict_proba, cls._background_data)
            explanation = explainer(row)
            values = explanation.values[0, :, 1].tolist()
            base_value = float(explanation.base_values[0, 1])
            return base_value, [float(v) for v in values]
        except Exception as exc:  # fallback in case SHAP backend differs
            logger.warning("SHAP explainer fallback triggered: %s", exc)
            model = cls._pipeline.named_steps["model"]
            scaler = cls._pipeline.named_steps["scaler"]
            coef = model.coef_[0]
            scaled_row = scaler.transform(row)[0]
            values = (coef * scaled_row).tolist()
            base_value = float(model.intercept_[0])
            return base_value, [float(v) for v in values]
