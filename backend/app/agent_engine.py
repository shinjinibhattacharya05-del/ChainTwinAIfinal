from .data_service import get_shipment
from .loss_engine import (
    calculate_factory_loss,
    next_week_projection,
)
from .recommendation_engine import generate_recommendations


def ask_agent(message: str):
    question = message.lower()

    if "loss" in question or "money" in question:
        data = calculate_factory_loss()

        return {
            "answer": (
                f"{data['factory']} currently has an estimated "
                f"weekly loss of ₹{data['total_loss']:,}. "
                f"The largest identified driver is "
                f"{data['primary_cause']}."
            ),
            "data": data,
        }

    if "next week" in question or "optimize" in question:
        data = next_week_projection()

        return {
            "answer": (
                "The current model projects "
                f"₹{data['projected_loss_without_action']:,} "
                "of next-week exposure. Applying the proposed "
                "actions reduces modeled exposure to "
                f"₹{data['projected_loss_with_optimization']:,}, "
                f"a potential saving of ₹{data['potential_saving']:,}."
            ),
            "data": data,
        }

    if "recommend" in question or "action" in question:
        recommendations = generate_recommendations()

        top = recommendations[0]

        return {
            "answer": (
                f"My highest-priority current action is: "
                f"{top['title']}. Modeled saving: "
                f"₹{top['expected_saving']:,} with "
                f"{top['confidence']}% confidence."
            ),
            "data": recommendations,
        }

    if "shipment" in question:
        for shipment_id in [
            "SHP-001",
            "SHP-002",
            "SHP-003",
            "SHP-004",
            "SHP-005",
        ]:
            if shipment_id.lower() in question:
                shipment = get_shipment(shipment_id)

                if shipment:
                    return {
                        "answer": (
                            f"{shipment_id} is currently "
                            f"{shipment['status']} with a "
                            f"{shipment['risk']}% risk score and "
                            f"{shipment['delay_hours']} hours "
                            "of expected delay."
                        ),
                        "data": shipment,
                    }

        return {
            "answer": (
                "Tell me the shipment ID, for example SHP-001, "
                "and I can inspect its current status."
            )
        }

    return {
        "answer": (
            "I can analyze factory losses, shipments, "
            "recommendations and next-week optimization. "
            "Try asking: Why did Plant Alpha lose money?"
        )
    }