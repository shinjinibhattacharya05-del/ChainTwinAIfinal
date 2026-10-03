import { useEffect, useState } from "react";

import {
  AlertTriangle,
  ArrowRight,
  BrainCircuit,
  RefreshCw,
  ShieldCheck,
  TrendingDown,
  Truck,
  Zap,
} from "lucide-react";

import KPICard from "../components/KPICard";
import LiveMap from "../components/LiveMap";
import RecommendationCard from "../components/RecommendationCard";

import {
  getDashboard,
  getRecommendations,
} from "../services/api";


function Dashboard() {

  const [dashboard, setDashboard] =
    useState(null);

  const [
    recommendations,
    setRecommendations,
  ] = useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [lastUpdated, setLastUpdated] =
    useState(new Date());


  // ======================================================
  // LOAD BACKEND DATA
  // ======================================================

  const loadDashboard = async () => {

    try {

      setLoading(true);
      setError("");

      const [
        dashboardData,
        recommendationData,
      ] = await Promise.all([
        getDashboard(),
        getRecommendations(),
      ]);

      setDashboard(
        dashboardData
      );

      setRecommendations(
        recommendationData
      );

      setLastUpdated(
        new Date()
      );

    } catch (err) {

      console.error(
        "ChainTwin backend error:",
        err
      );

      setError(
        "Unable to connect to the ChainTwin backend."
      );

    } finally {

      setLoading(false);

    }
  };


  // ======================================================
  // INITIAL LOAD
  // ======================================================

  useEffect(() => {

    loadDashboard();

  }, []);


  // ======================================================
  // MONEY FORMAT
  // ======================================================

  const formatMoney = (amount = 0) => {

    if (amount >= 10000000) {

      return `₹${(
        amount / 10000000
      ).toFixed(2)}Cr`;

    }

    if (amount >= 100000) {

      return `₹${(
        amount / 100000
      ).toFixed(2)}L`;

    }

    if (amount >= 1000) {

      return `₹${(
        amount / 1000
      ).toFixed(1)}K`;

    }

    return `₹${amount}`;
  };


  // ======================================================
  // LOADING
  // ======================================================

  if (loading) {

    return (

      <div className="dashboard-page">

        <div className="loading-screen">

          <RefreshCw
            size={32}
            className="spin"
          />

          <h2>
            Loading ChainTwin Intelligence
          </h2>

          <p>
            Synchronizing supply-chain
            digital twin...
          </p>

        </div>

      </div>
    );
  }


  // ======================================================
  // ERROR
  // ======================================================

  if (error || !dashboard) {

    return (

      <div className="dashboard-page">

        <div className="error-panel">

          <AlertTriangle
            size={38}
          />

          <h2>
            Backend Connection Error
          </h2>

          <p>
            {error ||
              "Dashboard data unavailable."}
          </p>

          <p>
            Make sure FastAPI is running
            on port 8000.
          </p>

          <button
            className="primary-btn"
            onClick={loadDashboard}
          >

            <RefreshCw size={16} />

            Try Again

          </button>

        </div>

      </div>
    );
  }


  const disruption =
    dashboard.active_disruption;


  // ======================================================
  // PAGE
  // ======================================================

  return (

    <div className="dashboard-page">


      {/* HERO */}

      <section className="dashboard-hero">

        <div>

          <div className="eyebrow">
            CHAINTWIN COMMAND CENTER
          </div>

          <h1>
            Your network needs attention.
          </h1>

          <p>
            Real-time supply-chain risk,
            financial exposure and decision
            intelligence.
          </p>

        </div>


        <div className="hero-status">

          <div className="live-indicator">

            <span className="live-dot" />

            LIVE INTELLIGENCE

          </div>


          <span className="updated-text">

            Updated{" "}

            {lastUpdated.toLocaleTimeString(
              [],
              {
                hour: "2-digit",
                minute: "2-digit",
              }
            )}

          </span>


          <button
            className="refresh-button"
            onClick={loadDashboard}
          >

            <RefreshCw size={16} />

            Refresh

          </button>

        </div>

      </section>


      {/* KPI CARDS */}

      <section className="kpi-grid">

        <KPICard
          title="Financial Exposure"
          value={formatMoney(
            dashboard.financial_exposure
          )}
          subtitle="Current network exposure"
          icon={TrendingDown}
        />


        <KPICard
          title="Network Risk"
          value={`${dashboard.network_risk}/100`}
          subtitle="High attention required"
          icon={AlertTriangle}
        />


        <KPICard
          title="Active Shipments"
          value={
            dashboard.active_shipments
          }
          subtitle="Across monitored routes"
          icon={Truck}
        />


        <KPICard
          title="Factory Efficiency"
          value={`${dashboard.factory_efficiency}%`}
          subtitle="Current efficiency"
          icon={Zap}
        />

      </section>


      {/* LIVE NETWORK TITLE */}

      <section className="section-header">

        <div>

          <span className="section-label">
            LIVE NETWORK
          </span>

          <h2>
            Supply Chain Digital Twin
          </h2>

        </div>


        <div className="section-status">

          <span className="status-dot" />

          Monitoring

        </div>

      </section>


      {/* MAP + INTELLIGENCE */}

      <section className="network-grid">


        <div className="map-panel">

          <div className="panel-heading">

            <div>

              <span className="panel-label">
                LIVE SHIPMENT MAP
              </span>

              <h3>
                Kolkata → Bhubaneswar
              </h3>

            </div>


            <div className="risk-badge">
              HIGH RISK
            </div>

          </div>


          <LiveMap />

        </div>


        {/* DISRUPTION */}

        <div className="intelligence-panel">

          <div className="panel-heading">

            <div>

              <span className="panel-label">
                DISRUPTION INTELLIGENCE
              </span>

              <h3>
                {disruption.name}
              </h3>

            </div>

            <AlertTriangle
              size={22}
            />

          </div>


          <div className="alert-box">

            <div className="alert-icon">

              <AlertTriangle
                size={20}
              />

            </div>


            <div>

              <strong>
                Active disruption detected
              </strong>

              <p>
                High-risk disruption
                affecting the current
                shipment corridor.
              </p>

            </div>

          </div>


          <div className="exposure-list">


            <div className="exposure-row">

              <span>
                Severity
              </span>

              <strong>
                {disruption.severity}
              </strong>

            </div>


            <div className="exposure-row">

              <span>
                Current Exposure
              </span>

              <strong>

                {formatMoney(
                  disruption.current_exposure
                )}

              </strong>

            </div>


            <div className="exposure-row">

              <span>
                Optimized Exposure
              </span>

              <strong className="positive-text">

                {formatMoney(
                  disruption.optimized_exposure
                )}

              </strong>

            </div>

          </div>


          <div className="saving-card">

            <div className="saving-icon">

              <ShieldCheck
                size={24}
              />

            </div>


            <div>

              <span>
                POTENTIAL LOSS AVOIDED
              </span>

              <h2>

                {formatMoney(
                  disruption.potential_loss_avoided
                )}

              </h2>

              <p>
                if recommended intervention
                is executed now
              </p>

            </div>

          </div>


          <button
            className="primary-btn full-width"
          >

            View Optimized Route

            <ArrowRight
              size={17}
            />

          </button>

        </div>

      </section>


      {/* RECOMMENDATIONS */}

      <section className="recommendation-section">


        <div className="section-header">

          <div>

            <span className="section-label">
              DECISION INTELLIGENCE
            </span>

            <h2>
              Recommended Actions
            </h2>

            <p>
              Preventive actions generated
              from current network risk.
            </p>

          </div>


          <div className="ai-badge">

            <BrainCircuit
              size={17}
            />

            AI DECISION ENGINE

          </div>

        </div>


        <div className="recommendation-grid">

          {recommendations.length > 0 ? (

            recommendations.map(
              (item) => (

                <RecommendationCard
                  key={item.id}
                  priority={
                    item.priority
                  }
                  title={
                    item.title
                  }
                  description={
                    item.description
                  }
                  saving={
                    formatMoney(
                      item.expected_saving
                    )
                  }
                  confidence={
                    item.confidence
                  }
                  metric={
                    `${item.before} → ${item.after}`
                  }
                  onSimulate={() =>
                    console.log(
                      "Simulating:",
                      item.title
                    )
                  }
                />

              )
            )

          ) : (

            <div className="empty-state">

              <ShieldCheck
                size={30}
              />

              <h3>
                Network stable
              </h3>

              <p>
                No urgent recommendations
                available.
              </p>

            </div>

          )}

        </div>

      </section>


      {/* SUMMARY */}

      <section className="decision-summary">

        <div>

          <span className="section-label">
            CHAINTWIN ASSESSMENT
          </span>

          <h2>
            Prevent disruption before
            it becomes financial loss.
          </h2>

          <p>

            ChainTwin currently identifies{" "}

            <strong>

              {formatMoney(
                disruption.potential_loss_avoided
              )}

            </strong>

            {" "}in potentially avoidable
            loss from the active disruption.

          </p>

        </div>


        <div className="decision-summary-icon">

          <BrainCircuit
            size={40}
          />

        </div>

      </section>

    </div>
  );
}


export default Dashboard;