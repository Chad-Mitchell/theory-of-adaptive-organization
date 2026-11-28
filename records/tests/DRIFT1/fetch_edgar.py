import requests, json, time, random
UA = {"User-Agent": "gtao-drift-research research@example.invalid", "Accept-Encoding": "gzip, deflate"}
S = requests.Session(); S.headers.update(UA)
tick = S.get("https://www.sec.gov/files/company_tickers.json", timeout=60).json()
ciks = sorted({v["cik_str"] for v in tick.values()})
random.Random(20261114).shuffle(ciks)
ciks = ciks[:2000]
with open("data/edgar_filings.jsonl", "w") as f:
    for i, c in enumerate(ciks):
        for k in range(4):
            try:
                r = S.get(f"https://data.sec.gov/submissions/CIK{c:010d}.json", timeout=30)
                if r.status_code == 200:
                    j = r.json(); rec = j["filings"]["recent"]
                    f.write(json.dumps({"cik": c, "name": j.get("name"), "sic": j.get("sic"), "dates": rec["filingDate"],
                                        "forms": rec["form"], "n_older_files": len(j["filings"].get("files", []))}) + "\n")
                    break
                time.sleep(1 + k)
            except Exception:
                time.sleep(2 + k)
        time.sleep(0.2)
        if i % 200 == 0: print(i, flush=True)
print("done")
