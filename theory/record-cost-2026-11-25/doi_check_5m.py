# Round 12-M (Conjecture C beyond (star)): Crossref check of every DOI cited in section 16 of the round 10 note. Output: doi_check_5m.out
import json, urllib.request, urllib.error, time
dois = ["10.1016/0022-247X(75)90186-9","10.1137/S003614450444614X","10.7146/math.scand.a-10456","10.22331/q-2025-01-20-1599",
"10.1088/1367-2630/17/12/123001"]
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
