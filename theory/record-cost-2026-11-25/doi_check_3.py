# Round 10 sources: Crossref check (prints OK with year, title, authors, venue).
import json, urllib.request, time
dois = ["10.22331/q-2023-11-03-1159","10.1103/PhysRevA.84.012311","10.1088/1367-2630/13/6/063001",
"10.1007/BFb0080769","10.1103/PhysRevA.70.052328","10.2178/bsl/1058448677","10.1103/PhysRevA.81.062348"]
for d in dois:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d, headers={"User-Agent":"gtao-rnd (mailto:none)"}), timeout=30))["message"]
        au = "; ".join(a.get("family","?") for a in r.get("author",[]))
        y = (r.get("published-print") or r.get("published-online") or r.get("issued"))["date-parts"][0][0]
        print("OK", d, "|", y, "|", (r.get("title") or ["?"])[0], "|", au, "|", (r.get("container-title") or ["?"])[0], r.get("volume",""), r.get("page", r.get("article-number","")))
    except Exception as e:
        print("FAIL", d, e)
    time.sleep(0.5)
