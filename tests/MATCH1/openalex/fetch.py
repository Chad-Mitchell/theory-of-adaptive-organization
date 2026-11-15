import json,urllib.request,time,random,collections
M="mailto=research@example.invalid"
def get(u):
    for i in range(5):
        try: return json.load(urllib.request.urlopen(u,timeout=60))
        except Exception: time.sleep(2+2*i)
# volume per publication year
vol=get(f"https://api.openalex.org/works?group_by=publication_year&per_page=200&{M}")["group_by"]
json.dump(vol,open("openalex/volume_by_year.json","w"))
# sample citing works published 2023 with references, random sample via seed
refs=[]; citing=0
for seed in range(1,41):
    d=get(f"https://api.openalex.org/works?filter=publication_year:2023,type:article,referenced_works_count:>0&sample=50&seed={seed}&select=id,referenced_works&per_page=50&{M}")
    for w in d.get("results",[]): citing+=1; refs+=w["referenced_works"]
print("citing",citing,"refs",len(refs),flush=True)
years=collections.Counter()
ids=[r.split("/")[-1] for r in refs]
for i in range(0,len(ids),50):
    b="|".join(ids[i:i+50])
    d=get(f"https://api.openalex.org/works?filter=openalex_id:{b}&select=id,publication_year&per_page=50&{M}")
    for w in (d or {}).get("results",[]):
        if w.get("publication_year"): years[w["publication_year"]]+=1
    if i%5000==0: print(i,len(ids),flush=True)
json.dump(dict(citing=citing,nrefs=len(refs),years=years),open("openalex/ref_years.json","w")); print("done")
