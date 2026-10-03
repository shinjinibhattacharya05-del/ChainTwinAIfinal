
from backend.state import ss
from backend.data.mock_data import SUP, BASE
from backend.services.geo import route, stats, alternatives
from backend.services.tracking import statuses
def sup_scores(hz, w):
    sts = statuses(hz); wt = ss.wts; out = {}
    for k, (n, c) in SUP.items():
        p = route(c, "BLR", hz, w)
        if not p: out[k] = dict(score=0, f={}, hrs=None, path=[]); continue
        s = stats(p, hz); f = dict(BASE[k]); f["Delivery"] = max(15, 100 - max(0, s["hrs"]-6)*3)
        f["Risk"] = max(5, 100 - s["risk"] - (60 if sts[k] == "disrupted" else 0))
        out[k] = dict(score=round(sum(f[c_]*wt[c_] for c_ in f)/sum(wt.values()), 1), f=f, hrs=s["hrs"], path=p)
    return out
def situation():
    hz = ss.hz; sc = sup_scores(hz, ss.w); alts = alternatives("PUN", "BLR", hz, ss.w)
    ht = "; ".join(f"{h['type']} near {h['name']} ({h['conf']:.0%})" for h in hz) or "no active hazards"
    rk = sorted(sc.items(), key=lambda x: -x[1]["score"])
    return ht, rk, alts