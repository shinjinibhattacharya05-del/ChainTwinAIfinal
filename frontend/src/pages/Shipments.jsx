import { useEffect, useState } from "react";
import {
  Truck,
  MapPin,
  AlertTriangle,
  Clock,
  Package,
  RefreshCw,
} from "lucide-react";

import { getShipments } from "../services/api";

function Shipments() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadShipments = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getShipments();
      setShipments(data);
    } catch (error) {
      console.error(error);
      setError("Could not load shipments.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadShipments();
  }, []);

  const statusColor = (status) => {
    if (status === "On Time") return "#22c55e";
    if (status === "At Risk") return "#f59e0b";
    if (status === "Delayed") return "#ef4444";
    return "#94a3b8";
  };

  const riskColor = (risk) => {
    if (risk >= 70) return "#ef4444";
    if (risk >= 40) return "#f59e0b";
    return "#22c55e";
  };

  if (loading) {
    return (
      <div style={{ padding: "28px" }}>
        Loading shipments...
      </div>
    );
  }

  return (
    <div style={{ padding: "28px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "25px",
        }}
      >
        <div>
          <h1>Live Shipments</h1>

          <p style={{ color: "#94a3b8" }}>
            Real-time shipment monitoring and risk intelligence.
          </p>
        </div>

        <button
          onClick={loadShipments}
          style={buttonStyle}
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </div>

      {error && (
        <div style={errorStyle}>
          {error}
        </div>
      )}

      <div style={gridStyle}>
        {shipments.map((shipment) => (
          <div
            key={shipment.shipment_id}
            style={cardStyle}
          >
            <div style={rowStyle}>
              <div
                style={{
                  display: "flex",
                  gap: "8px",
                  alignItems: "center",
                }}
              >
                <Truck size={20} />

                <strong>
                  {shipment.shipment_id}
                </strong>
              </div>

              <strong
                style={{
                  color: statusColor(
                    shipment.status
                  ),
                }}
              >
                {shipment.status}
              </strong>
            </div>

            <p>
              <Package size={15} />{" "}
              {shipment.material}
            </p>

            <p style={mutedStyle}>
              Supplier: {shipment.supplier}
            </p>

            <p>
              <MapPin size={15} />{" "}
              {shipment.origin} →{" "}
              {shipment.destination}
            </p>

            <div style={{ marginTop: "15px" }}>
              <div style={rowStyle}>
                <span>Progress</span>

                <strong>
                  {shipment.progress}%
                </strong>
              </div>

              <div style={progressTrackStyle}>
                <div
                  style={{
                    ...progressFillStyle,
                    width: `${shipment.progress}%`,
                  }}
                />
              </div>
            </div>

            <div
              style={{
                ...rowStyle,
                marginTop: "16px",
              }}
            >
              <span>
                <AlertTriangle size={15} /> Risk
              </span>

              <strong
                style={{
                  color: riskColor(
                    shipment.risk
                  ),
                }}
              >
                {shipment.risk}/100
              </strong>
            </div>

            <div style={rowStyle}>
              <span>
                <Clock size={15} /> Delay
              </span>

              <span>
                {shipment.delay_hours} h
              </span>
            </div>

            <div
              style={{
                ...rowStyle,
                borderTop:
                  "1px solid #1e293b",
                paddingTop: "14px",
                marginTop: "14px",
              }}
            >
              <span style={mutedStyle}>
                Shipment Value
              </span>

              <strong>
                ₹
                {Number(
                  shipment.value
                ).toLocaleString("en-IN")}
              </strong>
            </div>
          </div>
        ))}
      </div>
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
    "repeat(auto-fit,minmax(290px,1fr))",
  gap: "18px",
};

const rowStyle = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "10px",
  marginBottom: "10px",
};

const mutedStyle = {
  color: "#94a3b8",
};

const progressTrackStyle = {
  height: "7px",
  background: "#1e293b",
  borderRadius: "20px",
  overflow: "hidden",
};

const progressFillStyle = {
  height: "100%",
  background: "#38bdf8",
};

const buttonStyle = {
  display: "flex",
  gap: "7px",
  alignItems: "center",
  padding: "10px 15px",
  background: "#0f172a",
  color: "white",
  border: "1px solid #334155",
  borderRadius: "8px",
  cursor: "pointer",
};

const errorStyle = {
  background: "rgba(239,68,68,.12)",
  color: "#f87171",
  padding: "14px",
  borderRadius: "10px",
  marginBottom: "15px",
};

export default Shipments;