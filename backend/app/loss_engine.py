def calculate_factory_loss():
    causes = [
        {
            "cause": "Material-X shortage",
            "loss": 184000,
            "percentage": 38,
        },
        {
            "cause": "Production downtime",
            "loss": 126000,
            "percentage": 26,
        },
        {
            "cause": "Supplier delay",
            "loss": 97000,
            "percentage": 20,
        },
        {
            "cause": "Logistics disruption",
            "loss": 75000,
            "percentage": 16,
        },
    ]

    total_loss = sum(item["loss"] for item in causes)

    return {
        "factory": "Plant Alpha",
        "period": "Current Week",
        "total_loss": total_loss,
        "currency": "INR",
        "primary_cause": "Material-X shortage",
        "causes": causes,
    }


def next_week_projection():
    current = calculate_factory_loss()

    projected_without_action = 535000
    projected_with_optimization = 218000

    saving = (
        projected_without_action
        - projected_with_optimization
    )

    return {
        "factory": current["factory"],
        "projected_loss_without_action": projected_without_action,
        "projected_loss_with_optimization": projected_with_optimization,
        "potential_saving": saving,
        "reduction_percentage": round(
            saving / projected_without_action * 100,
            1
        ),
    }