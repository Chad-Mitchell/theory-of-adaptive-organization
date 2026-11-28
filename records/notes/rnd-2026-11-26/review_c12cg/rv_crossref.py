import json, urllib.request, urllib.parse, time
for d in ["10.1287/opre.11.3.399","10.1016/0022-247X(68)90201-1","10.1007/BFb0120690","10.1007/3-540-27659-9","10.1038/nature08400"]:
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+urllib.parse.quote(d),headers={"User-Agent":"gtao-review"}),timeout=30))["message"]
        au="; ".join((x.get("given","")+" "+x.get("family","")).strip() for x in r.get("author",[]))
        ed="; ".join((x.get("given","")+" "+x.get("family","")).strip() for x in r.get("editor",[]))
        yr=(r.get("published-print") or r.get("published-online") or r.get("issued"))["date-parts"][0]
        print(f"OK {d} | authors: {au or '-'} | editors: {ed or '-'} | {yr} | {r['title'][0]} | {(r.get('container-title') or [''])[0]} vol {r.get('volume','')} p {r.get('page','')} | type {r.get('type')} | edition {r.get('edition-number','')} | isbn {r.get('ISBN','')}")
    except Exception as e: print("FAIL",d,e)
    time.sleep(1)
