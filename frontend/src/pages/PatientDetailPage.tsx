import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import PageHeader from "../components/PageHeader";
import RiskGauge from "../components/RiskGauge";
import ShapBarChart from "../components/ShapBarChart";
import {
  fetchExplanationForPatient,
  fetchPatientById,
  fetchPredictionForPatient
} from "../services/api";
import type { Explanation, Patient, PredictionSummary } from "../types/patient";

export default function PatientDetailPage() {
  const { patientId } = useParams();
  const parsedId = Number(patientId);

  const [patient, setPatient] = useState<Patient | null>(null);
  const [prediction, setPrediction] = useState<PredictionSummary | null>(null);
  const [explanation, setExplanation] = useState<Explanation | null>(null);

  useEffect(() => {
    async function hydrate() {
      if (!Number.isFinite(parsedId)) return;
      const [patientData, predictionData, explanationData] = await Promise.all([
        fetchPatientById(parsedId),
        fetchPredictionForPatient(parsedId),
        fetchExplanationForPatient(parsedId)
      ]);
      setPatient(patientData);
      setPrediction(predictionData);
      setExplanation(explanationData);
    }

    void hydrate();
  }, [parsedId]);

  if (!patient || !prediction) {
    return (
      <section>
        <PageHeader title="Patient Detail" subtitle="Patient not found" />
        <Link to="/patients" className="link-button">
          Back to Patients
        </Link>
      </section>
    );
  }

  return (
    <section>
      <PageHeader
        title={`Patient ${patient.external_id}`}
        subtitle="Longitudinal clinical profile with model output and explainability"
      />

      <div className="detail-grid">
        <article className="panel">
          <h3>Clinical Snapshot</h3>
          <ul className="meta-list">
            <li>Age: {patient.age}</li>
            <li>Sex: {patient.sex}</li>
            <li>Blood Pressure: {patient.systolic_bp}/{patient.diastolic_bp}</li>
            <li>Cholesterol: {patient.cholesterol}</li>
            <li>BMI: {patient.bmi}</li>
            <li>HbA1c: {patient.hba1c}</li>
          </ul>
        </article>

        <article className="panel">
          <h3>Risk Score</h3>
          <RiskGauge score={prediction.risk_score} category={prediction.risk_category} />
          <p>Prediction ID: {prediction.prediction_id}</p>
          <p>Model version: {prediction.model_version}</p>
        </article>
      </div>

      <article className="panel">
        <h3>SHAP Explanation</h3>
        {explanation ? (
          <>
            <p>Base value: {explanation.base_value}</p>
            <ShapBarChart contributions={explanation.contributions} />
          </>
        ) : (
          <p>No explanation available yet for this patient.</p>
        )}
      </article>

      <Link to="/risk-analysis" className="link-button">
        Open Risk Analysis
      </Link>
    </section>
  );
}
