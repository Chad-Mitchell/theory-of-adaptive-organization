# Pull FDIC BankFind quarterly financials 2001Q1-2007Q4 (PREDICTORS ONLY; no failure/exit data).
import requests, pandas as pd, time, sys
rows=[]
for y in range(2001,2008):
    for md in ["0331","0630","0930","1231"]:
        d=f"{y}{md}"; off=0
        while True:
            r=requests.get("https://api.fdic.gov/banks/financials",params=dict(
                filters=f"REPDTE:{d}",fields="CERT,REPDTE,ASSET,EQ,NETINC,ROA,EQV",
                limit=10000,offset=off,format="json"),timeout=120)
            j=r.json(); dat=[x["data"] for x in j["data"]]; rows+=dat
            off+=len(dat)
            if off>=j["meta"]["total"] or not dat: break
        print(d,off,flush=True)
pd.DataFrame(rows).to_csv("data/financials_2001_2007.csv",index=False)
