import type { RiskCategory } from "../types/patient";

type PatientFilterBarProps = {
  query: string;
  riskFilter: RiskCategory | "all";
  onQueryChange: (value: string) => void;
  onRiskFilterChange: (value: RiskCategory | "all") => void;
};

export default function PatientFilterBar({
  query,
  riskFilter,
  onQueryChange,
  onRiskFilterChange
}: PatientFilterBarProps) {
  return (
    <div className="toolbar">
      <input
        className="input"
        placeholder="Search by external ID"
        value={query}
        onChange={(event) => onQueryChange(event.target.value)}
      />
      <select
        className="select"
        value={riskFilter}
        onChange={(event) => onRiskFilterChange(event.target.value as RiskCategory | "all")}
      >
        <option value="all">All risk levels</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>
    </div>
  );
}
