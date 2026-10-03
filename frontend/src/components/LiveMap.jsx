import { useEffect, useMemo, useState } from "react";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  Circle,
  useMapEvents,
} from "react-leaflet";

import L from "leaflet";


// =====================================================
// ICONS
// =====================================================

const pickupIcon = L.divIcon({
  html: `
    <div style="
      width:42px;
      height:42px;
      border-radius:50%;
      background:#16a34a;
      border:3px solid white;
      display:flex;
      justify-content:center;
      align-items:center;
      font-size:22px;
      box-shadow:0 4px 14px rgba(0,0,0,.45);
    ">
      📍
    </div>
  `,
  className: "",
  iconSize: [42, 42],
  iconAnchor: [21, 42],
});


const destinationIcon = L.divIcon({
  html: `
    <div style="
      width:42px;
      height:42px;
      border-radius:50%;
      background:#2563eb;
      border:3px solid white;
      display:flex;
      justify-content:center;
      align-items:center;
      font-size:22px;
      box-shadow:0 4px 14px rgba(0,0,0,.45);
    ">
      🏁
    </div>
  `,
  className: "",
  iconSize: [42, 42],
  iconAnchor: [21, 42],
});


const truckIcon = L.divIcon({
  html: `
    <div style="
      width:44px;
      height:44px;
      border-radius:50%;
      background:white;
      border:3px solid #06b6d4;
      display:flex;
      justify-content:center;
      align-items:center;
      font-size:25px;
      box-shadow:0 4px 14px rgba(0,0,0,.45);
    ">
      🚚
    </div>
  `,
  className: "",
  iconSize: [44, 44],
  iconAnchor: [22, 22],
});


// =====================================================
// MAP CLICK HANDLER
// =====================================================

function MapClickHandler({
  selectionMode,
  setPickup,
  setDestination,
}) {
  useMapEvents({
    click(event) {
      const point = [
        event.latlng.lat,
        event.latlng.lng,
      ];

      if (selectionMode === "pickup") {
        setPickup(point);
      }

      if (selectionMode === "destination") {
        setDestination(point);
      }
    },
  });

  return null;
}


// =====================================================
// CREATE POINTS BETWEEN PICKUP + DESTINATION
// =====================================================

function createRoutePoints(start, end, steps = 30) {
  if (!start || !end) {
    return [];
  }

  const points = [];

  for (let i = 0; i <= steps; i++) {
    const percentage = i / steps;

    const lat =
      start[0] +
      (end[0] - start[0]) * percentage;

    const lng =
      start[1] +
      (end[1] - start[1]) * percentage;

    points.push([lat, lng]);
  }

  return points;
}


// =====================================================
// DISTANCE CALCULATION
// =====================================================

function calculateDistance(point1, point2) {
  if (!point1 || !point2) {
    return 0;
  }

  const earthRadius = 6371;

  const lat1 = point1[0] * Math.PI / 180;
  const lat2 = point2[0] * Math.PI / 180;

  const deltaLat =
    (point2[0] - point1[0]) *
    Math.PI /
    180;

  const deltaLng =
    (point2[1] - point1[1]) *
    Math.PI /
    180;

  const a =
    Math.sin(deltaLat / 2) ** 2 +
    Math.cos(lat1) *
      Math.cos(lat2) *
      Math.sin(deltaLng / 2) ** 2;

  const c =
    2 *
    Math.atan2(
      Math.sqrt(a),
      Math.sqrt(1 - a)
    );

  return earthRadius * c;
}


// =====================================================
// MAIN COMPONENT
// =====================================================

function LiveMap() {

  // Default demo locations
  // User can replace them by clicking map.

  const [pickup, setPickup] = useState([
    22.4979,
    88.3109,
  ]);

  const [destination, setDestination] = useState([
    22.5867,
    88.4171,
  ]);


  const [selectionMode, setSelectionMode] =
    useState(null);


  const [truckPosition, setTruckPosition] =
    useState([
      22.4979,
      88.3109,
    ]);


  const [progress, setProgress] =
    useState(0);


  const [status, setStatus] =
    useState("READY");


  const [simulationStarted, setSimulationStarted] =
    useState(false);


  // User-controlled geofence radius
  const [geofenceRadius, setGeofenceRadius] =
    useState(1200);


  // =================================================
  // ROUTE
  // =================================================

  const routePoints = useMemo(() => {
    return createRoutePoints(
      pickup,
      destination,
      40
    );
  }, [pickup, destination]);


  // =================================================
  // GEOFENCE LOCATION
  // Middle of selected route
  // =================================================

  const geofenceCenter = useMemo(() => {

    if (!pickup || !destination) {
      return null;
    }

    return [
      (pickup[0] + destination[0]) / 2,
      (pickup[1] + destination[1]) / 2,
    ];

  }, [pickup, destination]);


  // =================================================
  // DISTANCE
  // =================================================

  const distance = useMemo(() => {

    return calculateDistance(
      pickup,
      destination
    );

  }, [pickup, destination]);


  // =================================================
  // RESET TRUCK WHEN LOCATIONS CHANGE
  // =================================================

  useEffect(() => {

    if (pickup) {
      setTruckPosition(pickup);
    }

    setProgress(0);
    setStatus("READY");
    setSimulationStarted(false);

  }, [pickup, destination]);


  // =================================================
  // VEHICLE SIMULATION
  // =================================================

  useEffect(() => {

    if (!simulationStarted) {
      return;
    }

    if (routePoints.length === 0) {
      return;
    }

    let currentIndex = 0;

    setTruckPosition(routePoints[0]);
    setStatus("IN TRANSIT");
    setProgress(0);


    const interval = setInterval(() => {

      currentIndex += 1;


      if (currentIndex >= routePoints.length) {

        clearInterval(interval);

        setTruckPosition(
          routePoints[
            routePoints.length - 1
          ]
        );

        setProgress(100);
        setStatus("ARRIVED");

        setSimulationStarted(false);

        return;
      }


      setTruckPosition(
        routePoints[currentIndex]
      );


      const currentProgress =
        Math.round(
          (
            currentIndex /
            (routePoints.length - 1)
          ) * 100
        );


      setProgress(currentProgress);

    }, 700);


    return () => {
      clearInterval(interval);
    };

  }, [
    simulationStarted,
    routePoints,
  ]);


  // =================================================
  // CHECK WHETHER TRUCK IS INSIDE GEOFENCE
  // =================================================

  const distanceFromGeofence =
    geofenceCenter
      ? calculateDistance(
          truckPosition,
          geofenceCenter
        ) * 1000
      : 999999;


  const insideGeofence =
    distanceFromGeofence <=
    geofenceRadius;


  // =================================================
  // START VEHICLE
  // =================================================

  const startVehicle = () => {

    if (!pickup || !destination) {
      alert(
        "Please choose pickup and destination first."
      );

      return;
    }

    setTruckPosition(pickup);
    setProgress(0);
    setStatus("IN TRANSIT");
    setSimulationStarted(true);
  };


  // =================================================
  // RESET
  // =================================================

  const resetMap = () => {

    setPickup(null);

    setDestination(null);

    setTruckPosition([
      22.5726,
      88.3639,
    ]);

    setProgress(0);

    setStatus("READY");

    setSimulationStarted(false);

    setSelectionMode(null);
  };


  // =================================================
  // UI
  // =================================================

  return (

    <div
      style={{
        width: "100%",
      }}
    >

      {/* ============================================
          CONTROLS
      ============================================ */}

      <div
        style={{
          display: "flex",
          gap: "10px",
          flexWrap: "wrap",
          marginBottom: "14px",
          alignItems: "center",
        }}
      >

        <button
          onClick={() =>
            setSelectionMode("pickup")
          }
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
            fontWeight: "600",
            background:
              selectionMode === "pickup"
                ? "#16a34a"
                : "#1e293b",
            color: "white",
          }}
        >
          📍 Choose Pickup
        </button>


        <button
          onClick={() =>
            setSelectionMode(
              "destination"
            )
          }
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
            fontWeight: "600",
            background:
              selectionMode ===
              "destination"
                ? "#2563eb"
                : "#1e293b",
            color: "white",
          }}
        >
          🏁 Choose Destination
        </button>


        <button
          onClick={startVehicle}
          disabled={
            !pickup ||
            !destination ||
            simulationStarted
          }
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
            fontWeight: "700",
            background: "#06b6d4",
            color: "#07111f",
          }}
        >
          🚚 Start Shipment
        </button>


        <button
          onClick={resetMap}
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border:
              "1px solid #475569",
            cursor: "pointer",
            background: "#0f172a",
            color: "white",
          }}
        >
          Reset
        </button>

      </div>


      {/* ============================================
          INSTRUCTIONS
      ============================================ */}

      <div
        style={{
          marginBottom: "12px",
          padding: "10px 14px",
          borderRadius: "8px",
          background:
            "rgba(15,23,42,.75)",
          border:
            "1px solid rgba(148,163,184,.15)",
          color: "#cbd5e1",
          fontSize: "13px",
        }}
      >

        {selectionMode === "pickup" && (
          <>
            📍 Click anywhere on the map
            to choose the pickup point.
          </>
        )}


        {selectionMode ===
          "destination" && (
          <>
            🏁 Click anywhere on the map
            to choose the destination.
          </>
        )}


        {!selectionMode && (
          <>
            Select Pickup or Destination,
            then click on the map.
          </>
        )}

      </div>


      {/* ============================================
          MAP CONTAINER
      ============================================ */}

      <div
        style={{
          position: "relative",
        }}
      >


        {/* ==========================================
            LIVE INFORMATION PANEL
        ========================================== */}

        <div
          style={{
            position: "absolute",
            zIndex: 1000,
            top: "14px",
            left: "14px",
            background:
              "rgba(7,15,30,.94)",
            color: "white",
            padding: "14px 16px",
            borderRadius: "12px",
            minWidth: "220px",
            fontSize: "13px",
            lineHeight: "1.7",
            border:
              "1px solid rgba(255,255,255,.12)",
            boxShadow:
              "0 6px 20px rgba(0,0,0,.35)",
          }}
        >

          <strong>
            🚚 SHP-001
          </strong>

          <div>
            Status: {status}
          </div>

          <div>
            Progress: {progress}%
          </div>

          <div>
            Distance:{" "}
            {distance.toFixed(2)} km
          </div>


          <div
            style={{
              color: insideGeofence
                ? "#f87171"
                : "#4ade80",
              fontWeight: "700",
              marginTop: "5px",
            }}
          >

            {insideGeofence
              ? "⚠ VEHICLE INSIDE GEOFENCE"
              : "● Vehicle outside geofence"}

          </div>

        </div>


        {/* ==========================================
            MAP
        ========================================== */}

        <MapContainer
          center={[
            22.545,
            88.365,
          ]}
          zoom={12}
          style={{
            width: "100%",
            height: "520px",
            borderRadius: "16px",
          }}
        >

          <TileLayer
            attribution={
              "© OpenStreetMap contributors"
            }
            url={
              "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            }
          />


          {/* ========================================
              USER CLICK
          ======================================== */}

          <MapClickHandler
            selectionMode={
              selectionMode
            }
            setPickup={(point) => {

              setPickup(point);

              setSelectionMode(null);

            }}
            setDestination={(point) => {

              setDestination(point);

              setSelectionMode(null);

            }}
          />


          {/* ========================================
              ROUTE
          ======================================== */}

          {pickup &&
            destination && (

            <Polyline
              positions={
                routePoints
              }
              pathOptions={{
                color: "#38bdf8",
                weight: 6,
                opacity: 0.9,
              }}
            />

          )}


          {/* ========================================
              PICKUP
          ======================================== */}

          {pickup && (

            <Marker
              position={pickup}
              icon={pickupIcon}
            >

              <Popup>

                <strong>
                  📍 Pickup Point
                </strong>

                <br />

                Latitude:{" "}
                {pickup[0].toFixed(5)}

                <br />

                Longitude:{" "}
                {pickup[1].toFixed(5)}

              </Popup>

            </Marker>

          )}


          {/* ========================================
              DESTINATION
          ======================================== */}

          {destination && (

            <Marker
              position={destination}
              icon={
                destinationIcon
              }
            >

              <Popup>

                <strong>
                  🏁 Destination
                </strong>

                <br />

                Latitude:{" "}
                {
                  destination[0]
                    .toFixed(5)
                }

                <br />

                Longitude:{" "}
                {
                  destination[1]
                    .toFixed(5)
                }

              </Popup>

            </Marker>

          )}


          {/* ========================================
              VISIBLE GEOFENCE
          ======================================== */}

          {geofenceCenter && (

            <Circle
              center={
                geofenceCenter
              }
              radius={
                geofenceRadius
              }
              pathOptions={{
                color: "#ef4444",
                fillColor:
                  "#ef4444",
                fillOpacity: 0.18,
                weight: 3,
                dashArray: "8 6",
              }}
            >

              <Popup>

                <strong>
                  ⚠ ChainTwin Geofence
                </strong>

                <br />

                Radius:{" "}

                {
                  geofenceRadius
                } meters

                <br />

                Monitored disruption zone

              </Popup>

            </Circle>

          )}


          {/* ========================================
              VEHICLE
          ======================================== */}

          {pickup && (

            <Marker
              position={
                truckPosition
              }
              icon={truckIcon}
            >

              <Popup>

                <strong>
                  🚚 SHP-001
                </strong>

                <br />

                Status: {status}

                <br />

                Progress:{" "}
                {progress}%

                <br />

                {
                  insideGeofence
                    ? "⚠ Inside disruption geofence"
                    : "Safe"
                }

              </Popup>

            </Marker>

          )}

        </MapContainer>

      </div>


      {/* ============================================
          GEOFENCE CONTROL
      ============================================ */}

      <div
        style={{
          marginTop: "14px",
          padding: "14px",
          background:
            "rgba(15,23,42,.75)",
          borderRadius: "10px",
        }}
      >

        <strong>
          Geofence Radius:{" "}
          {geofenceRadius} meters
        </strong>


        <input
          type="range"
          min="200"
          max="3000"
          step="100"
          value={
            geofenceRadius
          }
          onChange={(event) =>
            setGeofenceRadius(
              Number(
                event.target.value
              )
            )
          }
          style={{
            width: "100%",
            marginTop: "10px",
          }}
        />

      </div>

    </div>
  );
}


export default LiveMap;