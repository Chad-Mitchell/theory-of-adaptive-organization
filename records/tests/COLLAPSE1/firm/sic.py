import json,time,urllib.request,os,threading
from concurrent.futures import ThreadPoolExecutor
UA={"User-Agent":"Chad Mitchell research research@example.invalid"}
sic=json.load(open("sic.json")) if os.path.exists("sic.json") else {}
ciks=sorted(set(str(r["cik"]) for r in json.load(open("raw/InventoryNet_CY2023Q4I.json"))["data"]))
todo=[c for c in ciks if c not in sic]
lock=threading.Lock(); last=[0.0]
def one(c):
    for i in range(4):
        with lock:
            w=last[0]+0.12-time.time()
            if w>0: time.sleep(w)
            last[0]=time.time()
        try:
            r=urllib.request.urlopen(urllib.request.Request(f"https://data.sec.gov/submissions/CIK{int(c):010d}.json",headers=UA),timeout=60).read()
            d=json.loads(r); return c,d.get("sic")
        except Exception as e: time.sleep(2)
    return c,None
with ThreadPoolExecutor(8) as ex:
    for k,(c,s) in enumerate(ex.map(one,todo)):
        sic[c]=s
        if k%300==0: json.dump(sic,open("sic.json","w")); print(k,len(todo),flush=True)
json.dump(sic,open("sic.json","w")); print("done",len(sic))
