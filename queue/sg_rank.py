#!/usr/bin/env python3
"""SURPRISE-GUIDED-SEARCH (SG) ranking rule for the GTAO queue. Locked parameters below; any change
needs a new ledger entry of kind "rule_change" BEFORE use. Derivation: reviews/night2/AUDIT_DIVERGENCE.md §6
(Proposition SG; check reviews/night2/AUDIT_checks/sg_check.py).

Index  I_k = w_k * P_k * v_k * L_k / c_k
  w  stakes: 3 = could change a THEORY.md §0/§2 headline claim or a "theory's own" row (§8b list);
             2 = could change any other CLAIM_MAP row; 1 = process/infrastructure only.
  P  probability the claim's status is wrong / the item has "woken up":
       never tested on a valid instrument  -> 0.5
       otherwise surprise-updated regime-B prior:
         p0 = 1 - ((a+A0)/(a+DELTA+A0))**GAMMA,  a = days since the topic's last status change
         P  = LR*p0 / (1 - p0 + LR*p0),  LR from the locked surprise scale below
  v  validity: probability the planned run can change a CLAIM_MAP status at all (gates, tier ceiling)
  L  exposure: 1 + number of queue items / claim rows whose design depends on this result
  c  expected cost, weekly-usage percentage points (floor 0.5)
Surprise scale (LR): none 1; weak (1-2 SE off prediction, or a referee flag) 3;
  strong (>2 SE, locked pass/fail on a valid instrument, math counterexample, Chad correction) 10;
  decisive (exact reproducible contradiction) 30.
"""
import json, sys
GAMMA, A0, DELTA = 0.4, 1.0, 1.0   # GAMMA from SELF P1b (-0.39); the only in-environment estimate
LR = {"none": 1, "weak": 3, "strong": 10, "decisive": 30}

def prob(it):
    if it.get("untested", False):
        return 0.5
    a = max(it["age_days"], 0.1)
    p0 = 1 - ((a + A0) / (a + DELTA + A0)) ** GAMMA
    lr = LR[it["surprise"]]
    return lr * p0 / (1 - p0 + lr * p0)

def rank(items):
    out = []
    for it in items:
        P = prob(it)
        I = it["w"] * P * it["v"] * it["L"] / max(it["c"], 0.5)
        out.append({**it, "P": round(P, 3), "index": round(I, 3)})
    return sorted(out, key=lambda r: -r["index"])

if __name__ == "__main__":
    items = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "items.json"))
    for i, r in enumerate(rank(items), 1):
        print(f'{i:2d}. {r["id"]:22s} I={r["index"]:6.3f}  w={r["w"]} P={r["P"]} v={r["v"]} L={r["L"]} c={r["c"]}')
