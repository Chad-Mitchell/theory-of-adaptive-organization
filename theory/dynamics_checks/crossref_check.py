"""Crossref lookups for DYNAMICS.md and the wide-net scan it re-checks (20 Nov 2026). Usage: python3 crossref_check.py DOI ..."""
import json,urllib.request,sys,time
for d in sys.argv[1:]:
    for attempt in range(4):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d,headers={"User-Agent":"gtao-v29-check/1.0 (mailto:chad39@gmail.com)"}),timeout=30))["message"]
            au=r.get("author",[]); a=", ".join(x.get("family","?") for x in au[:4])
            y=(r.get("issued",{}).get("date-parts",[[None]])[0][0])
            print("OK  %s | %s %s | %s | %s %s"%(d,a,y,r.get("title",[""])[0][:110],(r.get("container-title") or [""])[0][:45], r.get("volume","")),flush=True); break
        except Exception as e:
            if "429" in str(e): time.sleep(15); continue
            print("FAIL %s %s"%(d,e),flush=True); break
    time.sleep(4)
