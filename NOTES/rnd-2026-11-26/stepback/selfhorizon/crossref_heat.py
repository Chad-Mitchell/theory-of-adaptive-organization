import json, urllib.request
dois=["10.1147/rd.53.0183","10.1145/958942.958945","10.1007/BF02084158","10.1287/opre.38.6.947"]
for d in dois:
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d,headers={"User-Agent":"gtao-notes (mailto:none)"}),timeout=30))["message"]
        print("OK",d,"|",r.get("issued",{}).get("date-parts",[[None]])[0][0],"|",";".join(a.get("family","") for a in r.get("author",[])),"|",r.get("title",[""])[0],"|",(r.get("container-title") or [""])[0],"|",r.get("volume"),r.get("page"))
    except Exception as e: print("FAIL",d,e)
