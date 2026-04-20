from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReviewStatus = Literal["new", "reviewed", "escalated", "monitored"]
TargetType = Literal["readmission", "deterioration", "adverse_event"]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class PatientCreate(BaseModel):
    full_name: str = Field(min_length=2)
    masked_identifier: str | None = Field(default=None, min_length=4, max_length=32)
    age: int = Field(ge=0, le=120)
    bmi: float = Field(ge=5, le=80)
    blood_pressure: float = Field(ge=40, le=300)
    cholesterol: float = Field(ge=40, le=500)
    glucose: float = Field(ge=30, le=500)
    smoker: bool = False
    has_historical_outcome: bool = False


class PatientRead(PatientCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    review_status: ReviewStatus
    assigned_reviewer: str | None = None
    created_at: datetime


class PredictRequest(BaseModel):
    patient_id: int


class PredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    target_type: TargetType
    risk_score: float
    baseline_risk_score: float
    confidence_score: float
    risk_category: str
    threshold_used: float
    reason_codes: str
    model_version: str
    created_at: datetime


class ExplanationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    prediction_id: int
    target_type: TargetType
    top_factors: str
    risk_factors: str
    protective_factors: str
    plain_summary: str
    rationale_summary: str
    provenance: str
    created_at: datetime


class TieredPredictionRead(BaseModel):
    patient_id: int
    predictions: list[PredictionRead]


class ReviewStatusUpdate(BaseModel):
    review_status: ReviewStatus
    assigned_reviewer: str | None = Field(default=None, max_length=64)


class TriageQueueItem(BaseModel):
    patient_id: int
    masked_identifier: str
    review_status: ReviewStatus
    assigned_reviewer: str | None = None
    target_type: TargetType
    risk_score: float
    risk_category: str
    confidence_score: float
    updated_at: datetime


class ObservationCreate(BaseModel):
    observed_at: datetime | None = None
    heart_rate: float | None = Field(default=None, ge=20, le=260)
    systolic_bp: float | None = Field(default=None, ge=40, le=300)
    diastolic_bp: float | None = Field(default=None, ge=20, le=200)
    oxygen_saturation: float | None = Field(default=None, ge=40, le=100)
    creatinine: float | None = Field(default=None, ge=0.1, le=20)
    glucose: float | None = Field(default=None, ge=30, le=500)
    source: str = Field(default="ehr", max_length=32)


class ObservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    observed_at: datetime
    heart_rate: float | None = None
    systolic_bp: float | None = None
    diastolic_bp: float | None = None
    oxygen_saturation: float | None = None
    creatinine: float | None = None
    glucose: float | None = None
    missingness_flags: str
    source: str
    created_at: datetime


class MetricsSummary(BaseModel):
    total_patients: int
    total_predictions: int
    average_risk_score: float
    high_risk_patients: int
    alerts_triggered: int
    recall_at_threshold: float
    monitored_cohort_size: int
    by_category: dict[str, int]


class CohortMetrics(BaseModel):
    by_review_status: dict[str, int]
    average_risk_by_target: dict[str, float]
    high_risk_watchlist_size: int


class ModelCardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model_name: str
    model_version: str
    target_type: str
    summary: str
    intended_use: str
    limitations: str
    threshold_config: str
    created_at: datetime


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    action: str
    resource_type: str
    resource_id: str
    details: str
    created_at: datetime
