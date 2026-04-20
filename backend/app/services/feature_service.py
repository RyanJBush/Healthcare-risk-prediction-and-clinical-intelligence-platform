from app.models.patient import Patient

FEATURE_ORDER = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "pulse_pressure",
    "cholesterol",
    "bmi",
    "hba1c",
    "metabolic_risk_index",
]


class FeatureEngineeringService:
    @staticmethod
    def build_features(patient: Patient) -> dict[str, float]:
        pulse_pressure = patient.systolic_bp - patient.diastolic_bp
        metabolic_risk_index = (patient.bmi * patient.hba1c) / 10.0

        return {
            "age": float(patient.age),
            "systolic_bp": float(patient.systolic_bp),
            "diastolic_bp": float(patient.diastolic_bp),
            "pulse_pressure": float(pulse_pressure),
            "cholesterol": float(patient.cholesterol),
            "bmi": float(patient.bmi),
            "hba1c": float(patient.hba1c),
            "metabolic_risk_index": float(metabolic_risk_index),
        }
