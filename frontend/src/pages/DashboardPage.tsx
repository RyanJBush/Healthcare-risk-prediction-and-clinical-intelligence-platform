import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import KPICard from "../components/KPICard";
import PageHeader from "../components/PageHeader";
import RiskGauge from "../components/RiskGauge";
import { fetchPatients, fetchPredictionForPatient } from "../services/api";
import type { Patient, PredictionSummary } from "../types/patient";

export default function DashboardPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [predictions, setPredictions] = useState<Record<number, PredictionSummary>>({});

  useEffect(() => {
    async function hydrate() {
      const patientsData = await fetchPatients();
      setPatients(patientsData);

      const predictionMap: Record<number, PredictionSummary> = {};
      for (const patient of patientsData) {
        predictionMap[patient.id] = await fetchPredictionForPatient(patient.id);
      }
      setPredictions(predictionMap);
    }

    void hydrate();
  }, []);

  const kpis = useMemo(() => {
    const summaries = Object.values(predictions);
    const total = summaries.length;
    const high = summaries.filter((item) => item.risk_category === "high").length;
    const medium = summaries.filter((item) => item.risk_category === "medium").length;
    const avgRisk = total ? summaries.reduce((sum, item) => sum + item.risk_score, 0) / total : 0;

    return {
      total,
      high,
      medium,
      avgRisk
    };
  }, [predictions]);

  return (
    <section>
      <PageHeader
        title="Clinical Risk Dashboard"
        subtitle="Portfolio view of patient risk posture, stratification, and explainability readiness"
      />

      <div className="kpi-grid">
        <KPICard label="Patients Tracked" value={`${kpis.total}`} trend="Updated just now" />
        <KPICard label="High-Risk Patients" value={`${kpis.high}`} trend="Needs intervention" />
        <KPICard label="Medium-Risk Patients" value={`${kpis.medium}`} trend="Requires follow-up" />
        <KPICard label="Average Risk Score" value={`${Math.round(kpis.avgRisk * 100)}%`} trend="Model v1" />
      </div>

      <section className="panel">
        <h3>Top At-Risk Patients</h3>
        <div className="stack">
          {patients.slice(0, 3).map((patient) => {
            const prediction = predictions[patient.id];
            if (!prediction) return null;

            return (
              <article className="row-card" key={patient.id}>
                <div>
                  <strong>{patient.external_id}</strong>
                  <p>
                    Age {patient.age} • BP {patient.systolic_bp}/{patient.diastolic_bp}
                  </p>
                </div>
                <RiskGauge score={prediction.risk_score} category={prediction.risk_category} />
                <Link className="link-button" to={`/patients/${patient.id}`}>
                  Open Detail
                </Link>
              </article>
            );
          })}
        </div>
      </section>
    </section>
  );
}
