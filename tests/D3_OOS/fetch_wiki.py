"""Fetch revision timestamps (+user) for the first 40 mainspace pages (by sortkey) of each category in categories.txt,
public MediaWiki API, newest first, cap 20 x 500 revisions per page. Output: wiki_revs.jsonl (scratch path arg)."""
import json, sys, time, urllib.request, urllib.parse
OUT = sys.argv[1]; API = "https://en.wikipedia.org/w/api.php"; UA = {"User-Agent": "GTAO-research-script/0.1 (private research; low rate)"}
def get(params):
    params = {**params, "format": "json", "formatversion": "2"}
    for k in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 + 3*k)
    raise RuntimeError("API fail")
with open(OUT, "w") as f:
    for cat in [l.strip() for l in open("categories.txt") if l.strip()]:
        cm = get({"action": "query", "list": "categorymembers", "cmtitle": cat, "cmtype": "page", "cmnamespace": 0, "cmlimit": 40, "cmsort": "sortkey"})
        for p in cm["query"]["categorymembers"]:
            revs = []; cont = {}; capped = False
            for page in range(20):
                q = get({"action": "query", "prop": "revisions", "titles": p["title"], "rvprop": "timestamp|user", "rvlimit": 500, **cont})
                revs += [(r["timestamp"], r.get("user", "")) for r in q["query"]["pages"][0].get("revisions", [])]
                if "continue" not in q: break
                cont = q["continue"]; time.sleep(0.2)
            else:
                capped = True
            f.write(json.dumps({"category": cat, "title": p["title"], "capped": capped, "revs": revs}) + "\n"); f.flush()
            time.sleep(0.2)
