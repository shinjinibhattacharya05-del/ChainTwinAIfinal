
import os, requests
BASE = os.getenv("CHAINTWIN_API", "http://localhost:8000")
class ApiError(Exception): pass
def _req(method, path, key=None, **kw):
    try:
        r = requests.request(method, BASE + path, headers={"X-Anthropic-Key": key} if key else {}, timeout=60, **kw); r.raise_for_status(); return r.json()
    except requests.RequestException as e: raise ApiError(str(e))
def get(path, **params): return _req("GET", path, params=params)
def post(path, body=None, key=None, **params): return _req("POST", path, key=key, json=body, params=params)