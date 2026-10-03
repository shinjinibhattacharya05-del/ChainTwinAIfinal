
import time, math
from backend.state import ss
from backend.data.mock_data import CITIES, SUP
from backend.services.geo import hav, route, fx, hkey, pc, stats, label
def sim_h(): return (time.time() - ss.t_start) * 0.05   # 1 real second = 3 simulated minutes
def log(m): ss.log.insert(0, f"{time.strftime('%H:%M:%S')}  {m}")
def wp_list(p): return [(c, CITIES[c][1], CITIES[c][2]) for c in p]
def cum(w):
    c = [0.0]
    for a, b in zip(w, w[1:]): c.append(c[-1] + hav(a[1], a[2], b[1], b[2])*1.22)
    return c
def cur_d(s, h): return s["d0"] if s["hold"] else min(cum(s["wps"])[-1], s["d0"] + s["spd"]*(h - s["t0"]))
def pos_at(w, d):
    c = cum(w)
    for i in range(len(w)-1):
        if d <= c[i+1] or i == len(w)-2:
            f = 0 if c[i+1] == c[i] else min(1, max(0, (d-c[i])/(c[i+1]-c[i])))
            return w[i][1] + (w[i+1][1]-w[i][1])*f, w[i][2] + (w[i+1][2]-w[i][2])*f
def rebase(s, h): s["d0"] = cur_d(s, h); s["t0"] = h
def new_ship(i, sup, src, qty, spd):
    p = route(src, "BLR", [], (1, .1, .1)); w = wp_list(p); h = sim_h()
    return dict(id=i, sup=sup, src=src, wps=w, d0=0.0, t0=h, spd=spd, qty=qty, hold=False, plan=h + cum(w)[-1]/spd, note="On plan")
def reset_state():
    ss.t_start = time.time(); ss.hz = []; ss.log = []; ss.mit = False; ss.scan = []; ss.chat = []; ss.auto = True
    ss.w = (1.0, .3, .5); ss.wts = dict(Cost=5, Delivery=5, Capacity=5, Reliability=5, Risk=5, Quality=5);
    ss.ships = [new_ship("SH-B", "Supplier B", "PUN", 50000, 55), new_ship("SH-C", "Supplier C", "HYD", 30000, 50), new_ship("SH-A", "Supplier A", "CHE", 40000, 50)]
def respond(optimize_all=False):
    """Hazard-aware re-planning of every shipment. Logs each change (this feeds the live tracker)."""
    h = sim_h(); hz = ss.hz; hk = hkey(hz); n = 0
    for s in ss.ships:
        c = cum(s["wps"]); d = cur_d(s, h)
        if d >= c[-1]-1: s["note"] = "Delivered"; continue
        c0 = CITIES[s["src"]]; cp = pos_at(s["wps"], d); hit = any(hav(c0[1], c0[2], x["lat"], x["lon"]) <= x["r"] and hav(cp[0], cp[1], x["lat"], x["lon"]) <= x["r"] and x["type"] in ("flood", "fire") for x in hz)
        if hit and not s["hold"]: rebase(s, h); s["hold"] = True; s["note"] = "HELD – origin site disrupted"; log(f"{s['id']} HELD: {s['sup']} site hit by hazard"); n += 1; continue
        if s["hold"]:
            if hit: continue
            rebase(s, h); s["hold"] = False; s["note"] = "Released"; log(f"{s['id']} released – origin clear"); n += 1
        il = max([i for i in range(len(s["wps"])) if c[i] <= d and s["wps"][i][0] != "cur"], default=1 if s["wps"][0][0] == "cur" else 0)
        rest = [x[0] for x in s["wps"][il:] if x[0] != "cur"]
        if len(rest) < 2: continue
        aff = any(fx(u, v, hk) != (1.0, False) for u, v in zip(rest, rest[1:]))
        best = route(rest[0], rest[-1], hz, ss.w)
        if best is None: rebase(s, h); s["hold"] = True; s["note"] = "HELD – no viable route"; log(f"{s['id']} HELD: no viable route"); n += 1; continue
        if best != rest and (aff or pc(best, hz, ss.w) < pc(rest, hz, ss.w) - .3):
            o, nw = stats(rest, hz), stats(best, hz); p = pos_at(s["wps"], d)
            s["wps"] = [("cur", *p)] + wp_list(best); s["d0"] = 0.0; s["t0"] = h
            s["note"] = ("Rerouted (hazard)" if aff else "Better route found")
            log(f"{s['id']} {s['note']}: {label(best)} | {nw['hrs']}h vs {'BLOCKED' if o['blocked'] else str(o['hrs'])+'h'} on old path"); n += 1
    return n
def statuses(hz):
    out = {}
    for k, (_, c) in SUP.items():
        d = min([hav(*CITIES[c][1:], x["lat"], x["lon"]) - x["r"] for x in hz] or [999]); out[k] = "disrupted" if d <= 0 else "at risk" if d < 60 else "healthy"
    down = out["A"] == "disrupted"; sc = lambda c: "disrupted" if any(hav(*CITIES[c][1:], x["lat"], x["lon"]) <= x["r"] for x in hz) else "at risk" if down else "healthy"
    out.update(X=sc("BLR"), Y=sc("HYD") if down else "healthy", Z="at risk" if down else "healthy"); return out
NODEPOS = {"X": ("Factory X", "BLR", 0), "Y": ("Warehouse Y", "HYD", .08), "Z": ("Customer Z", "MUM", 0)}
COL = {"healthy": "#3ddc97", "at risk": "#ffa94d", "disrupted": "#ff5a5f", "alt": "#4cc9f0"}