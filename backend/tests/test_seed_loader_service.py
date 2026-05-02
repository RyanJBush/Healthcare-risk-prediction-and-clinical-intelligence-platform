from app.services.seed_loader import generate_seed_patients


def test_generate_seed_patients_is_deterministic_for_same_seed() -> None:
    first = generate_seed_patients(count=5, seed=42)
    second = generate_seed_patients(count=5, seed=42)

    first_snapshot = [
        (p.full_name, p.masked_identifier, p.age, p.bmi, p.blood_pressure, p.cholesterol, p.glucose, p.smoker)
        for p in first
    ]
    second_snapshot = [
        (p.full_name, p.masked_identifier, p.age, p.bmi, p.blood_pressure, p.cholesterol, p.glucose, p.smoker)
        for p in second
    ]

    assert first_snapshot == second_snapshot


def test_generate_seed_patients_uses_expected_identifier_and_name_format() -> None:
    patients = generate_seed_patients(count=3, seed=7)

    assert [p.full_name for p in patients] == [
        "Synthetic Patient 1",
        "Synthetic Patient 2",
        "Synthetic Patient 3",
    ]
    assert [p.masked_identifier for p in patients] == [
        "DEMO-7-0001",
        "DEMO-7-0002",
        "DEMO-7-0003",
    ]


def test_generate_seed_patients_values_stay_in_expected_ranges() -> None:
    patients = generate_seed_patients(count=250, seed=9)

    assert len(patients) == 250
    for patient in patients:
        assert 24 <= patient.age <= 89
        assert 18.5 <= patient.bmi <= 40.0
        assert 98 <= patient.blood_pressure <= 176
        assert 130 <= patient.cholesterol <= 295
        assert 70 <= patient.glucose <= 255
        assert isinstance(patient.smoker, bool)
        assert isinstance(patient.has_historical_outcome, bool)


def test_generate_seed_patients_different_seed_produces_different_population() -> None:
    first = generate_seed_patients(count=3, seed=1)
    second = generate_seed_patients(count=3, seed=2)

    assert [p.masked_identifier for p in first] != [p.masked_identifier for p in second]
    assert [p.age for p in first] != [p.age for p in second]
