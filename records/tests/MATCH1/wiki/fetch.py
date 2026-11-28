import json,urllib.request,urllib.parse,time
UA={"User-Agent":"GTAO-research/0.1 (research@example.invalid)"}
API="https://en.wikipedia.org/w/api.php"
def get(p):
    u=API+"?"+urllib.parse.urlencode(p)
    for i in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
        except Exception: time.sleep(2+2*i)
import os
kept=sum(1 for _ in open("wiki/revisions.jsonl")) if os.path.exists("wiki/revisions.jsonl") else 0
out=open("wiki/revisions.jsonl","a"); tried=0
while kept<400:
    r=get(dict(action="query",list="random",rnnamespace=0,rnlimit=50,format="json"))
    if not r: continue
    for pg in r["query"]["random"]:
        tried+=1; revs=[]; cont={}
        while True:
            q=dict(action="query",prop="revisions",pageids=pg["id"],rvprop="timestamp|user",rvlimit=500,format="json",**cont)
            d=get(q)
            if not d: break
            p=list(d["query"]["pages"].values())[0]
            revs+= [(x["timestamp"],x.get("user","")) for x in p.get("revisions",[])]
            if "continue" in d: cont=d["continue"]; time.sleep(0.1)
            else: break
        if len(revs)>=30:
            out.write(json.dumps(dict(id=pg["id"],title=pg["title"],revs=revs))+"\n"); out.flush(); kept+=1
        time.sleep(0.05)
    print(kept,tried,flush=True)
