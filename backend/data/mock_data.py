CITIES = {"CHE": ("Chennai", 13.0827, 80.2707), "BLR": ("Bangalore", 12.9716, 77.5946), "HYD": ("Hyderabad", 17.385, 78.4867),
 "PUN": ("Pune", 18.5204, 73.8567), "MUM": ("Mumbai", 19.076, 72.8777), "CBE": ("Coimbatore", 11.0168, 76.9558),
 "KNL": ("Kurnool", 15.8281, 78.0373), "HUB": ("Hubballi", 15.3647, 75.124), "BEL": ("Belagavi", 15.8497, 74.4977),
 "SOL": ("Solapur", 17.6599, 75.9064), "VJA": ("Vijayawada", 16.5062, 80.648), "NLR": ("Nellore", 14.4426, 79.9865),
 "ATP": ("Anantapur", 14.6819, 77.6006), "KOL": ("Kolhapur", 16.705, 74.2433)}
ROADS = [("CHE","NLR"),("NLR","VJA"),("VJA","HYD"),("CHE","BLR"),("CHE","CBE"),("CBE","BLR"),("BLR","ATP"),("ATP","KNL"),
 ("KNL","HYD"),("NLR","ATP"),("HYD","SOL"),("SOL","PUN"),("PUN","KOL"),("KOL","BEL"),("BEL","HUB"),("HUB","BLR"),
 ("SOL","HUB"),("PUN","MUM"),("KNL","HUB")]
SUP = {"A": ("Supplier A", "CHE"), "B": ("Supplier B", "PUN"), "C": ("Supplier C", "HYD"), "D": ("Supplier D", "CBE")}
BASE = {"A": dict(Cost=88, Capacity=85, Reliability=90, Quality=90), "B": dict(Cost=90, Capacity=91, Reliability=94, Quality=93),
        "C": dict(Cost=82, Capacity=80, Reliability=86, Quality=85), "D": dict(Cost=70, Capacity=74, Reliability=78, Quality=77)}
DOCS = [
 ("Supplier B capacity report", "2025-03-28", "Supplier B Pune semiconductor capacity 120000 units per month with 40 percent headroom, can ship 50000 units within 5 days."),
 ("Supplier B delivery performance", "2025-04-02", "Supplier B on-time delivery 96.4 percent over 24 months, reliable, quality defect rate 0.21 PPM ISO 9001."),
 ("Supplier B emergency contract", "2024-11-09", "Contract clause lets Supplier B allocate up to 60000 units at plus 6 percent price during supplier disruption emergencies."),
 ("Supplier C capacity and delivery", "2025-03-15", "Supplier C Hyderabad capacity 30000 units per month, on-time delivery 85 percent, would need split shipments for 50000 units."),
 ("Supplier D quality report", "2025-01-20", "Supplier D Coimbatore small capacity 20000 units, higher unit cost, quality acceptable, longer lead time."),
 ("Chennai flood playbook", "2023-12-10", "Chennai floods in 2015 and 2023 caused 9 to 12 day outages at Supplier A Chennai; roads and ports near Chennai flooded, recovery slow."),
 ("Western Ghat route advisory", "2025-04-20", "Kolhapur to Belagavi ghat road on NH48 is prone to landslides and blockages; alternate via Solapur and Hubballi adds about 110 km."),
 ("Hubballi hub fire advisory", "2025-03-30", "Fire near Hubballi logistics hub causes road closures and delays of 6 to 10 hours; avoid hub, prefer Hyderabad Kurnool corridor."),
 ("NH44 Anantapur road works", "2025-04-18", "Road blockage at Anantapur on NH44 stops freight between Bangalore and Kurnool; use Hubballi route or wait for clearance."),
 ("Inventory and SLA policy", "2025-01-05", "Critical inventory threshold is 7 days. Customer Z Mumbai SLA penalty is 1 lakh rupees per day after 4 days of delay."),
 ("Satellite detection SOP", "2025-02-02", "Sentinel-2 change detection with confidence above 85 percent triggers automatic reroute review and supplier re-ranking.")]
EVENTS = {"🌊 Flood · Chennai (Supplier A)": ("flood", "CHE", None, 40, 11), "⛰️ Landslide · Kolhapur–Belagavi ghat": ("landslide", "KOL", "BEL", 25, 12),
          "🔥 Fire · Hubballi logistics hub": ("fire", "HUB", None, 18, 13), "🚧 Road blockage · Anantapur (NH44)": ("road_block", "ATP", None, 10, 14)}
HZ = {"flood": dict(m=2.5, blk=False, c="#4aa3ff", ic="🌊"), "fire": dict(m=3.0, blk=False, c="#ff7a1a", ic="🔥"),
      "landslide": dict(m=1, blk=True, c="#e0b020", ic="⛰️"), "road_block": dict(m=1, blk=True, c="#ff5a5f", ic="🚧")}
PIPE = ["Detect Event", "Query Graph", "Assess Risk", "Retrieve (RAG)", "Simulate", "Optimize", "Explain (LLM)", "Recommend"]
