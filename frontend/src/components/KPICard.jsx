function KPICard({
  title,
  value,
  subtitle,
  icon: Icon,
}) {
  return (
    <div className="kpi-card">

      <div className="kpi-card-top">
        <span className="kpi-title">
          {title}
        </span>

        {Icon && (
          <div className="kpi-icon">
            <Icon size={20} />
          </div>
        )}
      </div>

      <h2 className="kpi-value">
        {value}
      </h2>

      {subtitle && (
        <p className="kpi-subtitle">
          {subtitle}
        </p>
      )}

    </div>
  );
}

export default KPICard;