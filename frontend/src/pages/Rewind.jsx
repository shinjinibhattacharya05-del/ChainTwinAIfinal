import {
  useEffect,
  useState,
} from "react";

import {
  History,
  AlertTriangle,
  Clock,
  IndianRupee,
  ShieldCheck,
  ArrowRight,
} from "lucide-react";

import {
  getRewind,
} from "../services/api";

function Rewind() {
  const [data, setData] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const loadRewind = async () => {
      try {
        const result =
          await getRewind();

        setData(result);
      } catch (error) {
        console.error(
          "Rewind API error:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadRewind();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: "28px" }}>
        Reconstructing disruption...
      </div>
    );
  }

  if (!data) {
    return (
      <div style={{ padding: "28px" }}>
        Rewind data unavailable.
      </div>
    );
  }

  const event =
    data.event ||
    data.disruption ||
    "Historical Disruption";

  const actualLoss =
    data.actual_loss || 0;

  const actualDelay =
    data.actual_delay_hours ||
    data.actual_delay ||
    0;

  const intervention =
    data.intervention ||
    "Earlier intervention";

  const counterfactualLoss =
    data.counterfactual_loss ||
    0;

  const avoidableLoss =
    data.avoidable_loss ||
    data.loss_avoided ||
    0;

  return (
    <div style={{ padding: "28px" }}>
      <div
        style={{
          display: "flex",
          gap: "12px",
          alignItems: "center",
        }}
      >
        <History size={28} />

        <div>
          <h1>Rewind Engine</h1>

          <p style={mutedStyle}>
            Replay historical disruptions and discover
            which earlier decisions could have reduced
            losses.
          </p>
        </div>
      </div>

      <div
        style={{
          ...cardStyle,
          marginTop: "25px",
        }}
      >
        <span
          style={{
            color: "#f87171",
            fontWeight: "700",
          }}
        >
          HISTORICAL EVENT
        </span>

        <h2>{event}</h2>

        <p style={mutedStyle}>
          ChainTwin reconstructed the disruption and
          compared the actual outcome with an optimized
          counterfactual response.
        </p>
      </div>

      <div
        style={{
          ...comparisonGrid,
          marginTop: "22px",
        }}
      >
        <div
          style={{
            ...cardStyle,
            border:
              "1px solid rgba(239,68,68,.35)",
          }}
        >
          <AlertTriangle
            color="#ef4444"
          />

          <h2>What Actually Happened</h2>

          <DataRow
            icon={<IndianRupee />}
            title="Financial Loss"
            value={`₹${Number(
              actualLoss
            ).toLocaleString(
              "en-IN"
            )}`}
          />

          <DataRow
            icon={<Clock />}
            title="Delay"
            value={`${actualDelay} h`}
          />

          <div
            style={{
              marginTop: "18px",
              color: "#fca5a5",
            }}
          >
            Reactive response after the
            disruption had already affected
            operations.
          </div>
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <ArrowRight size={32} />
        </div>

        <div
          style={{
            ...cardStyle,
            border:
              "1px solid rgba(34,197,94,.35)",
          }}
        >
          <ShieldCheck
            color="#22c55e"
          />

          <h2>ChainTwin Rewind</h2>

          <DataRow
            title="Earlier Intervention"
            value={intervention}
          />

          <DataRow
            icon={<IndianRupee />}
            title="Counterfactual Loss"
            value={`₹${Number(
              counterfactualLoss
            ).toLocaleString(
              "en-IN"
            )}`}
          />

          <div
            style={{
              marginTop: "18px",
              color: "#86efac",
            }}
          >
            ChainTwin tests what could have
            happened if action had been taken
            earlier.
          </div>
        </div>
      </div>

      <div
        style={{
          ...cardStyle,
          marginTop: "22px",
          background:
            "rgba(34,197,94,.07)",
        }}
      >
        <span style={mutedStyle}>
          AVOIDABLE LOSS
        </span>

        <h1
          style={{
            color: "#4ade80",
          }}
        >
          ₹
          {Number(
            avoidableLoss
          ).toLocaleString("en-IN")}
        </h1>

        <p>
          {data.lesson ||
            "Earlier disruption intelligence could have reduced financial exposure."}
        </p>
      </div>
    </div>
  );
}

function DataRow({
  icon,
  title,
  value,
}) {
  return (
    <div
      style={{
        marginTop: "18px",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "7px",
          color: "#94a3b8",
          alignItems: "center",
        }}
      >
        {icon}
        {title}
      </div>

      <strong>
        {value}
      </strong>
    </div>
  );
}

const cardStyle = {
  background: "rgba(15,23,42,.85)",
  border: "1px solid #1e293b",
  borderRadius: "14px",
  padding: "22px",
};

const mutedStyle = {
  color: "#94a3b8",
};

const comparisonGrid = {
  display: "grid",
  gridTemplateColumns:
    "minmax(250px,1fr) 50px minmax(250px,1fr)",
  gap: "15px",
};

export default Rewind;

