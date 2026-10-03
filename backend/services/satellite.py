import io, base64
import numpy as np
from PIL import Image
from backend.data.mock_data import CITIES, EVENTS
def scene(kind, seed, n=48):
    g = np.random.default_rng(seed); yy, xx = np.mgrid[:n, :n]
    b = np.array([70, 110, 60.]) + g.normal(0, 6, (n, n, 3)); b[g.random((n, n)) < .15] = [110, 95, 70]; b[n//2-1:n//2+2, :] = [105, 105, 105]
    a = b + g.normal(0, 3, (n, n, 3))
    if kind:
        cx, cy = g.integers(16, 32, 2); rr = np.hypot(xx-cx, yy-cy) + g.normal(0, 1.5, (n, n))
        if kind == "flood": a[rr < 12] = [40, 90, 170]
        elif kind == "fire": a[rr < 12] = [40, 30, 30]; a[rr < 7] = [230, 90, 30]
        elif kind == "landslide": a[np.abs(xx-yy-(cx-cy)) < 5] = [150, 135, 120]
        else: a[n//2-2:n//2+3, 16:30] = [150, 70, 40]
    return np.clip(b, 0, 255).astype(np.uint8), np.clip(a, 0, 255).astype(np.uint8)
def detect(before, after, thr=70):
    """Pixel change detection + spectral classification. Works on any two same-size RGB arrays."""
    d = np.abs(after.astype(int) - before.astype(int)).sum(2); m = d > thr; frac = m.mean()
    if frac < .01: return None, m
    p = after[m].astype(int); r, g, b = p[:, 0], p[:, 1], p[:, 2]
    sh = {"flood": np.mean(b > r+60), "fire": np.mean((r > g+100) | (p.sum(1) < 140)),
          "road_block": np.mean((r-g > 50) & (r-g < 110) & (b < 80)), "landslide": np.mean((abs(r-g) < 40) & (r > 100) & (b > 80))}
    k = max(sh, key=sh.get)
    return dict(type=k, conf=min(.99, .62 + .3*sh[k] + min(frac, .25)), area=round(frac*100, 1)), m
def run_scan(selected):
    res = []
    for lab, (ty, c1, c2, r, seed) in EVENTS.items():
        on = lab in selected; b, a = scene(ty if on else None, seed); det, m = detect(b, a)
        lat, lon = (CITIES[c1][1], CITIES[c1][2]) if not c2 else ((CITIES[c1][1]+CITIES[c2][1])/2, (CITIES[c1][2]+CITIES[c2][2])/2)
        res.append(dict(zone=lab.split("· ")[1], name=lab.split("· ")[1], b=b, a=a, m=m, det=det, lat=lat, lon=lon, r=r))
    b, a = scene(None, 99); det, m = detect(b, a)
    res.append(dict(zone="Coimbatore (control zone)", name="Coimbatore", b=b, a=a, m=m, det=det, lat=11.0168, lon=76.9558, r=0))
    return res
def to_b64(a, size=220):
    buf = io.BytesIO(); Image.fromarray(a).resize((size, size), Image.NEAREST).save(buf, "PNG"); return base64.b64encode(buf.getvalue()).decode()
def from_b64(s, n=96): return np.array(Image.open(io.BytesIO(base64.b64decode(s))).convert("RGB").resize((n, n)))