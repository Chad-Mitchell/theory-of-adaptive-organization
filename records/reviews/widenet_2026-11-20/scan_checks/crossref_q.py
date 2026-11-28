import json,urllib.request,urllib.parse,sys,time
for q in sys.argv[1:]:
    time.sleep(8)
    u="https://api.crossref.org/works?rows=2&query.bibliographic="+urllib.parse.quote(q)
    try:
        for r in json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"gtao-scan (mailto:none@example.com)"}),timeout=30))["message"]["items"]:
            print("Q[%s] -> %s | %s %s | %s"%(q[:30],r["DOI"],r.get("author",[{}])[0].get("family","?"),r.get("issued",{}).get("date-parts",[[None]])[0][0],r.get("title",[""])[0][:80]))
    except Exception as e: print("FAIL",q,e)
