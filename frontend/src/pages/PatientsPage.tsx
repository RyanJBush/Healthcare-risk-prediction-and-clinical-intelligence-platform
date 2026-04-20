import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../components/PageHeader";
import PatientFilterBar from "../components/PatientFilterBar";
import RiskGauge from "../components/RiskGauge";
import { fetchPatients, fetchPredictionForPatient } from "../services/api";
import type { Patient, PredictionSummary, RiskCategory } from "../types/patient";

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [predictions, setPredictions] = useState<Record<number, PredictionSummary>>({});
  const [query, setQuery] = useState("");
  const [riskFilter, setRiskFilter] = useState<RiskCategory | "all">("all");

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

  const filtered = useMemo(
    () =>
      patients.filter((patient) => {
        const queryMatch = patient.external_id.toLowerCase().includes(query.trim().toLowerCase());
        const riskMatch =
          riskFilter === "all" || predictions[patient.id]?.risk_category === riskFilter;

        return queryMatch && riskMatch;
      }),
    [patients, predictions, query, riskFilter]
  );

  return (
    <section>
      <PageHeader
        title="Patients"
        subtitle="Population list with filtering for fast clinical review and risk triage"
      />
      <PatientFilterBar
        query={query}
        riskFilter={riskFilter}
        onQueryChange={setQuery}
        onRiskFilterChange={setRiskFilter}
      />

      <section className="panel">
        {filtered.map((patient) => {
          const prediction = predictions[patient.id];
          if (!prediction) return null;

          return (
            <article className="row-card" key={patient.id}>
              <div>
                <strong>{patient.external_id}</strong>
                <p>
                  {patient.sex} • Age {patient.age} • HbA1c {patient.hba1c}
                </p>
              </div>
              <RiskGauge score={prediction.risk_score} category={prediction.risk_category} />
              <Link className="link-button" to={`/patients/${patient.id}`}>
                View Patient
              </Link>
            </article>
          );
        })}
      </section>
    </section>
  );
}
