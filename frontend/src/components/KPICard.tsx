type KPICardProps = {
  label: string;
  value: string;
  trend?: string;
};

export default function KPICard({ label, value, trend }: KPICardProps) {
  return (
    <article className="kpi-card">
      <span className="kpi-label">{label}</span>
      <strong className="kpi-value">{value}</strong>
      {trend ? <span className="kpi-trend">{trend}</span> : null}
    </article>
  );
}
