import {
  useState,
} from "react";

import {
  Play,
  AlertTriangle,
  IndianRupee,
  Clock,
  ShieldCheck,
} from "lucide-react";

import {
  runWhatIf,
} from "../services/api";

function WhatIf() {
  const [
    disruptionType,
    setDisruptionType,
  ] = useState("Flood");

  const [severity, setSeverity] =
    useState(7);

  const [
    durationHours,
    setDurationHours,
  ] = useState(6);

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const simulate = async () => {
    try {
      setLoading(true);

      const data =
        await runWhatIf({
          disruption_type:
            disruptionType,

          severity:
            Number(severity),

          duration_hours:
            Number(durationHours),
        });

      setResult(data);
    } catch (error) {
      console.error(
        "Simulation error:",
        error
      );

      alert(
        "Simulation failed. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "28px" }}>
      <h1>What-If Simulator</h1>

      <p
        style={{
          color: "#94a3b8",
          marginBottom: "25px",
        }}
      >
        Simulate supply-chain disruptions before they
        happen and measure their potential impact.
      </p>

      <div style={cardStyle}>
        <h2>Build Scenario</h2>

        <div style={formGridStyle}>
          <div>
            <label style={labelStyle}>
              Disruption Type
            </label>

            <select
              value={disruptionType}
              onChange={(event) =>
                setDisruptionType(
                  event.target.value
                )
              }
              style={inputStyle}
            >
              <option>Flood</option>
              <option>
                Road Closure
              </option>
              <option>
                Supplier Delay
              </option>
              <option>
                Factory Breakdown
              </option>
              <option>
                Port Disruption
              </option>
              <option>
                Severe Weather
              </option>
            </select>
          </div>

          <div>
            <label style={labelStyle}>
              Severity: {severity}/10
            </label>

            <input
              type="range"
              min="1"
              max="10"
              value={severity}
              onChange={(event) =>
                setSeverity(
                  event.target.value
                )
              }
              style={{
                width: "100%",
              }}
            />
          </div>

          <div>
            <label style={labelStyle}>
              Duration (hours)
            </label>

            <input
              type="number"
              min="1"
              value={durationHours}
              onChange={(event) =>
                setDurationHours(
                  event.target.value
                )
              }
              style={inputStyle}
            />
          </div>
        </div>

        <button
          onClick={simulate}
          style={simulateButtonStyle}
        >
          <Play size={17} />

          {loading
            ? "Running Simulation..."
            : "Run Simulation"}
        </button>
      </div>

      {result && (
        <>
          <div
            style={{
              ...gridStyle,
              marginTop: "22px",
            }}
          >
            <ResultCard
              icon={
                <AlertTriangle />
              }
              title="Affected Shipments"
              value={
                result.affected_shipments ??
                "-"
              }
            />

            <ResultCard
              icon={<Clock />}
              title="Expected Delay"
              value={`${
                result.expected_delay_hours ??
                result.delay_hours ??
                "-"
              } h`}
            />

            <ResultCard
              icon={
                <IndianRupee />
              }
              title="Financial Exposure"
              value={`₹${Number(
                result.financial_exposure ||
                  0
              ).toLocaleString(
                "en-IN"
              )}`}
            />

            <ResultCard
              icon={
                <ShieldCheck />
              }
              title="Potential Saving"
              value={`₹${Number(
                result.potential_saving ||
                  0
              ).toLocaleString(
                "en-IN"
              )}`}
            />
          </div>

          <div
            style={{
              ...cardStyle,
              marginTop: "22px",
            }}
          >
            <h2>
              ChainTwin Recommendation
            </h2>

            <div
              style={{
                background:
                  "rgba(34,197,94,.08)",
                border:
                  "1px solid rgba(34,197,94,.25)",
                padding: "18px",
                borderRadius: "12px",
                marginTop: "15px",
              }}
            >
              <strong
                style={{
                  color: "#4ade80",
                }}
              >
                OPTIMIZATION RESPONSE
              </strong>

              <p>
                {result.recommendation ||
                  "Optimization scenario generated."}
              </p>
            </div>

            <div
              style={{
                ...gridStyle,
                marginTop: "18px",
              }}
            >
              <ResultCard
                title="Production Risk"
                value={
                  result.production_risk ??
                  "-"
                }
              />

              <ResultCard
                title="Optimized Exposure"
                value={`₹${Number(
                  result.optimized_exposure ||
                    0
                ).toLocaleString(
                  "en-IN"
                )}`}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function ResultCard({
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

const formGridStyle = {
  display: "grid",
  gridTemplateColumns:
    "repeat(auto-fit,minmax(220px,1fr))",
  gap: "20px",
  marginTop: "20px",
};

const labelStyle = {
  display: "block",
  color: "#cbd5e1",
  marginBottom: "8px",
};

const inputStyle = {
  width: "100%",
  background: "#0b1220",
  color: "white",
  border: "1px solid #334155",
  padding: "11px",
  borderRadius: "8px",
};

const simulateButtonStyle = {
  marginTop: "22px",
  display: "flex",
  gap: "8px",
  alignItems: "center",
  background: "#2563eb",
  color: "white",
  border: "none",
  padding: "12px 18px",
  borderRadius: "9px",
  cursor: "pointer",
  fontWeight: "700",
};

export default WhatIf;