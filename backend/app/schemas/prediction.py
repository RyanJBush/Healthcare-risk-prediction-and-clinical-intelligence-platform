from pydantic import BaseModel


class PredictionRequest(BaseModel):
    patient_id: int


class PredictionResponse(BaseModel):
    prediction_id: int
    patient_id: int
    risk_score: float
    risk_category: str
    model_version: str
