import logging

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate

logger = logging.getLogger(__name__)


class PatientService:
    @staticmethod
    def create_patient(db: Session, payload: PatientCreate) -> Patient:
        patient = Patient(**payload.model_dump())
        db.add(patient)
        db.commit()
        db.refresh(patient)
        logger.info("Patient created", extra={"patient_id": patient.id, "external_id": patient.external_id})
        return patient

    @staticmethod
    def ingest_patients(db: Session, payloads: list[PatientCreate]) -> list[Patient]:
        created: list[Patient] = []
        for payload in payloads:
            created.append(Patient(**payload.model_dump()))
        db.add_all(created)
        db.commit()
        for patient in created:
            db.refresh(patient)
        logger.info("Patient ingestion complete", extra={"count": len(created)})
        return created

    @staticmethod
    def list_patients(db: Session) -> list[Patient]:
        return db.query(Patient).order_by(Patient.id.desc()).all()
