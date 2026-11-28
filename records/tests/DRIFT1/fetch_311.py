import requests, json, time
B = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
H = {"User-Agent": "gtao-drift-research research@example.invalid"}
def q(params):
    for k in range(5):
        try:
            r = requests.get(B, params=params, headers=H, timeout=300)
            if r.status_code == 200: return r.json()
            print(r.status_code, r.text[:200]); time.sleep(10)
        except Exception as e:
            print(e); time.sleep(10)
items = q({"$select": "complaint_type, community_board, count(*) as n", "$where": "created_date >= '2025-01-01T00:00:00' AND created_date < '2026-01-01T00:00:00'",
           "$group": "complaint_type, community_board", "$limit": 50000})
json.dump(items, open("data/nyc311_items_2025.json", "w"))
print("items", len(items))
rows = []
for y in range(2020, 2026):
    for half in [("01-01", "07-01"), ("07-01", None)]:
        end = f"{y}-{half[1]}" if half[1] else f"{y+1}-01-01"
        r = q({"$select": "date_trunc_ymdh(created_date) as h, count(*) as n", "$where": f"created_date >= '{y}-{half[0]}T00:00:00' AND created_date < '{end}T00:00:00'",
               "$group": "h", "$order": "h", "$limit": 50000})
        rows += r; print(y, half, len(r), flush=True)
json.dump(rows, open("data/nyc311_hourly_2020_2025.json", "w"))
print("done")
