import type { Explanation, Patient, PredictionSummary } from "../types/patient";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

const mockPatients: Patient[] = [
  {
    id: 1,
    external_id: "P-1001",
    age: 68,
    sex: "male",
    systolic_bp: 152,
    diastolic_bp: 88,
    cholesterol: 245,
    bmi: 32.5,
    hba1c: 7.4
  },
  {
    id: 2,
    external_id: "P-1002",
    age: 57,
    sex: "female",
    systolic_bp: 134,
    diastolic_bp: 82,
    cholesterol: 210,
    bmi: 28.1,
    hba1c: 6.2
  },
  {
    id: 3,
    external_id: "P-1003",
    age: 49,
    sex: "female",
    systolic_bp: 126,
    diastolic_bp: 78,
    cholesterol: 189,
    bmi: 25.2,
    hba1c: 5.8
  },
  {
    id: 4,
    external_id: "P-1004",
    age: 72,
    sex: "male",
    systolic_bp: 161,
    diastolic_bp: 92,
    cholesterol: 270,
    bmi: 34.7,
    hba1c: 8.0
  }
];

const mockPredictionByPatient: Record<number, PredictionSummary> = {
  1: { prediction_id: 5001, patient_id: 1, risk_score: 0.84, risk_category: "high", model_version: "lr-v1" },
  2: { prediction_id: 5002, patient_id: 2, risk_score: 0.51, risk_category: "medium", model_version: "lr-v1" },
  3: { prediction_id: 5003, patient_id: 3, risk_score: 0.24, risk_category: "low", model_version: "lr-v1" },
  4: { prediction_id: 5004, patient_id: 4, risk_score: 0.9, risk_category: "high", model_version: "lr-v1" }
};

const mockExplanationByPatient: Record<number, Explanation> = {
  1: {
    patient_id: 1,
    prediction_id: 5001,
    model_version: "lr-v1",
    base_value: -0.42,
    contributions: [
      { feature: "hba1c", value: 7.4, contribution: 0.64 },
      { feature: "bmi", value: 32.5, contribution: 0.37 },
      { feature: "systolic_bp", value: 152, contribution: 0.32 },
      { feature: "age", value: 68, contribution: 0.27 },
      { feature: "cholesterol", value: 245, contribution: 0.23 },
      { feature: "metabolic_risk_index", value: 24.05, contribution: 0.2 },
      { feature: "pulse_pressure", value: 64, contribution: 0.12 },
      { feature: "diastolic_bp", value: 88, contribution: -0.09 }
    ]
  },
  2: {
    patient_id: 2,
    prediction_id: 5002,
    model_version: "lr-v1",
    base_value: -0.42,
    contributions: [
      { feature: "hba1c", value: 6.2, contribution: 0.28 },
      { feature: "bmi", value: 28.1, contribution: 0.19 },
      { feature: "systolic_bp", value: 134, contribution: 0.15 },
      { feature: "age", value: 57, contribution: 0.14 },
      { feature: "cholesterol", value: 210, contribution: 0.11 },
      { feature: "metabolic_risk_index", value: 17.42, contribution: 0.1 },
      { feature: "pulse_pressure", value: 52, contribution: 0.06 },
      { feature: "diastolic_bp", value: 82, contribution: -0.06 }
    ]
  }
};

async function safeJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`);
    if (!response.ok) {
      return fallback;
    }
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function fetchHealth(): Promise<{ status: string }> {
  try {
    const response = await fetch(`${API_BASE_URL.replace("/api/v1", "")}/health`);
    if (!response.ok) return { status: "mock-ok" };
    return (await response.json()) as { status: string };
  } catch {
    return { status: "mock-ok" };
  }
}

export async function fetchPatients(): Promise<Patient[]> {
  return safeJson<Patient[]>("/patients", mockPatients);
}

export async function fetchPatientById(patientId: number): Promise<Patient | null> {
  const patients = await fetchPatients();
  return patients.find((patient) => patient.id === patientId) ?? null;
}

export async function fetchPredictionForPatient(patientId: number): Promise<PredictionSummary> {
  const fallback = mockPredictionByPatient[patientId] ?? {
    prediction_id: 0,
    patient_id: patientId,
    risk_score: 0.0,
    risk_category: "low",
    model_version: "lr-v1"
  };

  return safeJson<PredictionSummary>("/predictions", fallback);
}

export async function fetchExplanationForPatient(patientId: number): Promise<Explanation | null> {
  const fallback = mockExplanationByPatient[patientId] ?? null;
  return safeJson<Explanation | null>(`/explanations/${patientId}`, fallback);
}
