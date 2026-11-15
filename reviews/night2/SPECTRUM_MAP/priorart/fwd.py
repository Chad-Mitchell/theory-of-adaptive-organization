import json,urllib.request,time,sys
def inv(ii):
    if not ii: return ""
    pos=[]
    for w,ps in ii.items():
        for p in ps: pos.append((p,w))
    return " ".join(w for p,w in sorted(pos))
out={}
for wid in ["W1897832025","W4392251645"]:
    recs=[];page=1
    while True:
        u=f"https://api.openalex.org/works?filter=cites:{wid}&per-page=200&page={page}&mailto=research@example.invalid"
        d=json.load(urllib.request.urlopen(u))
        for w in d["results"]:
            recs.append(dict(id=w["id"],title=w["display_name"],year=w["publication_year"],doi=w.get("doi"),abstract=inv(w.get("abstract_inverted_index"))))
        if len(d["results"])<200: break
        page+=1; time.sleep(1)
    out[wid]=recs; print(wid,len(recs))
json.dump(out,open("fwd_bm2016_abolhassani2024.json","w"),indent=1)
