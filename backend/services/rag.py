import re, math
from collections import Counter
from functools import lru_cache
from backend.data.mock_data import DOCS
def tok(s): return re.findall(r"[a-z0-9]+", s.lower())
class Retriever:
    def __init__(s, docs):
        s.docs = docs; s.tf = [Counter(tok(t+" "+x)) for t, _, x in docs]; df = Counter(w for t in s.tf for w in t)
        s.idf = {w: math.log((1+len(docs))/(1+c))+1 for w, c in df.items()}
    def v(s, c): v = {w: n*s.idf.get(w, 0) for w, n in c.items()}; return v, math.sqrt(sum(x*x for x in v.values())) or 1
    def search(s, q, k=4):
        qv, qn = s.v(Counter(tok(q))); out = []
        for d, t in zip(s.docs, s.tf):
            dv, dn = s.v(t); out.append((sum(x*dv.get(w, 0) for w, x in qv.items())/(qn*dn), d))
        return sorted(out, key=lambda x: -x[0])[:k]
@lru_cache(None)
def retriever(): return Retriever(DOCS)
