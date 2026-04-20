from app.models.patient import Patient
from app.services.feature_service import FeatureEngineeringService


def test_feature_engineering_builds_expected_values() -> None:
    patient = Patient(
        external_id="P-001",
        age=55,
        sex="female",
        systolic_bp=145,
        diastolic_bp=90,
        cholesterol=230,
        bmi=31.2,
        hba1c=7.1,
    )

    features = FeatureEngineeringService.build_features(patient)

    assert features["pulse_pressure"] == 55.0
    assert round(features["metabolic_risk_index"], 4) == round((31.2 * 7.1) / 10.0, 4)
