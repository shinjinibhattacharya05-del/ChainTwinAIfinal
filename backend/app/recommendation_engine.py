def generate_recommendations():
    return [
        {
            "id": 1,
            "priority": "CRITICAL",
            "title": "Increase Material-X safety stock",
            "description": (
                "Increase inventory coverage from 1.2 to "
                "1.8 days to reduce production interruption risk."
            ),
            "confidence": 92,
            "expected_saving": 126000,
            "before": "68% shortage risk",
            "after": "14% shortage risk",
            "action": "Increase safety stock",
        },
        {
            "id": 2,
            "priority": "HIGH",
            "title": "Advance Supplier S-14 delivery",
            "description": (
                "Move the next delivery forward by 6 hours "
                "because current inventory may reach the safety threshold."
            ),
            "confidence": 88,
            "expected_saving": 84000,
            "before": "6.2h expected delay",
            "after": "1.1h expected delay",
            "action": "Advance delivery",
        },
        {
            "id": 3,
            "priority": "MEDIUM",
            "title": "Schedule Line-3 preventive maintenance",
            "description": (
                "Use the predicted low-demand window for "
                "maintenance instead of waiting for failure."
            ),
            "confidence": 81,
            "expected_saving": 61000,
            "before": "High downtime exposure",
            "after": "74% lower downtime risk",
            "action": "Schedule maintenance",
        },
    ]