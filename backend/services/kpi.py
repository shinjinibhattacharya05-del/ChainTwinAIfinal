
from backend.state import ss
from backend.services.tracking import statuses

def kpis():
    hz = ss.hz; down = statuses(hz)["A"] == "disrupted"
    exp = (50 if down else 0) + 4 * sum(h["type"] != "flood" for h in hz); dly = 10 if down else (2 if hz else 0)
    if ss.mit: exp, dly = min(exp, 5), min(dly, 3)
    return dict(
        risk=dict(v="MITIGATED" if ss.mit else "HIGH" if down else "ELEVATED" if hz else "LOW", good=bool(ss.mit or not hz)),
        inventory=dict(v="5 DAYS" if down and not ss.mit else "14 DAYS" if not down else "9 DAYS", good=not (down and not ss.mit)),
        delay=dict(v=f"{dly} DAYS", good=dly <= 3), exposure=dict(v=f"₹{exp},00,000", good=bool(ss.mit or not exp)), mitigated=bool(ss.mit))