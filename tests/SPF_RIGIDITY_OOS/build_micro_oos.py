#!/usr/bin/env python3
"""SPF-RIGIDITY-OOS: extract individual SPF forecasts (h = 0..4) for the 9 unseen candidate variables.
Reuses ../SPF_NOISE_PROXY/build_micro.extract with the kind map extended (CPI is reported as an annualised q/q rate,
as in ../LFK_SPF/build_data.VARS). No outcome (no actual, no CG regression) is touched here.
Output: data/micro_<VAR>.csv (survey_q, id, h, f). Sample: surveys with t+3 <= 2019Q4 (as LFK/SPF-NOISE-PROXY)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "SPF_NOISE_PROXY"))
import build_micro as bm
CAND = ["NGDP", "PGDP", "CPROF", "RGDP", "RCONSUM", "RNRESIN", "RRESINV", "RFEDGOV", "CPI"]
bm.KIND.update({v: "growth" for v in CAND}); bm.KIND["CPI"] = "level"   # "level" branch = take the reported value
if __name__ == "__main__":
    for v in sys.argv[1:] or CAND:
        o = bm.extract(v)
        o.to_csv(os.path.join(HERE, "data", f"micro_{v}.csv"), index=False)
        print(v, "rows", len(o), "surveys", o.survey_q.nunique(), "forecasters", o.id.nunique(), flush=True)
