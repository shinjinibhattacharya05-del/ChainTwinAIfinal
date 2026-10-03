def run_what_if(
    disruption_type: str,
    severity: int,
    duration_hours: float,
):
    severity = max(0, min(severity, 100))
    duration_hours = max(0, duration_hours)

    affected_shipments = max(
        1,
        round((severity / 100) * 12)
    )

    estimated_delay = round(
        duration_hours * (severity / 100) * 0.75,
        1
    )

    financial_exposure = round(
        severity * duration_hours * 1350
    )

    production_risk = min(
        100,
        round(severity * 0.82)
    )

    optimized_exposure = round(
        financial_exposure * 0.42
    )

    potential_saving = (
        financial_exposure - optimized_exposure
    )

    return {
        "scenario": disruption_type,
        "severity": severity,
        "duration_hours": duration_hours,
        "affected_shipments": affected_shipments,
        "estimated_delay_hours": estimated_delay,
        "production_risk": production_risk,
        "financial_exposure": financial_exposure,
        "optimized_exposure": optimized_exposure,
        "potential_saving": potential_saving,
        "recommendation": (
            "Reroute high-value shipments and increase "
            "Material-X safety inventory."
        ),
    }


def rewind_disruption():
    return {
        "event": "NH-16 Flood Disruption",
        "actual_loss": 482000,
        "actual_delay_hours": 8.4,
        "intervention": (
            "Reroute shipment SHP-001 six hours before "
            "the disruption threshold."
        ),
        "counterfactual_loss": 173000,
        "avoidable_loss": 309000,
        "lesson": (
            "Earlier rerouting combined with temporary "
            "safety-stock expansion would have reduced exposure."
        ),
    }