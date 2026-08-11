type MetricCardProps = {
  label: string;
  value: string;
  description: string;
  icon: string;
};

export function MetricCard({
  label,
  value,
  description,
  icon,
}: MetricCardProps) {
  return (
    <article className="qwos-metric-card">
      <div className="qwos-metric-card-top">
        <div>
          <p className="qwos-metric-card-label">{label}</p>
          <p className="qwos-metric-card-value">{value}</p>
        </div>

        <div className="qwos-metric-card-icon">
          {icon}
        </div>
      </div>

      <p className="qwos-metric-card-description">
        {description}
      </p>
    </article>
  );
}