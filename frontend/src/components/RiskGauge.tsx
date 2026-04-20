import type { RiskCategory } from "../types/patient";

type RiskGaugeProps = {
  score: number;
  category: RiskCategory;
};

export default function RiskGauge({ score, category }: RiskGaugeProps) {
  const normalized = Math.round(score * 100);
  return (
    <div className="risk-gauge-wrap">
      <div className="risk-gauge">
        <div className={`risk-gauge-fill ${category}`} style={{ width: `${normalized}%` }} />
      </div>
      <div className="risk-gauge-meta">
        <strong>{normalized}%</strong>
        <span className={`risk-chip ${category}`}>{category.toUpperCase()} RISK</span>
      </div>
    </div>
  );
}
