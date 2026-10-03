import math, heapq
from functools import lru_cache
import numpy as np
from backend.data.mock_data import CITIES, ROADS, HZ
def hav(la1, lo1, la2, lo2):
    p = math.pi / 180; a = math.sin((la2-la1)*p/2)**2 + math.cos(la1*p)*math.cos(la2*p)*math.sin((lo2-lo1)*p/2)**2
    return 12742 * math.asin(math.sqrt(a))
ADJ = {k: {} for k in CITIES}
for a, b in ROADS:
    km = hav(*CITIES[a][1:], *CITIES[b][1:]) * 1.22; ADJ[a][b] = km; ADJ[b][a] = km
def hkey(hz): return tuple((h["type"], h["lat"], h["lon"], h["r"]) for h in hz)
@lru_cache(None)
def fx(a, b, hk):
    (la1, lo1), (la2, lo2) = CITIES[a][1:], CITIES[b][1:]; m, blk = 1.0, False
    for ty, la, lo, r in hk:
        if any(hav(la1+(la2-la1)*t, lo1+(lo2-lo1)*t, la, lo) <= r for t in np.linspace(0, 1, 15)):
            m = max(m, HZ[ty]["m"]); blk |= HZ[ty]["blk"]
    return m, blk
def ecost(u, v, hk, w):
    m, blk = fx(u, v, hk)
    return None if blk else w[0]*ADJ[u][v]/50*m + w[1]*ADJ[u][v]*.0055 + w[2]*(m-1)*8
def route(src, dst, hz, w):
    hk = hkey(hz); pq = [(0, src, [src])]; seen = set()
    while pq:
        c, u, p = heapq.heappop(pq)
        if u == dst: return p
        if u in seen: continue
        seen.add(u)
        for v in ADJ[u]:
            e = ecost(u, v, hk, w)
            if e is not None and v not in seen: heapq.heappush(pq, (c+e, v, p+[v]))
def pc(p, hz, w):
    hk = hkey(hz); t = 0
    for u, v in zip(p, p[1:]):
        e = ecost(u, v, hk, w)
        if e is None: return math.inf
        t += e
    return t
def stats(p, hz):
    hk = hkey(hz); km = hrs = rk = 0; blk = False
    for u, v in zip(p, p[1:]):
        m, b = fx(u, v, hk); k = ADJ[u][v]; km += k; hrs += k/50*m; rk += (m-1)*20 + k/100; blk |= b
    r = min(100, round(rk*2))
    return dict(km=round(km), hrs=round(hrs, 1), cost_L=round(km*.0055, 2), risk=r, level="Low" if r < 25 else "Medium" if r < 55 else "High", blocked=blk)
PROFILES = {"⚡ Fastest": (1, .1, .1), "💰 Cheapest": (.1, 2, .1), "🛡 Safest": (.3, .1, 2)}
def alternatives(src, dst, hz, w):
    out = {}
    for n, pw in {**PROFILES, "🎯 Your priorities": w}.items():
        p = route(src, dst, hz, pw)
        if p: out.setdefault(tuple(p), []).append(n)
    return [dict(name=" / ".join(n), path=list(p), **stats(list(p), hz)) for p, n in out.items()]
def label(p): return " → ".join(CITIES[c][0] for c in p)
