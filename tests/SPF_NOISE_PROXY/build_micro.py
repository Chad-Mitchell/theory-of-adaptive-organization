#!/usr/bin/env python3
"""Extract SPF individual forecasts at horizons h = 0..4 (current quarter .. 4 quarters ahead) for the 7 variables.
Source: Philadelphia Fed SPFmicrodata.xlsx (box: <local>/lfk_spf/, sha256 in ../LFK_SPF/data/RAW_SHA256.txt).
Columns VAR2..VAR6 = quarters t..t+4 (VAR1 = t-1). Level variables: the value. Growth variables: annualised q/q growth
100((X_k/X_{k-1})^4 - 1) from the same forecaster's levels (as ../LFK_SPF). Sample: surveys with t+3 <= 2019Q4 (LFK sample).
Output: data/micro_<VAR>.csv (survey_q, id, h, f). Usage: python3 build_micro.py [VARS...]
"""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.environ.get("LFK_RAW", "<local>/lfk_spf")
KIND = {"UNEMP": "level", "HOUSING": "level", "TBILL": "level", "BOND": "level", "TBOND": "level",
        "RSLGOV": "growth", "INDPROD": "growth", "CPROF": "growth"}
END_Q = 2019 * 4 + 3

def extract(v):
    d = pd.read_excel(os.path.join(RAW, "SPFmicrodata.xlsx"), sheet_name=v, engine="calamine")
    sq = (d.YEAR * 4 + d.QUARTER - 1).astype(int)
    c = {k: pd.to_numeric(d[f"{v}{k}"], errors="coerce") for k in range(1, 7)}
    rows = []
    for h in range(5):
        k = h + 2
        f = c[k] if KIND[v] == "level" else 100 * ((c[k] / c[k - 1]) ** 4 - 1)
        rows.append(pd.DataFrame({"survey_q": sq, "id": d.ID.astype(int), "h": h, "f": f}))
    out = pd.concat(rows).dropna()
    out = out[np.isfinite(out.f) & (out.survey_q + 3 <= END_Q)]
    out = out.drop_duplicates(["survey_q", "id", "h"])
    return out

if __name__ == "__main__":
    vs = sys.argv[1:] or ["UNEMP", "HOUSING", "TBILL", "BOND", "TBOND", "RSLGOV", "INDPROD"]
    for v in vs:
        o = extract(v)
        o.to_csv(os.path.join(HERE, "data", f"micro_{v}.csv"), index=False)
        print(v, "rows", len(o), "surveys", o.survey_q.nunique(), "forecasters", o.id.nunique())
