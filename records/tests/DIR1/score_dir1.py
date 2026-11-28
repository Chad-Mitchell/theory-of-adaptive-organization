#!/usr/bin/env python3
"""DIR1 scoring (locked before any outcome retrieval). Reads data/coded.csv, writes ANALYSIS_DIR1.json.

coded.csv columns: cell,class,prediction,rank,doi,included,code,exclusion_reason,locator
  included in {1,0}; code in {1,0,-1} for included rows.
"""
import csv, json, sys
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def binom_upper(k, n, p=0.5):
    """One-sided exact P(X >= k), X ~ Bin(n, p)."""
    if n == 0:
        return 1.0
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def summarize(rows):
    n = len(rows)
    plus = sum(1 for r in rows if r["code"] == 1)
    minus = sum(1 for r in rows if r["code"] == -1)
    zero = n - plus - minus
    nz = plus + minus
    return {"n": n, "plus": plus, "minus": minus, "zero": zero,
            "rate": (plus / n) if n else None,
            "p_primary": binom_upper(plus, n), "p_sign_vs_R0": binom_upper(plus, nz) if nz else None}


def main(path=None):
    spec = json.loads((HERE / "PREDICTIONS_DIR1.json").read_text())
    sc = spec["scoring"]
    path = Path(path) if path else HERE / "data" / "coded.csv"
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if r["included"].strip() == "1":
                r["code"] = int(r["code"])
                assert r["code"] in (1, 0, -1), r
                rows.append(r)
    # one system per (cell, doi): duplicates are an error
    keys = [(r["cell"], r["doi"].lower()) for r in rows]
    assert len(keys) == len(set(keys)), "duplicate system in a cell"
    out = {"by_cell": {}, "by_prediction": {}, "by_class": {}, "pooled": summarize(rows)}
    for c in spec["cells"]:
        out["by_cell"][c["id"]] = summarize([r for r in rows if r["cell"] == c["id"]])
    for d in spec["predictions"]:
        out["by_prediction"][d] = summarize([r for r in rows if r["prediction"] == d])
    n_support = n_fail = 0
    for k in spec["classes"]:
        s = summarize([r for r in rows if r["class"] == k])
        s["qualifies_n"] = s["n"] >= sc["n_min_per_class"]
        s["supports"] = bool(s["qualifies_n"] and s["p_primary"] < sc["alpha"] and s["rate"] > sc["kill_rate"])
        s["fails"] = bool(s["qualifies_n"] and s["rate"] <= sc["kill_rate"])
        n_support += s["supports"]; n_fail += s["fails"]
        out["by_class"][k] = s
    pooled_rate = out["pooled"]["rate"] or 0.0
    if pooled_rate <= sc["kill_rate"] or n_fail >= 2:
        verdict = "FAIL"
    elif n_support >= 2:
        verdict = "PASS"
    else:
        verdict = "INCONCLUSIVE"
    out["classes_supporting"] = n_support
    out["classes_failing"] = n_fail
    out["verdict"] = verdict
    out["note"] = "Verdict concerns the directional corollary under the coarse qualification tier QC only; it is not a test of the banded hypothesis of THEORY section 3."
    (HERE / "ANALYSIS_DIR1.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({"verdict": verdict, "pooled": out["pooled"], "by_class": out["by_class"]}, indent=1))
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
