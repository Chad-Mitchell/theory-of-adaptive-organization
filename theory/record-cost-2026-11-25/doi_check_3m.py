# Round 10b-M (inflow/composition/cost worker): Crossref check of every DOI cited. Output: doi_check_3m.out
import json, urllib.request, urllib.error, time
dois = ["10.1088/1367-2630/13/6/063001","10.1103/PhysRevLett.104.080402","10.1088/1751-8113/47/32/325303",
"10.1088/1367-2630/17/12/123001","10.1007/s10701-014-9777-1","10.1103/PhysRevLett.109.090403",
"10.1073/pnas.1304884110","10.1038/s41534-018-0123-x","10.1103/PhysRevLett.51.1127","10.1103/PhysRevLett.99.100602",
"10.1103/PhysRevA.70.052328","10.1147/rd.53.0183","10.1103/PhysRevA.84.012311","10.1088/1367-2630/12/3/033024",
"10.1103/PhysRevA.89.052124","10.1103/PhysRevA.81.062348","10.1088/1367-2630/12/3/033023"]
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
