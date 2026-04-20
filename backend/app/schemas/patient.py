from pydantic import BaseModel, ConfigDict, Field


class PatientBase(BaseModel):
    external_id: str
    age: int = Field(ge=18, le=120)
    sex: str
    systolic_bp: float = Field(ge=70, le=250)
    diastolic_bp: float = Field(ge=40, le=150)
    cholesterol: float = Field(ge=80, le=500)
    bmi: float = Field(ge=10, le=80)
    hba1c: float = Field(ge=3.0, le=20.0)


class PatientCreate(PatientBase):
    pass


class PatientIngestRequest(BaseModel):
    patients: list[PatientCreate]


class PatientRead(PatientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PatientIngestResponse(BaseModel):
    created: int
    patient_ids: list[int]
