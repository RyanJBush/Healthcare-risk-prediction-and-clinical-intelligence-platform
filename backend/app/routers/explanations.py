from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.patient import Patient
from app.schemas.explanation import ExplanationResponse
from app.services.prediction_service import PredictionService

router = APIRouter(prefix="/explanations", tags=["explanations"])


@router.get("/{patient_id}", response_model=ExplanationResponse)
def explain(patient_id: int, db: Session = Depends(get_db)) -> ExplanationResponse:
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    explanation = PredictionService.get_latest_explanation(db, patient)
    if not explanation:
        raise HTTPException(status_code=404, detail="No prediction available for patient")
    return explanation
