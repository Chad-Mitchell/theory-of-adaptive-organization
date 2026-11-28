"""WIKIDATA-BAND POST-LOCK ADDENDUM (declared; see ADDENDUM_STABILITY.md). Written and committed BEFORE any main-sample outcome
was computed (main-sample collection was still running; raw/main_items.json and raw/main_pages.json did not exist).
Adds the item-level per-property stability gate described in QUEUE.md Q8 ("per-property split-half change-rate Spearman >= 0.3;
properties failing it are excluded and counted"), which the lock (PREREG §2b) did not implement (the lock's stability check is
an aggregate rate ratio). Uses the locked modules unchanged. Results are a declared SENSITIVITY: they cannot change the locked
P1-P4 verdicts. Usage: python addendum_stability.py <tag>   (reads <tag>_results.json only for the locked verdicts it reports beside)."""
import sys, json, collections
import numpy as np
from scipy.stats import spearmanr
from props import PROPS
import regime as RG
import analyze as A
SEED = 20261115; B = 500; MIN_ITEMS = 10; THRESH = 0.3

def halves(ev):
    return sum(1 for t in ev if 2016 <= t < 2021), sum(1 for t in ev if 2021 <= t < 2026)

def item_gate(items, rng):
    """Per property: items whose dated history starts before 2016 (same eligibility as the lock's split-half check).
    Spearman across items of event counts 2016-2020 vs 2021-2025. Stable iff n >= 10, both halves vary, and rho >= 0.3."""
    H = [RG.history(x)[0] for x in items]; old = [e for e in H if e and e[0] < 2016]
    out = {"n": len(old)}
    if len(old) < MIN_ITEMS: out.update(rho=None, verdict="NOT ASSESSABLE (n<10)"); return out
    a = np.array([halves(e) for e in old], float)
    if a[:, 0].std() == 0 or a[:, 1].std() == 0: out.update(rho=None, verdict="NOT ASSESSABLE (no variation)"); return out
    rho = float(spearmanr(a[:, 0], a[:, 1]).correlation); bs = []
    for _ in range(B):
        s = a[rng.integers(0, len(a), len(a))]
        if s[:, 0].std() > 0 and s[:, 1].std() > 0: bs.append(spearmanr(s[:, 0], s[:, 1]).correlation)
    out.update(rho=rho, lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), verdict="STABLE" if rho >= THRESH else "UNSTABLE")
    return out

if __name__ == "__main__":
    tag = sys.argv[1]; rng = np.random.default_rng(SEED)
    D, drift, rows = A.build(tag)
    gate = {p: item_gate([x for x in D["items"] if x["pid"] == p], rng) for p, *_ in PROPS}
    stable = sorted(p for p, g in gate.items() if g["verdict"] == "STABLE")
    res = {"gate": gate, "n_stable": len(stable), "n_unstable": sum(g["verdict"] == "UNSTABLE" for g in gate.values()),
           "n_not_assessable": sum(g["verdict"].startswith("NOT") for g in gate.values()), "stable_props": stable}
    R = [r for r in rows if r["mode"] in ("LOCAL", "LOOKUP")]; y1 = lambda r: 1 if r["mode"] == "LOOKUP" else 0
    def sens(keep, label):
        Rk = [r for r in R if r["pid"] in keep]
        if len({r["pid"] for r in Rk}) >= 5 and 0 < sum(map(y1, Rk)) < len(Rk):
            res[label] = A.coef_boot(Rk, drift, y1, ["age_rank", "log_q", "log_N"], np.random.default_rng(SEED))
            res[label]["n_rows"] = len(Rk); res[label]["props"] = sorted(keep)
        else: res[label] = f"NOT RUN (<5 properties or no outcome variation; {len({r['pid'] for r in Rk})} properties)"
    sens(set(stable), "P1_sens_item_stable")
    moot = {p for p in drift if drift[p]["lam_hi"] <= 0.02}
    sens(set(stable) | moot, "P1_sens_item_stable_or_moot")
    try:
        L = json.load(open(f"{tag}_results.json")); res["locked_verdicts_for_reference"] = {k: L.get(k) for k in ("P1", "P2", "P3", "P4")}
        ok = set(L.get("regime_ok_props", [])); sens(ok & set(stable) | moot, "P1_sens_lockregimeA_and_itemstable_or_moot")
    except FileNotFoundError: res["locked_verdicts_for_reference"] = "run analyze.py first"
    json.dump(res, open(f"{tag}_addendum_stability.json", "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in res.items() if k != "gate"}, indent=1, default=str)[:3000])
    for p, g in gate.items(): print(p, g)
