import { useEffect, useMemo, useState } from "react";
import PageHeader from "../components/PageHeader";
import ShapBarChart from "../components/ShapBarChart";
import { fetchExplanationForPatient, fetchPatients, fetchPredictionForPatient } from "../services/api";
import type { Explanation, Patient, PredictionSummary } from "../types/patient";

export default function RiskAnalysisPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null);
  const [prediction, setPrediction] = useState<PredictionSummary | null>(null);
  const [explanation, setExplanation] = useState<Explanation | null>(null);

  useEffect(() => {
    async function loadPatients() {
      const data = await fetchPatients();
      setPatients(data);
      if (data.length > 0) {
        setSelectedPatientId(data[0].id);
      }
    }

    void loadPatients();
  }, []);

  useEffect(() => {
    async function loadRiskData() {
      if (!selectedPatientId) return;
      const [predictionData, explanationData] = await Promise.all([
        fetchPredictionForPatient(selectedPatientId),
        fetchExplanationForPatient(selectedPatientId)
      ]);
      setPrediction(predictionData);
      setExplanation(explanationData);
    }

    void loadRiskData();
  }, [selectedPatientId]);

  const selectedPatient = useMemo(
    () => patients.find((patient) => patient.id === selectedPatientId) ?? null,
    [patients, selectedPatientId]
  );

  return (
    <section>
      <PageHeader
        title="Risk Analysis"
        subtitle="Deep dive into risk drivers and contribution analysis for a selected patient"
      />

      <div className="toolbar">
        <label className="label">Select patient</label>
        <select
          className="select"
          value={selectedPatientId ?? ""}
          onChange={(event) => setSelectedPatientId(Number(event.target.value))}
        >
          {patients.map((patient) => (
            <option key={patient.id} value={patient.id}>
              {patient.external_id}
            </option>
          ))}
        </select>
      </div>

      <div className="detail-grid">
        <article className="panel">
          <h3>Patient Context</h3>
          {selectedPatient ? (
            <ul className="meta-list">
              <li>Age: {selectedPatient.age}</li>
              <li>Blood Pressure: {selectedPatient.systolic_bp}/{selectedPatient.diastolic_bp}</li>
              <li>BMI: {selectedPatient.bmi}</li>
              <li>HbA1c: {selectedPatient.hba1c}</li>
            </ul>
          ) : (
            <p>No patient selected.</p>
          )}
        </article>
        <article className="panel">
          <h3>Current Risk Output</h3>
          {prediction ? (
            <>
              <p>Risk score: {(prediction.risk_score * 100).toFixed(0)}%</p>
              <p>Risk category: {prediction.risk_category.toUpperCase()}</p>
              <p>Model version: {prediction.model_version}</p>
            </>
          ) : (
            <p>Prediction unavailable.</p>
          )}
        </article>
      </div>

      <article className="panel">
        <h3>Feature Contribution Chart</h3>
        {explanation ? <ShapBarChart contributions={explanation.contributions} /> : <p>No SHAP data available.</p>}
      </article>
    </section>
  );
}
