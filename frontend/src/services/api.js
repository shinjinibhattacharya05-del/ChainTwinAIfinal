import axios from "axios";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_URL,

  headers: {
    "Content-Type":
      "application/json",
  },

  timeout: 10000,
});


// ==============================================
// DASHBOARD
// ==============================================

export const getDashboard =
  async () => {
    const response =
      await api.get(
        "/api/dashboard"
      );

    return response.data;
  };


// ==============================================
// SHIPMENTS
// ==============================================

export const getShipments =
  async () => {
    const response =
      await api.get(
        "/api/shipments"
      );

    return response.data;
  };


export const getShipment =
  async (shipmentId) => {
    const response =
      await api.get(
        `/api/shipments/${shipmentId}`
      );

    return response.data;
  };


// ==============================================
// FACTORIES
// ==============================================

export const getFactoryLoss =
  async () => {
    const response =
      await api.get(
        "/api/factories/loss-analysis"
      );

    return response.data;
  };


export const getNextWeekProjection =
  async () => {
    const response =
      await api.get(
        "/api/factories/next-week"
      );

    return response.data;
  };


// ==============================================
// RECOMMENDATIONS
// ==============================================

export const getRecommendations =
  async () => {
    const response =
      await api.get(
        "/api/recommendations"
      );

    return response.data;
  };


// ==============================================
// ROUTE OPTIMIZATION
// ==============================================

export const optimizeRoute =
  async (shipmentId) => {
    const response =
      await api.get(
        `/api/optimize-route/${shipmentId}`
      );

    return response.data;
  };


// ==============================================
// WHAT-IF
// ==============================================

export const runWhatIf =
  async (scenario) => {
    const response =
      await api.post(
        "/api/what-if",
        scenario
      );

    return response.data;
  };


// ==============================================
// REWIND
// ==============================================

export const getRewind =
  async () => {
    const response =
      await api.get(
        "/api/rewind"
      );

    return response.data;
  };


// ==============================================
// AGENT
// ==============================================

export const askAgent =
  async (message) => {
    const response =
      await api.post(
        "/api/agent",
        {
          message,
        }
      );

    return response.data;
  };


// ==============================================
// DYNAMIC ROUTING
// ==============================================

export const createShipmentRoute =
  async (
    shipmentId,
    routeData
  ) => {
    const response =
      await api.post(
        `/api/routes/${shipmentId}`,
        routeData
      );

    return response.data;
  };


// ==============================================
// GPS WEBSOCKET
// ==============================================

export const getGPSWebSocketURL =
  (shipmentId) => {
    const wsURL =
      import.meta.env.VITE_WS_URL ||
      "ws://127.0.0.1:8000";

    return `${wsURL}/ws/gps/${shipmentId}`;
  };


export default api;