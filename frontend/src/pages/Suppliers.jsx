import {
  useEffect,
  useState,
} from "react";

import {
  Building2,
  Package,
  AlertTriangle,
  Truck,
} from "lucide-react";

import {
  getShipments,
} from "../services/api";

function Suppliers() {
  const [suppliers, setSuppliers] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const loadSuppliers = async () => {
      try {
        const shipments =
          await getShipments();

        const grouped = {};

        shipments.forEach(
          (shipment) => {
            const name =
              shipment.supplier;

            if (!grouped[name]) {
              grouped[name] = {
                name,
                shipments: 0,
                totalRisk: 0,
                totalValue: 0,
                delayed: 0,
                materials: [],
              };
            }

            grouped[name].shipments += 1;

            grouped[name].totalRisk +=
              Number(
                shipment.risk || 0
              );

            grouped[name].totalValue +=
              Number(
                shipment.value || 0
              );

            if (
              shipment.status ===
                "Delayed" ||
              shipment.status ===
                "At Risk"
            ) {
              grouped[name].delayed += 1;
            }

            if (
              !grouped[
                name
              ].materials.includes(
                shipment.material
              )
            ) {
              grouped[
                name
              ].materials.push(
                shipment.material
              );
            }
          }
        );

        const result = Object.values(
          grouped
        ).map((supplier) => {
          const averageRisk =
            supplier.shipments
              ? Math.round(
                  supplier.totalRisk /
                    supplier.shipments
                )
              : 0;

          const reliability =
            Math.max(
              0,
              100 - averageRisk
            );

          return {
            ...supplier,
            averageRisk,
            reliability,
          };
        });

        setSuppliers(result);
      } catch (error) {
        console.error(
          "Supplier API error:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadSuppliers();
  }, []);

  const riskColor = (risk) => {
    if (risk >= 70) return "#ef4444";
    if (risk >= 40) return "#f59e0b";
    return "#22c55e";
  };

  if (loading) {
    return (
      <div style={{ padding: "28px" }}>
        Loading supplier intelligence...
      </div>
    );
  }

  return (
    <div style={{ padding: "28px" }}>
      <h1>Supplier Intelligence</h1>

      <p
        style={{
          color: "#94a3b8",
          marginBottom: "25px",
        }}
      >
        Supplier reliability, shipment exposure and
        material dependency.
      </p>

      <div style={gridStyle}>
        {suppliers.map(
          (supplier) => (
            <div
              key={supplier.name}
              style={cardStyle}
            >
              <div style={rowStyle}>
                <div
                  style={{
                    display: "flex",
                    gap: "9px",
                    alignItems: "center",
                  }}
                >
                  <Building2
                    size={21}
                  />

                  <strong>
                    {supplier.name}
                  </strong>
                </div>

                <span
                  style={{
                    color: riskColor(
                      supplier.averageRisk
                    ),
                    fontWeight: "700",
                  }}
                >
                  Risk{" "}
                  {supplier.averageRisk}
                </span>
              </div>

              <div style={sectionStyle}>
                <Package size={16} />

                <span>
                  Materials:{" "}
                  {supplier.materials.join(
                    ", "
                  )}
                </span>
              </div>

              <div style={sectionStyle}>
                <Truck size={16} />

                <span>
                  Active Shipments:{" "}
                  {supplier.shipments}
                </span>
              </div>

              <div style={sectionStyle}>
                <AlertTriangle
                  size={16}
                />

                <span>
                  At Risk / Delayed:{" "}
                  {supplier.delayed}
                </span>
              </div>

              <div
                style={{
                  marginTop: "18px",
                }}
              >
                <div style={rowStyle}>
                  <span>
                    Reliability
                  </span>

                  <strong>
                    {supplier.reliability}%
                  </strong>
                </div>

                <div style={trackStyle}>
                  <div
                    style={{
                      height: "100%",
                      width:
                        `${supplier.reliability}%`,
                      background:
                        supplier.reliability >=
                        70
                          ? "#22c55e"
                          : "#f59e0b",
                    }}
                  />
                </div>
              </div>

              <div
                style={{
                  ...rowStyle,
                  marginTop: "18px",
                  paddingTop: "14px",
                  borderTop:
                    "1px solid #1e293b",
                }}
              >
                <span
                  style={{
                    color: "#94a3b8",
                  }}
                >
                  Financial Exposure
                </span>

                <strong>
                  ₹
                  {supplier.totalValue.toLocaleString(
                    "en-IN"
                  )}
                </strong>
              </div>
            </div>
          )
        )}
      </div>
    </div>
  );
}

const gridStyle = {
  display: "grid",
  gridTemplateColumns:
    "repeat(auto-fit,minmax(290px,1fr))",
  gap: "18px",
};

const cardStyle = {
  background: "rgba(15,23,42,.85)",
  border: "1px solid #1e293b",
  borderRadius: "14px",
  padding: "20px",
};

const rowStyle = {
  display: "flex",
  justifyContent: "space-between",
  gap: "12px",
  alignItems: "center",
};

const sectionStyle = {
  display: "flex",
  alignItems: "center",
  gap: "8px",
  color: "#cbd5e1",
  marginTop: "15px",
};

const trackStyle = {
  height: "7px",
  background: "#1e293b",
  borderRadius: "10px",
  overflow: "hidden",
  marginTop: "8px",
};

export default Suppliers;