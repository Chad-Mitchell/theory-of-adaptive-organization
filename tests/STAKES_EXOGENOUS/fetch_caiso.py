#!/usr/bin/env python3
"""Fetch CAISO OASIS public data for STAKES-EXOGENOUS (no login, no key). Monthly chunks, 6 s between requests.
Writes raw CSVs into data/raw/<year>/<query>_<yyyymm>.csv. Re-runnable: skips files that exist and are non-empty."""
import io, os, sys, time, zipfile, urllib.request, calendar
BASE = "https://oasis.caiso.com/oasisapi/SingleZip"
NODES = "TH_NP15_GEN-APND,TH_SP15_GEN-APND"
Q = {"load_da": "queryname=SLD_FCST&market_run_id=DAM&version=1",
     "load_act": "queryname=SLD_FCST&market_run_id=ACTUAL&version=1",
     "lmp_da": f"queryname=PRC_LMP&market_run_id=DAM&node={NODES}&version=12",
     "lmp_fmm": f"queryname=PRC_RTPD_LMP&market_run_id=RTPD&node={NODES}&version=3"}
HERE = os.path.dirname(os.path.abspath(__file__))

def get(url, tries=5):
    for k in range(tries):
        try:
            b = urllib.request.urlopen(url, timeout=120).read()
            z = zipfile.ZipFile(io.BytesIO(b))
            name = z.namelist()[0]
            if name.endswith(".csv"):
                return z.read(name)
            print("  non-csv", name, z.read(name)[:300], flush=True)
        except Exception as e:
            print("  err", k, e, flush=True)
        time.sleep(15 * (k + 1))
    return None

def main(years):
    for y in years:
        for m in range(1, 13):
            ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
            # two chunks per month (OASIS caps a query at 31 days); GMT windows padded by 1 h, trimmed later by OPR_DT
            for half, (s, e) in enumerate([(f"{y}{m:02d}01T07:00-0000", f"{y}{m:02d}16T08:00-0000"),
                                           (f"{y}{m:02d}16T07:00-0000", f"{ny}{nm:02d}01T08:00-0000")]):
                for key, q in Q.items():
                    out = os.path.join(HERE, "data", "raw", str(y), f"{key}_{y}{m:02d}_{half}.csv")
                    if os.path.exists(out) and os.path.getsize(out) > 0:
                        continue
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    url = f"{BASE}?{q}&startdatetime={s}&enddatetime={e}&resultformat=6"
                    print(key, y, m, half, flush=True)
                    b = get(url)
                    if b is not None:
                        open(out, "wb").write(b)
                    time.sleep(6)

if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or [2025, 2024])
