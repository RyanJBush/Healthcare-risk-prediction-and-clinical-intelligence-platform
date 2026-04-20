from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.patient import (
    PatientCreate,
    PatientIngestRequest,
    PatientIngestResponse,
    PatientRead,
)
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db)) -> list[PatientRead]:
    return PatientService.list_patients(db)


@router.post("", response_model=PatientRead, status_code=201)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)) -> PatientRead:
    return PatientService.create_patient(db, payload)


@router.post("/ingest", response_model=PatientIngestResponse, status_code=201)
def ingest_patients(payload: PatientIngestRequest, db: Session = Depends(get_db)) -> PatientIngestResponse:
    created = PatientService.ingest_patients(db, payload.patients)
    return PatientIngestResponse(created=len(created), patient_ids=[patient.id for patient in created])
