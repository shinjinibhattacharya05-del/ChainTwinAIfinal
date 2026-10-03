def optimize_route(shipment_id: str):
    routes = [
        {
            "name": "Current Route",
            "distance_km": 462,
            "delay_hours": 6.2,
            "risk_score": 78,
            "estimated_cost": 92000,
        },
        {
            "name": "Alternative Route A",
            "distance_km": 488,
            "delay_hours": 1.4,
            "risk_score": 24,
            "estimated_cost": 68000,
        },
        {
            "name": "Alternative Route B",
            "distance_km": 505,
            "delay_hours": 2.1,
            "risk_score": 31,
            "estimated_cost": 72000,
        },
    ]

    best_route = min(
        routes,
        key=lambda route: (
            route["estimated_cost"]
            + route["risk_score"] * 500
            + route["delay_hours"] * 5000
        ),
    )

    return {
        "shipment_id": shipment_id,
        "recommended_route": best_route,
        "routes": routes,
        "reason": (
            "Selected using combined cost, delay and "
            "operational-risk scoring."
        ),
    }