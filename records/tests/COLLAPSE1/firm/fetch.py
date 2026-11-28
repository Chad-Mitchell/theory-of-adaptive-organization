import json,time,urllib.request,os
UA={"User-Agent":"Chad Mitchell research research@example.invalid"}
def get(u):
    for i in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60))
        except Exception as e:
            time.sleep(2+i*2); err=e
    raise err
os.makedirs("raw",exist_ok=True)
frames=[("InventoryNet","CY%dQ4I"),("CostOfGoodsAndServicesSold","CY%d"),("CostOfRevenue","CY%d"),("CostOfGoodsSold","CY%d")]
for tag,f in frames:
    for y in range(2019,2024):
        fn=f"raw/{tag}_{f%y}.json"
        if os.path.exists(fn): continue
        try:
            d=get(f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/{f%y}.json")
            json.dump(d,open(fn,"w"))
        except Exception as e: print("fail",tag,y,e)
        time.sleep(0.2)
ciks=set(r["cik"] for r in json.load(open("raw/InventoryNet_CY2023Q4I.json"))["data"])
sic={}
if os.path.exists("sic.json"): sic=json.load(open("sic.json"))
for i,c in enumerate(sorted(ciks)):
    if str(c) in sic: continue
    try:
        d=get(f"https://data.sec.gov/submissions/CIK{int(c):010d}.json")
        sic[str(c)]=d.get("sic")
    except Exception as e: sic[str(c)]=None
    time.sleep(0.12)
    if i%200==0: json.dump(sic,open("sic.json","w")); print(i,len(ciks),flush=True)
json.dump(sic,open("sic.json","w")); print("done")
