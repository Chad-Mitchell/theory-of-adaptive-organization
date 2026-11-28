import requests, json, time, random
from concurrent.futures import ThreadPoolExecutor
UA = {"User-Agent": "gtao-drift-research/0.1 (research script; research@example.invalid)"}
API = "https://en.wikipedia.org/w/api.php"
S = requests.Session(); S.headers.update(UA)
def get(params):
    for k in range(6):
        try:
            r = S.get(API, params={**params, "format": "json", "maxlag": 5}, timeout=30)
            j = r.json()
            if "error" in j and j["error"].get("code") == "maxlag":
                time.sleep(5); continue
            return j
        except Exception:
            time.sleep(2 * (k + 1))
    return None
titles = []
while len(titles) < 3000:
    j = get({"action": "query", "list": "random", "rnnamespace": 0, "rnfilterredir": "nonredirects", "rnlimit": 500})
    titles += [p["title"] for p in j["query"]["random"]]
titles = list(dict.fromkeys(titles))[:3000]
def revs(t):
    ts = []; cont = {}
    for _ in range(10):
        j = get({"action": "query", "prop": "revisions", "titles": t, "rvprop": "timestamp", "rvlimit": "max", **cont})
        if not j: break
        for p in j.get("query", {}).get("pages", {}).values():
            ts += [r["timestamp"] for r in p.get("revisions", [])]
        if "continue" in j: cont = j["continue"]
        else: break
    return {"title": t, "ts": ts, "capped": "continue" in (j or {}), "pulled": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
with open("data/wiki_revs.jsonl", "w") as f, ThreadPoolExecutor(3) as ex:
    for i, r in enumerate(ex.map(revs, titles)):
        f.write(json.dumps(r) + "\n")
        if i % 250 == 0: print(i, flush=True)
print("done")
