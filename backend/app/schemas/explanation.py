from pydantic import BaseModel


class FeatureContribution(BaseModel):
    feature: str
    value: float
    contribution: float


class ExplanationResponse(BaseModel):
    patient_id: int
    prediction_id: int
    model_version: str
    base_value: float
    contributions: list[FeatureContribution]
