# Hostile foundations review errata (26 Nov 2026): Crossref check of every DOI cited in theory/RECORD_COST_ERRATA_2026-11-26.md. Output: doi_check_7f.out
import json, urllib.request, urllib.error, time
dois = ["10.1088/1367-2630/16/12/123029","10.1088/1367-2630/17/12/123001","10.1090/S0002-9904-1946-08506-7"]
def fetch(d, tries=4):
    for k in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d, headers={"User-Agent":"gtao-rnd (mailto:none@example.com)"}), timeout=30))["message"]
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == tries - 1: raise
            time.sleep(5 * (k + 1))  # rate limit: wait and retry
for d in dois:
    try:
        r = fetch(d)
        au = "; ".join(a.get("family","?") for a in r.get("author",[]))
        print("OK", d, "|", r["issued"]["date-parts"][0][0], "|", (r.get("title") or ["?"])[0], "|", au, "|", (r.get("container-title") or ["?"])[0], r.get("volume",""), r.get("page", r.get("article-number","")))
    except Exception as e:
        print("FAIL", d, e)
    time.sleep(0.4)
