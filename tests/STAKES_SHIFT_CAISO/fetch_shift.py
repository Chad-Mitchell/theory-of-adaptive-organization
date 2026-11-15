#!/usr/bin/env python3
"""Fetch CAISO OASIS public data for STAKES-SHIFT-CAISO (no login, no key). CA ISO-TAC only, half-month chunks, 6 s apart.
Writes raw CSVs to data/raw/<year>/<key>_<yyyymm>_<half>.csv. Re-runnable (skips non-empty files).
Usage: python3 fetch_shift.py 2026 2025 2024 2023 2022 2021 2020 2019   (2026 stops at 2026-10-31)."""
import io, os, sys, time, zipfile, subprocess
BASE = "https://oasis.caiso.com/oasisapi/SingleZip"
TAC = "tac_area_name=CA%20ISO-TAC"
Q = {"load_da":  f"queryname=SLD_FCST&market_run_id=DAM&version=1&{TAC}",
     "load_2da": f"queryname=SLD_FCST&market_run_id=2DA&version=1&{TAC}",
     "load_act": f"queryname=SLD_FCST&market_run_id=ACTUAL&version=1&{TAC}",
     "load_rtd": f"queryname=SLD_FCST&market_run_id=RTM&execution_type=RTD&version=1&{TAC}"}
HERE = os.path.dirname(os.path.abspath(__file__))

def get(url, tries=4):
    for k in range(tries):
        try:
            b = subprocess.run(["curl", "-s", "-m", "180", url], capture_output=True, timeout=200).stdout
            z = zipfile.ZipFile(io.BytesIO(b)); name = z.namelist()[0]
            if name.endswith(".csv"):
                return z.read(name)
            print("  non-csv", name, z.read(name)[-300:], flush=True)
            if b"No data returned" in z.read(name):
                return b""          # empty marker: OASIS holds nothing for this window
        except Exception as e:
            print("  err", k, e, flush=True)
        time.sleep(15 * (k + 1))
    return None

def main(years):
    for y in years:
        for m in range(1, 13):
            if y == 2026 and m > 10:
                break
            ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
            for half, (s, e) in enumerate([(f"{y}{m:02d}01T07:00-0000", f"{y}{m:02d}16T08:00-0000"),
                                           (f"{y}{m:02d}16T07:00-0000", f"{ny}{nm:02d}01T08:00-0000")]):
                for key, q in Q.items():
                    out = os.path.join(HERE, "data", "raw", str(y), f"{key}_{y}{m:02d}_{half}.csv")
                    if os.path.exists(out):
                        continue
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    print(key, y, m, half, flush=True)
                    b = get(f"{BASE}?{q}&startdatetime={s}&enddatetime={e}&resultformat=6")
                    if b is not None:
                        open(out, "wb").write(b)
                    time.sleep(6)

if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])
