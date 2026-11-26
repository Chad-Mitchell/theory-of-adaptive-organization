# QM-selection addendum (26 Nov 2026): Crossref check of the DOIs cited in RESULTS.md (addendum) and DEVIATIONS.md. Output: doi_check.out
import json, urllib.request, urllib.error, time
dois = ["10.2307/1968975","10.1007/BF01378063"]
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
