import { useEffect, useState } from "react";

import {
  Factory,
  TrendingDown,
  AlertTriangle,
  IndianRupee,
  Activity,
} from "lucide-react";

import {
  getFactoryLoss,
  getNextWeekProjection,
} from "../services/api";

function Factories() {
  const [loss, setLoss] = useState(null);
  const [projection, setProjection] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [
          lossData,
          projectionData,
        ] = await Promise.all([
          getFactoryLoss(),
          getNextWeekProjection(),
        ]);

        setLoss(lossData);
        setProjection(projectionData);
      } catch (error) {
        console.error(
          "Factory API error:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: "28px" }}>
        Loading factory intelligence...
      </div>
    );
  }

  if (!loss) {
    return (
      <div style={{ padding: "28px" }}>
        Factory data unavailable.
      </div>
    );
  }

  const causes = loss.causes || [];

  return (
    <div style={{ padding: "28px" }}>
      <div style={{ marginBottom: "25px" }}>
        <h1>Factory Intelligence</h1>

        <p style={{ color: "#94a3b8" }}>
          Production loss, disruption impact and predictive
          factory intelligence.
        </p>
      </div>

      <div style={gridStyle}>
        <MetricCard
          icon={<Factory size={22} />}
          title="Factory"
          value={
            loss.factory ||
            loss.factory_name ||
            "Plant Alpha"
          }
        />

        <MetricCard
          icon={
            <IndianRupee size={22} />
          }
          title="Current Loss"
          value={`₹${Number(
            loss.total_loss || 0
          ).toLocaleString("en-IN")}`}
        />

        <MetricCard
          icon={
            <AlertTriangle size={22} />
          }
          title="Risk Status"
          value="HIGH"
        />

        <MetricCard
          icon={<Activity size={22} />}
          title="Monitoring"
          value="LIVE"
        />
      </div>

      <div
        style={{
          ...cardStyle,
          marginTop: "22px",
        }}
      >
        <h2>Root Cause Analysis</h2>

        <p style={{ color: "#94a3b8" }}>
          Financial contribution of major production-loss
          drivers.
        </p>

        <div style={{ marginTop: "20px" }}>
          {causes.map((cause, index) => {
            const amount =
              cause.amount ??
              cause.loss ??
              cause.value ??
              0;

            const percentage =
              cause.percentage ?? 0;

            const name =
              cause.cause ||
              cause.name ||
              "Unknown Cause";

            return (
              <div
                key={index}
                style={{
                  marginBottom: "20px",
                }}
              >
                <div style={rowStyle}>
                  <strong>{name}</strong>

                  <span>
                    ₹
                    {Number(
                      amount
                    ).toLocaleString(
                      "en-IN"
                    )}
                    {" · "}
                    {percentage}%
                  </span>
                </div>

                <div style={progressTrackStyle}>
                  <div
                    style={{
                      height: "100%",
                      width: `${percentage}%`,
                      background: "#f59e0b",
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {projection && (
        <div
          style={{
            ...cardStyle,
            marginTop: "22px",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
            }}
          >
            <TrendingDown size={22} />

            <h2>
              Next-Week Loss Projection
            </h2>
          </div>

          <div
            style={{
              ...gridStyle,
              marginTop: "20px",
            }}
          >
            <MiniCard
              title="Without Action"
              value={`₹${Number(
                projection.projected_loss_without_action ||
                  0
              ).toLocaleString("en-IN")}`}
            />

            <MiniCard
              title="With Optimization"
              value={`₹${Number(
                projection.projected_loss_with_optimization ||
                  0
              ).toLocaleString("en-IN")}`}
            />

            <MiniCard
              title="Potential Saving"
              value={`₹${Number(
                projection.potential_saving ||
                  0
              ).toLocaleString("en-IN")}`}
            />

            <MiniCard
              title="Loss Reduction"
              value={`${
                projection.reduction_percentage ||
                0
              }%`}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function MetricCard({
  icon,
  title,
  value,
}) {
  return (
    <div style={cardStyle}>
      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
          color: "#94a3b8",
        }}
      >
        {title}
        {icon}
      </div>

      <h2>{value}</h2>
    </div>
  );
}

function MiniCard({
  title,
  value,
}) {
  return (
    <div
      style={{
        background: "#0b1220",
        padding: "18px",
        borderRadius: "12px",
      }}
    >
      <div style={{ color: "#94a3b8" }}>
        {title}
      </div>

      <h2>{value}</h2>
    </div>
  );
}

const cardStyle = {
  background: "rgba(15,23,42,.85)",
  border: "1px solid #1e293b",
  borderRadius: "14px",
  padding: "20px",
};

const gridStyle = {
  display: "grid",
  gridTemplateColumns:
    "repeat(auto-fit,minmax(200px,1fr))",
  gap: "16px",
};

const rowStyle = {
  display: "flex",
  justifyContent: "space-between",
  gap: "15px",
};

const progressTrackStyle = {
  marginTop: "8px",
  height: "7px",
  borderRadius: "10px",
  background: "#1e293b",
  overflow: "hidden",
};

export default Factories;