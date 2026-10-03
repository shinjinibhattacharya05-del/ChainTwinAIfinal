import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .data_service import get_shipments, get_shipment
from .loss_engine import calculate_factory_loss, next_week_projection
from .recommendation_engine import generate_recommendations
from .optimization_engine import optimize_route
from .simulation_engine import run_what_if, rewind_disruption
from .agent_engine import ask_agent


# =========================================================
# ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# APPLICATION LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("ChainTwin AI backend started.")
    yield
    print("ChainTwin AI backend stopped.")


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="ChainTwin AI API",
    description="Supply Chain Risk & Decision Twin Backend",
    version="1.0.0",
    lifespan=lifespan,
)


# =========================================================
# CORS
# =========================================================
# During development Vite may use 5173, 5174, etc.
# This regex allows localhost/127.0.0.1 Vite ports.
#
# For production we will restrict this to the deployed
# frontend domain.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST MODELS
# =========================================================

class WhatIfRequest(BaseModel):
    disruption_type: str
    severity: int
    duration_hours: float


class AgentRequest(BaseModel):
    message: str


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "name": "ChainTwin AI",
        "status": "online",
        "version": "1.0.0",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ChainTwin AI Backend",
    }


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/api/dashboard")
def dashboard():
    return {
        "financial_exposure": 482000,
        "network_risk": 78,
        "active_shipments": 18,
        "factory_efficiency": 71,

        "active_disruption": {
            "name": "NH-16 Flood",
            "severity": "High",
            "current_exposure": 184000,
            "optimized_exposure": 71000,
            "potential_loss_avoided": 113000,
        },
    }


# =========================================================
# SHIPMENTS
# =========================================================

@app.get("/api/shipments")
def shipments():
    return get_shipments()


@app.get("/api/shipments/{shipment_id}")
def shipment(shipment_id: str):

    result = get_shipment(shipment_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    return result


# =========================================================
# FACTORY INTELLIGENCE
# =========================================================

@app.get("/api/factories/loss-analysis")
def factory_loss():
    return calculate_factory_loss()


@app.get("/api/factories/next-week")
def factory_next_week():
    return next_week_projection()


# =========================================================
# RECOMMENDATIONS
# =========================================================

@app.get("/api/recommendations")
def recommendations():
    return generate_recommendations()


# =========================================================
# ROUTE OPTIMIZATION
# =========================================================

@app.get("/api/optimize-route/{shipment_id}")
def route_optimization(shipment_id: str):

    shipment_data = get_shipment(shipment_id)

    if shipment_data is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    return optimize_route(shipment_id)


# =========================================================
# WHAT-IF SIMULATOR
# =========================================================

@app.post("/api/what-if")
def what_if(request: WhatIfRequest):

    return run_what_if(
        request.disruption_type,
        request.severity,
        request.duration_hours,
    )


# =========================================================
# REWIND ENGINE
# =========================================================

@app.get("/api/rewind")
def rewind():
    return rewind_disruption()


# =========================================================
# CHAINTWIN AGENT
# =========================================================

@app.post("/api/agent")
def agent(request: AgentRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty",
        )

    return ask_agent(request.message)


# =========================================================
# LIVE GPS WEBSOCKET
# =========================================================

@app.websocket("/ws/gps/{shipment_id}")
async def gps_stream(
    websocket: WebSocket,
    shipment_id: str,
):

    await websocket.accept()

    route = [
        (22.5726, 88.3639),
        (22.4500, 88.1000),
        (22.2500, 87.7500),
        (22.0500, 87.4000),
        (21.8500, 87.0500),
        (21.6500, 86.7500),
        (21.3500, 86.3500),
        (20.9500, 85.9500),
        (20.6000, 85.8500),
        (20.2961, 85.8245),
    ]

    try:

        index = 0

        while True:

            lat, lng = route[index]

            progress = round(
                ((index + 1) / len(route)) * 100,
                1,
            )

            await websocket.send_json(
                {
                    "shipment_id": shipment_id,
                    "lat": lat,
                    "lng": lng,
                    "speed_kmph": 48,
                    "status": "IN_TRANSIT",
                    "route_progress": progress,
                }
            )

            index = (index + 1) % len(route)

            await asyncio.sleep(2)

    except WebSocketDisconnect:

        print(
            f"GPS client disconnected: {shipment_id}"
        )