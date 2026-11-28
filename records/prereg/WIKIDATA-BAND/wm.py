"""Polite Wikimedia API client (read-only). UA identifies the project; serial requests; maxlag; retries; on-disk cache."""
import requests, time, json, hashlib, os
UA = "GTAO-research/0.1 (private read-only research; contact via github.com/Chad-Mitchell)"
S = requests.Session(); S.headers.update({"User-Agent": UA, "Accept-Encoding": "gzip"})
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "cache")
os.makedirs(CACHE, exist_ok=True)
_last = [0.0]
MIN_GAP = float(os.environ.get("WM_GAP", "0.25"))
def _key(url, params):
    return hashlib.sha256((url + json.dumps(params, sort_keys=True)).encode()).hexdigest()
def get(url, params=None, cache=True, tries=6):
    params = dict(params or {})
    k = _key(url, params); p = os.path.join(CACHE, k[:2], k + ".json")
    if cache and os.path.exists(p):
        with open(p) as f: return json.load(f)
    for i in range(tries):
        gap = time.time() - _last[0]
        g = 3.0 if "www.wikidata.org/w/api.php" in url else (1.5 if "/w/api.php" in url else MIN_GAP)
        if gap < g: time.sleep(g - gap)
        _last[0] = time.time()
        try:
            r = S.get(url, params=params, timeout=90)
        except Exception as e:
            print("exc", repr(e)[:120], flush=True); time.sleep(2 ** i); continue
        if r.status_code == 404:
            out = {"__status": 404}; break
        if r.status_code in (429, 500, 502, 503, 504):
            print("http", r.status_code, url[:60], r.headers.get("Retry-After"), json.dumps(params)[:150], flush=True)
            ra = r.headers.get("Retry-After"); time.sleep(float(ra) if ra and ra.isdigit() else 2 ** (i + 1)); continue
        r.raise_for_status()
        out = r.json()
        if isinstance(out, dict) and out.get("error", {}).get("code") == "maxlag":
            print("maxlag", out["error"].get("lag"), flush=True); time.sleep(5 * (i + 1)); continue
        break
    else:
        raise RuntimeError("failed " + url + json.dumps(params)[:200])
    if cache:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f: json.dump(out, f)
    return out
def api(host, **params):
    params.setdefault("format", "json"); params.setdefault("formatversion", "2")
    if "wikidata" in host: params.setdefault("maxlag", "5")
    return get(f"https://{host}/w/api.php", params)
def sparql(q):
    return get("https://query.wikidata.org/sparql", {"query": q, "format": "json"})

def raw(url, tries=8):
    for i in range(tries):
        gap = time.time() - _last[0]
        if gap < 2.5: time.sleep(2.5 - gap)
        _last[0] = time.time()
        try: r = S.get(url, timeout=90)
        except Exception as e:
            print("exc", repr(e)[:120], flush=True); time.sleep(2 ** i); continue
        if r.status_code == 404: return None
        if r.status_code in (429, 500, 502, 503, 504):
            ra = r.headers.get("Retry-After"); print("http", r.status_code, url[:80], ra, flush=True)
            time.sleep(float(ra) if ra and ra.isdigit() else 2 ** (i + 1)); continue
        r.raise_for_status(); return r.text
    return None
