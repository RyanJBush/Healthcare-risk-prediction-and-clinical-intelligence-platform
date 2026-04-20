def test_ingest_predict_and_explain_flow(client) -> None:
    ingest_payload = {
        "patients": [
            {
                "external_id": "P-1001",
                "age": 68,
                "sex": "male",
                "systolic_bp": 152,
                "diastolic_bp": 88,
                "cholesterol": 245,
                "bmi": 32.5,
                "hba1c": 7.4,
            }
        ]
    }

    ingest_response = client.post("/api/v1/patients/ingest", json=ingest_payload)
    assert ingest_response.status_code == 201
    patient_id = ingest_response.json()["patient_ids"][0]

    prediction_response = client.post("/api/v1/predictions", json={"patient_id": patient_id})
    assert prediction_response.status_code == 200
    prediction_body = prediction_response.json()
    assert prediction_body["risk_category"] in {"low", "medium", "high"}
    assert 0.0 <= prediction_body["risk_score"] <= 1.0

    explanation_response = client.get(f"/api/v1/explanations/{patient_id}")
    assert explanation_response.status_code == 200
    explanation_body = explanation_response.json()
    assert explanation_body["patient_id"] == patient_id
    assert len(explanation_body["contributions"]) == 8
