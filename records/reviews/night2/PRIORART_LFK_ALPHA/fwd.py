import json, sys, urllib.request, urllib.parse, time
M="mailto=box@example.invalid"
def get(u):
    for k in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=60))
        except Exception as e: err=e; time.sleep(2)
    raise err
def wid(doi):
    return get(f"https://api.openalex.org/works/doi:{doi}?{M}")
def citers(w):
    out=[]; cur="*"
    while cur:
        d=get(f"https://api.openalex.org/works?filter=cites:{w}&per-page=200&cursor={cur}&{M}")
        out+=d["results"]; cur=d["meta"].get("next_cursor")
        if not d["results"]: break
    return out
def abstract(r):
    ii=r.get("abstract_inverted_index") or {}
    pos=sorted((p,w) for w,ps in ii.items() for p in ps)
    return " ".join(w for _,w in pos)
res={}
for name,doi in [("LFK2024","10.1098/rspb.2024.1606"),("LFK_preprint","10.1101/2022.09.01.506204"),
                 ("Afterman2022","10.1137/20M1360359"),("Kleptsyna2020","10.1134/S0005117920030030"),
                 ("MoraNemenman2019","10.1103/PhysRevLett.123.198101")]:
    try: w=wid(doi)
    except Exception as e: res[name]={"error":str(e)}; continue
    c=citers(w["id"].split("/")[-1])
    res[name]={"id":w["id"],"cited_by_count":w.get("cited_by_count"),"citers":[
      {"id":r["id"],"doi":r.get("doi"),"title":r.get("title"),"year":r.get("publication_year"),
       "oa":(r.get("best_oa_location") or {}).get("pdf_url") or (r.get("open_access") or {}).get("oa_url"),
       "abstract":abstract(r)} for r in c]}
    print(name, w.get("cited_by_count"), len(c), flush=True)
json.dump(res,open("fwd_citers.json","w"),indent=1)
