import type { FeatureContribution } from "../types/patient";

type ShapBarChartProps = {
  contributions: FeatureContribution[];
};

export default function ShapBarChart({ contributions }: ShapBarChartProps) {
  const sorted = [...contributions].sort(
    (left, right) => Math.abs(right.contribution) - Math.abs(left.contribution)
  );
  const max = Math.max(...sorted.map((item) => Math.abs(item.contribution)), 0.01);

  return (
    <section className="shap-chart">
      {sorted.map((item) => {
        const width = Math.max((Math.abs(item.contribution) / max) * 100, 6);
        const positive = item.contribution >= 0;

        return (
          <div key={item.feature} className="shap-row">
            <div className="shap-row-header">
              <span>{item.feature}</span>
              <span>{item.value}</span>
            </div>
            <div className="shap-track">
              <div
                className={`shap-bar ${positive ? "positive" : "negative"}`}
                style={{ width: `${width}%` }}
              />
            </div>
            <span className="shap-score">{item.contribution.toFixed(3)}</span>
          </div>
        );
      })}
    </section>
  );
}
