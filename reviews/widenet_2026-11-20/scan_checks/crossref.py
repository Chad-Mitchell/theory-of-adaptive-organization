import json,urllib.request,sys
dois=sys.argv[1:]
import time
for d in dois:
    time.sleep(2.5)
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d,headers={"User-Agent":"gtao-scan (mailto:none@example.com)"}),timeout=20))["message"]
        a=r.get("author",[{}])[0].get("family","?"); y=(r.get("issued",{}).get("date-parts",[[None]])[0][0])
        print("OK  %s | %s %s | %s | %s"%(d,a,y,r.get("title",[""])[0][:90],(r.get("container-title") or [""])[0][:40]))
    except Exception as e: print("FAIL %s %s"%(d,e))
