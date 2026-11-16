#!/usr/bin/env python3
"""Fetch CAISO OASIS SLD_FCST RTM/RTD (CA ISO-TAC), 2024-2025, half-month chunks. Public API, no login/key. Own copy of pick 15's query."""
import io, os, sys, time, zipfile, subprocess
BASE = "https://oasis.caiso.com/oasisapi/SingleZip"
Q = "queryname=SLD_FCST&market_run_id=RTM&execution_type=RTD&version=1&tac_area_name=CA%20ISO-TAC"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
def get(url):
    for k in range(4):
        try:
            b = subprocess.run(["curl", "-s", "-m", "180", url], capture_output=True, timeout=200).stdout
            z = zipfile.ZipFile(io.BytesIO(b)); n = z.namelist()[0]
            if n.endswith(".csv"): return z.read(n)
            print("non-csv", n, z.read(n)[-200:], flush=True)
        except Exception as e: print("err", k, e, flush=True)
        time.sleep(15 * (k + 1))
for y in (2024, 2025):
    for m in range(1, 13):
        ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        for h, (s, e) in enumerate([(f"{y}{m:02d}01T07:00-0000", f"{y}{m:02d}16T08:00-0000"), (f"{y}{m:02d}16T07:00-0000", f"{ny}{nm:02d}01T08:00-0000")]):
            f = os.path.join(OUT, f"rtd_{y}{m:02d}_{h}.csv")
            if os.path.exists(f) and os.path.getsize(f) > 0: continue
            os.makedirs(OUT, exist_ok=True); print(y, m, h, flush=True)
            b = get(f"{BASE}?{Q}&startdatetime={s}&enddatetime={e}&resultformat=6")
            if b: open(f, "wb").write(b)
            time.sleep(6)
