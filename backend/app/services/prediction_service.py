import logging

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.models.prediction import Prediction
from app.schemas.explanation import ExplanationResponse, FeatureContribution
from app.schemas.prediction import PredictionResponse
from app.services.feature_service import FEATURE_ORDER, FeatureEngineeringService
from app.services.ml_service import MLService

logger = logging.getLogger(__name__)


class PredictionService:
    @staticmethod
    def categorize_risk(risk_score: float) -> str:
        if risk_score >= 0.66:
            return "high"
        if risk_score >= 0.33:
            return "medium"
        return "low"

    @classmethod
    def create_prediction(cls, db: Session, patient: Patient) -> PredictionResponse:
        features = FeatureEngineeringService.build_features(patient)
        risk_score, model_version = MLService.predict(features)
        risk_category = cls.categorize_risk(risk_score)
        base_value, shap_values = MLService.explain(features)

        prediction = Prediction(
            patient_id=patient.id,
            risk_score=risk_score,
            risk_category=risk_category,
            model_version=model_version,
            feature_vector=features,
            shap_values=shap_values,
            base_value=base_value,
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        logger.info(
            "Prediction created",
            extra={"prediction_id": prediction.id, "patient_id": patient.id, "risk_category": risk_category},
        )
        return PredictionResponse(
            prediction_id=prediction.id,
            patient_id=patient.id,
            risk_score=round(risk_score, 4),
            risk_category=risk_category,
            model_version=model_version,
        )

    @staticmethod
    def get_latest_explanation(db: Session, patient: Patient) -> ExplanationResponse | None:
        prediction = (
            db.query(Prediction)
            .filter(Prediction.patient_id == patient.id)
            .order_by(Prediction.id.desc())
            .first()
        )
        if prediction is None:
            return None

        contributions = [
            FeatureContribution(
                feature=feature,
                value=round(float(prediction.feature_vector[feature]), 4),
                contribution=round(float(prediction.shap_values[idx]), 4),
            )
            for idx, feature in enumerate(FEATURE_ORDER)
        ]

        return ExplanationResponse(
            patient_id=patient.id,
            prediction_id=prediction.id,
            model_version=prediction.model_version,
            base_value=round(float(prediction.base_value), 4),
            contributions=contributions,
        )
