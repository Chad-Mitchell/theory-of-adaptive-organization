import requests, json, time
B = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
H = {"User-Agent": "gtao-drift-research research@example.invalid"}
def q(params):
    for k in range(5):
        try:
            r = requests.get(B, params=params, headers=H, timeout=600)
            if r.status_code == 200: return r.json()
            print(r.status_code, r.text[:300], flush=True); time.sleep(10)
        except Exception as e:
            print(e, flush=True); time.sleep(10)
    return []
rows = []
for y in range(2020, 2026):
    for a, b in [("01-01", "04-01"), ("04-01", "07-01"), ("07-01", "10-01"), ("10-01", None)]:
        end = f"{y}-{b}" if b else f"{y+1}-01-01"
        r = q({"$select": "date_trunc_ymd(created_date) as d, date_extract_hh(created_date) as hh, count(*) as n",
               "$where": f"created_date >= '{y}-{a}T00:00:00' AND created_date < '{end}T00:00:00'",
               "$group": "d, hh", "$order": "d, hh", "$limit": 50000})
        rows += r; print(y, a, len(r), flush=True)
json.dump(rows, open("data/nyc311_hourly_2020_2025.json", "w"))
print("done")
