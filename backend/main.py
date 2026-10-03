from typing import Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel
from backend.state import ss
from backend.data.mock_data import CITIES, SUP, DOCS, EVENTS, HZ, PIPE
from backend.services.geo import alternatives, pc, label, PROFILES
from backend.services.satellite import run_scan, detect, to_b64, from_b64
from backend.services.rag import retriever
from backend.services.llm import ask_llm
from backend.services.suppliers import sup_scores, situation
from backend.services.kpi import kpis
from backend.services import tracking as T

app = FastAPI(title="ChainTwin AI API", version="2.0")
T.reset_state()

class ScanReq(BaseModel): events: list[str]
class PrioReq(BaseModel): w: list[float]; auto: bool = True
class AssignReq(BaseModel): path: list[str]
class RankReq(BaseModel): weights: dict[str, int]
class AskReq(BaseModel): question: str; retrieval_query: Optional[str] = None; k: int = 4
class UploadReq(BaseModel): before: str; after: str; city: str; radius: int = 25; apply: bool = False

def best_of(alts): return min(alts, key=lambda a: pc(a["path"], ss.hz, ss.w)) if alts else None
def ships_view():
    h = T.sim_h(); out = []
    for s in ss.ships:
        c = T.cum(s["wps"]); d = T.cur_d(s, h); rem = max(0, c[-1] - d); eta = None if s["hold"] else rem / s["spd"]
        la, lo = T.pos_at(s["wps"], d)
        out.append(dict(id=s["id"], supplier=s["sup"], hold=s["hold"], note=s["note"], lat=la, lon=lo, delivered=rem < 1,
            route=[x[0] for x in s["wps"] if x[0] != "cur"], line=[[x[1], x[2]] for x in s["wps"]], progress=round(100 * d / c[-1]) if c[-1] else 100,
            remaining_km=round(rem), eta_h=None if eta is None else round(eta, 1), delay_h=None if eta is None else round(h + eta - s["plan"], 1)))
    return out

@app.get("/api/meta")
def meta(): return dict(cities={k: dict(name=v[0], lat=v[1], lon=v[2]) for k, v in CITIES.items()}, suppliers={k: dict(name=n, city=c) for k, (n, c) in SUP.items()},
    nodes={k: dict(name=v[0], city=v[1], offset=v[2]) for k, v in T.NODEPOS.items()}, events=list(EVENTS), hazard_styles=HZ, pipeline=PIPE, colors=T.COL, docs=DOCS)

@app.get("/api/state")
def state():
    alts = alternatives("PUN", "BLR", ss.hz, ss.w); rk = sorted(sup_scores(ss.hz, ss.w).items(), key=lambda x: -x[1]["score"])
    return dict(hazards=ss.hz, statuses=T.statuses(ss.hz), kpis=kpis(), w=list(ss.w), auto=ss.auto, mitigated=ss.mit, log=ss.log[:25],
        routes=alts, best=best_of(alts), ranking=[dict(id=k, **v) for k, v in rk], zones=[dict(zone=z["zone"], det=z["det"], lat=z["lat"], lon=z["lon"]) for z in ss.scan])

@app.get("/api/ships")
def ships(): return dict(ships=ships_view(), log=ss.log[:12], hazards=ss.hz, statuses=T.statuses(ss.hz))

@app.post("/api/scan")
def scan(r: ScanReq):
    ss.scan = run_scan(r.events); ss.hz = [dict(type=z["det"]["type"], lat=z["lat"], lon=z["lon"], r=z["r"], conf=z["det"]["conf"], name=z["name"]) for z in ss.scan if z["det"]]
    for h in ss.hz: T.log(f"DETECTED {h['type']} @ {h['name']} ({h['conf']:.0%})")
    n = T.respond(True) if ss.auto else 0; ss.mit = bool(ss.hz) and ss.auto and n > 0
    return dict(changes=n, hazards=ss.hz, zones=[dict(zone=z["zone"], det=z["det"]) for z in ss.scan])

@app.get("/api/scan/images")
def scan_images(): return [dict(zone=z["zone"], det=z["det"], lat=z["lat"], lon=z["lon"], before=to_b64(z["b"]), after=to_b64(z["a"]),
    mask=to_b64((z["m"][..., None] * __import__("numpy").array([255, 60, 60])).astype("uint8"))) for z in ss.scan]

@app.post("/api/scan/upload")
def upload(r: UploadReq):
    det, _ = detect(from_b64(r.before), from_b64(r.after))
    if det and r.apply:
        c = CITIES[r.city]; ss.hz.append(dict(type=det["type"], lat=c[1], lon=c[2], r=r.radius, conf=det["conf"], name=c[0])); T.respond(True)
    return dict(detection=det)

@app.post("/api/hazards/clear")
def clear(): ss.hz = []; ss.mit = False; T.respond(True); T.log("Hazards cleared – routes re-optimised"); return {"ok": True}

@app.post("/api/priorities")
def priorities(r: PrioReq):
    ss.auto = r.auto; changed = tuple(r.w) != ss.w
    if changed: ss.w = tuple(r.w); T.log(f"Priorities changed to speed={r.w[0]}, cost={r.w[1]}, safety={r.w[2]}")
    return dict(changes=T.respond(True) if (changed and ss.auto) else 0)

@app.post("/api/respond")
def respond(): n = T.respond(True); ss.mit = bool(ss.hz); return dict(changes=n)

@app.post("/api/fast-forward")
def ff(hours: float = 6): ss.t_start -= hours * 20; return {"ok": True}

@app.post("/api/reset")
def reset(): T.reset_state(); return {"ok": True}

@app.get("/api/routes")
def routes(origin: str, dest: str):
    alts = alternatives(origin, dest, ss.hz, ss.w); return dict(routes=alts, best=best_of(alts))

@app.post("/api/ships/{sid}/assign")
def assign(sid: str, r: AssignReq):
    s = next(x for x in ss.ships if x["id"] == sid); h = T.sim_h(); p = T.pos_at(s["wps"], T.cur_d(s, h))
    s["wps"] = [("cur", *p)] + T.wp_list(r.path); s["d0"] = 0.0; s["t0"] = h; s["note"] = "Rerouted (manual)"; T.log(f"{sid} manually assigned {label(r.path)}"); return {"ok": True}

@app.post("/api/suppliers/rank")
def rank(r: RankReq):
    ss.wts.update(r.weights); rk = sorted(sup_scores(ss.hz, ss.w).items(), key=lambda x: -x[1]["score"])
    return [dict(id=k, name=SUP[k][0], city=CITIES[SUP[k][1]][0], status=T.statuses(ss.hz)[k], **v) for k, v in rk]

@app.post("/api/copilot")
def copilot(r: AskReq, x_anthropic_key: Optional[str] = Header(None)):
    ht, rk, alts = situation(); docs = retriever().search((r.retrieval_query or r.question) + " " + ht, r.k)
    ans, src = ask_llm(r.question, docs, ht, rk, alts, key=x_anthropic_key)
    return dict(answer=ans, source=src, error=None if ans else src, evidence=[dict(title=d[0], date=d[1], text=d[2], score=round(min(.99, s), 2)) for s, d in docs])

@app.get("/api/health")
def health(): return dict(status="ok")
