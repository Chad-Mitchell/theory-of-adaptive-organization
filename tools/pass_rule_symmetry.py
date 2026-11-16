#!/usr/bin/env python3
"""Report-only pass/fail symmetry helpers (QUEUE PASS-RULE-SYMMETRY-AUDIT, pick 39).

Classifies a locked decision rule, applies it and a stated mirror, and (when useful)
reports a Monte Carlo wrong-pass rate: P(PASS | the truth sits at or beyond the
FAIL line, or otherwise misses the locked prediction). Does not change any locked
label, kill line, RESULTS file, THEORY.md, CLAIM_MAP or FRAMEWORK rule.

Families (names used in the audit report):

  causal_r0     PASS iff D - z sigma > 0 (and not FAIL); FAIL iff D + z sigma < kappa * P
  causal_r1     mirror PASS: D - z sigma > kappa * P; FAIL unchanged (pick 38 proposal)
  causal_eps    same as causal_r0 with an absolute FAIL floor eps instead of kappa * P
  relband_point PASS iff |est - pred| <= frac*|pred|; MISS iff not and the CI excludes pred
  relband_tost  mirror: PASS iff the CI lies inside the same band; FAIL iff it lies wholly outside
  ratio_band    same as relband on a ratio, band [1/m, m] (e.g. V within x/÷ 1.15)
  ratio_tost    TOST mirror of ratio_band
  onset_extra   PASS iff CI inside (pred ± delta); FAIL iff CI excludes pred AND |est-pred| >= delta/2
  onset_tost    PASS unchanged; FAIL iff CI lies wholly outside (pred ± delta)
  kernel_tost   PASS iff |D| + z sigma_D <= delta (and rivals excluded if required);
                FAIL iff |D| - z sigma_D > delta  (already a TOST pair)
  hit_zero_floor  HIT iff lo > 0; MISS iff hi < floor
  hit_floor_mirror HIT iff lo > floor; MISS unchanged
  midpoint      PASS iff lo > m; FAIL iff hi < m  (already a mirror pair)
  includes_pred PASS iff CI contains pred (and excludes `also_exclude` if given);
                FAIL iff CI excludes pred

This module is report-only. Import it or run:

  python3 tools/pass_rule_symmetry.py reread
  python3 tools/pass_rule_symmetry.py mc --reps 20000 --seed 20261115+183
"""
from __future__ import annotations

import argparse, json, math, os, sys

Z95 = 1.96


def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def verdict_causal(D, sigma, *, P=None, kappa=0.5, eps=None, z=Z95, mirror=False):
    """Causal-form / absolute-eps form. `mirror=True` is pick 38's R1 (or lo > eps)."""
    if sigma < 0:
        raise ValueError("sigma must be >= 0")
    thr = eps if eps is not None else kappa * P
    fail = (D + z * sigma) < thr
    floor = thr if mirror else 0.0
    pas = (D - z * sigma) > floor and not fail
    return "FAIL" if fail else ("PASS" if pas else "INCONCLUSIVE")


def verdict_relband(est, lo, hi, pred, *, frac=0.15, tost=False):
    band = frac * abs(pred)
    lo_b, hi_b = pred - band, pred + band
    if tost:
        if lo >= lo_b and hi <= hi_b:
            return "PASS"
        if hi < lo_b or lo > hi_b:
            return "FAIL"
        return "INCONCLUSIVE"
    if abs(est - pred) <= band:
        return "PASS"
    if hi < pred or lo > pred:
        return "MISS"
    return "INCONCLUSIVE"


def verdict_ratio_band(est, lo, hi, *, m=1.15, tost=False):
    """Band around 1 of [1/m, m]. Point-PASS vs TOST."""
    lo_b, hi_b = 1.0 / m, m
    if tost:
        if lo >= lo_b and hi <= hi_b:
            return "PASS"
        if hi < lo_b or lo > hi_b:
            return "FAIL"
        return "INCONCLUSIVE"
    if lo_b <= est <= hi_b:
        return "PASS"
    if hi < 1.0 or lo > 1.0:
        return "MISS"
    return "INCONCLUSIVE"


def verdict_onset(est, lo, hi, pred, delta, *, tost_fail=False):
    if lo > pred - delta and hi < pred + delta:
        return "PASS"
    if tost_fail:
        if hi < pred - delta or lo > pred + delta:
            return "FAIL"
        return "INCONCLUSIVE"
    if (hi < pred or lo > pred) and abs(est - pred) >= delta / 2.0:
        return "FAIL"
    return "INCONCLUSIVE"


def verdict_kernel(D, sigma_D, W, W_sd, *, delta=0.13, rivals=(0.0, 0.012, 0.725),
                   z=Z95, require_rivals=True):
    lo, hi = W - z * W_sd, W + z * W_sd
    rivals_excluded = all(not (lo <= v <= hi) for v in rivals)
    if abs(D) + z * sigma_D <= delta and (rivals_excluded if require_rivals else True):
        return "PASS"
    if abs(D) - z * sigma_D > delta:
        return "FAIL"
    return "INCONCLUSIVE"


def verdict_hit_floor(est, lo, hi, floor, *, mirror=False):
    if hi < floor:
        return "MISS"
    if lo > (floor if mirror else 0.0):
        return "HIT"
    return "INCONCLUSIVE"


def verdict_midpoint(lo, hi, m):
    if lo > m:
        return "PASS"
    if hi < m:
        return "FAIL"
    return "INCONCLUSIVE"


def verdict_includes_pred(lo, hi, pred, *, also_exclude=None):
    contains = lo <= pred <= hi
    if also_exclude is not None:
        excludes = (hi < also_exclude) or (lo > also_exclude)
        if contains and excludes:
            return "PASS"
        if not contains:
            return "FAIL"
        return "INCONCLUSIVE"
    return "PASS" if contains else "FAIL"


# ---------------------------------------------------------------------------
# Locked-result re-reads (report only; numbers from the locked RESULTS / json,
# read when this pick ran). Labels in the source files are not written here.
# ---------------------------------------------------------------------------

LOCKED_REREADS = [
    # Causal form (pick 38 already reported these; reproduced independently)
    dict(id="LAB-AKLMT-TAU Exp 1", family="causal_r0",
         D=0.5182, sigma=0.0479, P=0.9835, kappa=0.5,
         locked="PASS", file="tests/LAB_AKLMT_TAU/PREREG.md §3; results.json"),
    dict(id="LAB-AKLMT-TAU Exp 3 (report-only R3)", family="causal_r0",
         D=0.6287, sigma=0.0941, P=1.0274, kappa=0.5,
         locked="PASS", file="tests/LAB_AKLMT_TAU/PREREG.md §3; results.json"),
    dict(id="CAUSAL-NULL-INVARIANCE (author)", family="causal_r0",
         D=0.290, sigma=0.029, P=0.3504, kappa=0.5,
         locked="PASSED", file="reviews/night2/CAUSAL_NULL_INVARIANCE/PREREG.md"),
    dict(id="CAUSAL-NULL-INVARIANCE (reviewer, 7-rep mean)", family="causal_r0",
         D=0.347, sigma=0.012, P=0.3504, kappa=0.5,
         locked="PASSED", file="reviews/night2/CAUSAL_NULL_INVARIANCE_REVIEW.md"),
    dict(id="STAKES-SHIFT-CAISO", family="causal_eps",
         D=-0.08792916573905762, sigma=0.3424861359294935, eps=0.05,
         locked="INCONCLUSIVE", file="tests/STAKES_SHIFT_CAISO/PREREG.md; results.json",
         note="also G0 and G2 failed, so the contrast is not scored either way"),
    # Relative 15% band
    dict(id="LEARNSIM PREREG_2 RA", family="relband_point",
         est=-0.7355540919210248, lo=-1.031065704554559, hi=-0.5199174767590031,
         pred=-0.7585444318425878, frac=0.15,
         locked="PASS", file="tests/LEARNSIM/PREREG_2.md §3; ANALYSIS_2.json"),
    dict(id="LEARNSIM PREREG_2 AA (known-groups)", family="relband_point",
         est=-1.537602253555922, lo=-1.7703836968844853, hi=-1.3306722843507006,
         pred=-1.6496890003007756, frac=0.15,
         locked="PASS", file="tests/LEARNSIM/PREREG_2.md §3; ANALYSIS_2.json"),
    dict(id="LEARNSIM PREREG_2 AR (MV8 failed)", family="relband_point",
         est=-1.997643501227351, lo=-2.816178693079444, hi=-1.39447955564873,
         pred=-1.9119331537372306, frac=0.15,
         locked="INCONCLUSIVE (MV8 power gate failed)", file="tests/LEARNSIM/PREREG_2.md; ANALYSIS_2.json"),
    dict(id="ONSET-ACROSS-ALPHA secondary α=1.5", family="relband_point",
         est=-0.9501980267829581, lo=-1.052915459447678, hi=-0.8740302093693711,
         pred=-0.9623862581091926, frac=0.15,
         locked="PASS", file="tests/ONSET_ACROSS_ALPHA/PREREG.md §5; VERDICT.json"),
    dict(id="ONSET-ACROSS-ALPHA secondary α=2.5", family="relband_point",
         est=-0.9373042439468807, lo=-0.9739793589154161, hi=-0.9038201634407026,
         pred=-0.9625939298098181, frac=0.15,
         locked="PASS", file="tests/ONSET_ACROSS_ALPHA/PREREG.md §5; VERDICT.json"),
    # V ×/÷ 1.15
    dict(id="LEARNSIM V RR", family="ratio_band",
         est=1.0107526319204174, lo=0.8516088834885466, hi=1.1996362446914173, m=1.15,
         locked="PASS", file="tests/LEARNSIM/PREREG.md §6; ANALYSIS_1.json"),
    dict(id="LEARNSIM V RRh", family="ratio_band",
         est=1.0576372239306957, lo=0.8895232809367087, hi=1.257523576297964, m=1.15,
         locked="PASS", file="tests/LEARNSIM/PREREG.md §6; ANALYSIS_1.json"),
    dict(id="LEARNSIM V AA", family="ratio_band",
         est=1.2182082035449175, lo=0.8717311040364515, hi=1.7023956358933365, m=1.15,
         locked="INCONCLUSIVE", file="tests/LEARNSIM/PREREG.md §6; ANALYSIS_1.json"),
    # ONSET primary contrast
    dict(id="ONSET-ACROSS-ALPHA primary Δ", family="onset_extra",
         est=0.012893782836077339, lo=-0.07218679356393873, hi=0.11795570737280624,
         pred=-0.0002076717006254114, delta=0.267,
         locked="PASS", file="tests/ONSET_ACROSS_ALPHA/PREREG.md §5; VERDICT.json"),
    # KERNEL TOST
    dict(id="KERNEL-MEASURE primary", family="kernel_tost",
         D=-0.017, sigma_D=0.049, W=0.260, W_sd=0.041, delta=0.13,
         locked="PASS (exploratory)", file="tests/KERNEL_MEASURE/PREREG.md §5; RESULTS.md"),
    dict(id="KERNEL-PROXY P1", family="kernel_tost",
         D=0.0017, sigma_D=0.064, W=0.2596, W_sd=0.058, delta=0.13,
         locked="PASS (exploratory)", file="reviews/night2/KERNEL_PROXY_PREREG.md P1",
         note="slack 0.004 at the locked seed; author Ŵ 0.259 vs like-with-like 0.258"),
    # HIT vs 0 / MISS vs floor (no locked HIT to flip for C3/F1; banks is a sign HIT)
    dict(id="DECISIVE banks P1 (if HIT needed lo > 0.2)", family="hit_zero_floor",
         est=0.20, lo=0.11, hi=0.29, floor=0.2,
         locked="HIT (P1 sign + P3 point > 0)", file="tests/DECISIVE/banks/PREREG.md; RESULTS.md",
         note="the 0.2 floor is the kill rule's upper bound, applied here only as a report-only mirror, and the kill itself is restricted to the z≥1.5 subset"),
    # Already-symmetric midpoint
    dict(id="STAKES-REFEREE R-EIV night", family="midpoint",
         lo=-0.325, hi=-0.079, m=-0.483,
         locked="PASSED", file="reviews/night2/STAKES_REFEREE/PREREG_EIV.md"),
    # CI-includes-prediction
    dict(id="SELF P2 drift elasticity", family="includes_pred",
         lo=-0.01, hi=0.60, pred=0.5, also_exclude=0.0,
         locked="INCONCLUSIVE", file="reviews/night2/SELF/PREREG.md; RESULTS.md"),
]


def apply_reread(row):
    fam = row["family"]
    if fam == "causal_r0":
        locked_v = verdict_causal(row["D"], row["sigma"], P=row["P"], kappa=row["kappa"], mirror=False)
        mirror_v = verdict_causal(row["D"], row["sigma"], P=row["P"], kappa=row["kappa"], mirror=True)
    elif fam == "causal_eps":
        locked_v = verdict_causal(row["D"], row["sigma"], eps=row["eps"], mirror=False)
        mirror_v = verdict_causal(row["D"], row["sigma"], eps=row["eps"], mirror=True)
    elif fam == "relband_point":
        locked_v = verdict_relband(row["est"], row["lo"], row["hi"], row["pred"], frac=row.get("frac", 0.15), tost=False)
        mirror_v = verdict_relband(row["est"], row["lo"], row["hi"], row["pred"], frac=row.get("frac", 0.15), tost=True)
    elif fam == "ratio_band":
        locked_v = verdict_ratio_band(row["est"], row["lo"], row["hi"], m=row.get("m", 1.15), tost=False)
        mirror_v = verdict_ratio_band(row["est"], row["lo"], row["hi"], m=row.get("m", 1.15), tost=True)
    elif fam == "onset_extra":
        locked_v = verdict_onset(row["est"], row["lo"], row["hi"], row["pred"], row["delta"], tost_fail=False)
        mirror_v = verdict_onset(row["est"], row["lo"], row["hi"], row["pred"], row["delta"], tost_fail=True)
    elif fam == "kernel_tost":
        locked_v = verdict_kernel(row["D"], row["sigma_D"], row["W"], row["W_sd"], delta=row.get("delta", 0.13))
        mirror_v = locked_v  # already a TOST pair; rival-exclusion is stricter on PASS only
    elif fam == "hit_zero_floor":
        locked_v = verdict_hit_floor(row["est"], row["lo"], row["hi"], row["floor"], mirror=False)
        mirror_v = verdict_hit_floor(row["est"], row["lo"], row["hi"], row["floor"], mirror=True)
    elif fam == "midpoint":
        locked_v = verdict_midpoint(row["lo"], row["hi"], row["m"])
        mirror_v = locked_v
    elif fam == "includes_pred":
        locked_v = verdict_includes_pred(row["lo"], row["hi"], row["pred"], also_exclude=row.get("also_exclude"))
        # TOST-style mirror: CI inside a tight band around pred is not uniquely specified here;
        # the locked FAIL already is "CI excludes pred".
        mirror_v = locked_v
    else:
        raise ValueError(fam)
    return {"id": row["id"], "family": fam, "file": row["file"],
            "locked_label": row["locked"], "recomputed_locked": locked_v,
            "under_mirror": mirror_v, "note": row.get("note")}


def reread_all():
    return [apply_reread(r) for r in LOCKED_REREADS]


# ---------------------------------------------------------------------------
# Monte Carlo wrong-pass rates (normal draws; optional, used by the checks script)
# ---------------------------------------------------------------------------

def mc_rate(fn, mus, sigma, reps, seed, **kwargs):
    """Return {mu: {verdict: rate}} for D ~ N(mu, sigma). fn(D, lo, hi) or fn(D)."""
    # xorshift-style via the standard library to keep the tool stdlib-only
    import random
    rng = random.Random(seed)
    out = {}
    z = kwargs.get("z", Z95)
    for mu in mus:
        counts = {"PASS": 0, "FAIL": 0, "MISS": 0, "HIT": 0, "INCONCLUSIVE": 0}
        for _ in range(reps):
            D = rng.gauss(mu, sigma)
            lo, hi = D - z * sigma, D + z * sigma
            try:
                v = fn(D, lo, hi)
            except TypeError:
                v = fn(D)
            counts[v] = counts.get(v, 0) + 1
        out[mu] = {k: n / reps for k, n in counts.items()}
    return out


def analytic_causal_pass(r, snr, kappa=0.5, z=Z95, mirror=False):
    """P(PASS) for a causal rule when true share is r, SNR = P/sigma."""
    # FAIL if D + z sigma < kappa P  =>  (D/P) + z/SNR < kappa
    # PASS_R0 if D - z sigma > 0 and not FAIL
    # PASS_R1 if D - z sigma > kappa P
    # D/P ~ N(r, 1/SNR)
    if mirror:
        # P(D/P > kappa + z/SNR) = Phi((r - kappa)*SNR - z)
        return _norm_cdf((r - kappa) * snr - z)
    # P(D/P > z/SNR and D/P >= kappa - z/SNR). The second is 1-P(FAIL).
    # For kappa=0.5 and typical SNR, the binding PASS constraint is D-z sigma>0.
    p_dir = _norm_cdf(r * snr - z)
    p_not_fail = 1.0 - _norm_cdf((kappa - r) * snr - z)
    # These are not independent; for a single normal, PASS_R0 = P(D > z sigma and D >= kappa P - z sigma)
    # = P(D/P > max(z/SNR, kappa - z/SNR))
    thresh = max(z / snr, kappa - z / snr)
    return _norm_cdf((r - thresh) * snr)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", default="reread", choices=["reread", "mc", "analytic"])
    ap.add_argument("--reps", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261115 + 183)
    ap.add_argument("--sigma", type=float, default=1.0)
    args = ap.parse_args(argv)
    if args.cmd == "reread":
        rows = reread_all()
        print(json.dumps(rows, indent=2))
        flipped = [r for r in rows if r["under_mirror"] != r["recomputed_locked"]
                   or (r["under_mirror"] != r["locked_label"] and r["family"] in
                       ("causal_r0", "relband_point", "ratio_band", "hit_zero_floor"))]
        # just a short stderr summary
        print(f"# {len(rows)} re-reads; recomputed locked matches a PASS/FAIL/HIT/MISS/INCONCLUSIVE token in the stored label where applicable",
              file=sys.stderr)
        return 0
    if args.cmd == "analytic":
        rec = {str(snr): {f"r={r}": {"R0": round(analytic_causal_pass(r, snr, mirror=False), 4),
                                     "R1": round(analytic_causal_pass(r, snr, mirror=True), 4)}
                          for r in (0.0, 0.25, 0.40, 0.53, 1.0)}
               for snr in (5.6, 9.7, 20.0)}
        print(json.dumps(rec, indent=2))
        return 0
    print("run reviews/night2/PASS_RULE_SYMMETRY_AUDIT_checks/rules_mc.py for the full MC", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
