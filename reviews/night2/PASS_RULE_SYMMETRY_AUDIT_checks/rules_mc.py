#!/usr/bin/env python3
"""Quick Monte Carlo of wrong-pass rates for the rule families in the
PASS-RULE-SYMMETRY-AUDIT report. Own code; imports only the report-only helper
tools/pass_rule_symmetry.py (stdlib + that). Run at nice 19:

    nice -n 19 python3 reviews/night2/PASS_RULE_SYMMETRY_AUDIT_checks/rules_mc.py

Writes rules_mc.json next to this file. Seed 20261115+183. 20,000 reps per cell
unless noted. D ~ Normal(mu, sigma); CI = D ± 1.96 sigma (known sigma, matching
the locked normal-CI rules).
"""
import json, math, os, random, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pass_rule_symmetry as prs

REPS = 20000
SEED = 20261115 + 183
Z = 1.96


def rates(fn, mus, sigma, reps=REPS, seed=SEED):
    rng = random.Random(seed)
    out = {}
    for mu in mus:
        counts = {}
        for _ in range(reps):
            D = rng.gauss(mu, sigma)
            lo, hi = D - Z * sigma, D + Z * sigma
            v = fn(D, lo, hi)
            counts[v] = counts.get(v, 0) + 1
        out[str(mu)] = {k: round(n / reps, 4) for k, n in sorted(counts.items())}
        out[str(mu)]["_n"] = reps
        out[str(mu)]["_sigma"] = sigma
    return out


def main():
    t0 = time.time()
    rec = {"reps": REPS, "seed": SEED, "z": Z, "families": {}}

    # A. Causal form, share r, P=1, sigma = 1/SNR, kappa=1/2. Wrong-pass = PASS | r <= kappa.
    causal = {}
    for snr in (5.6, 9.7, 20.0):
        sigma = 1.0 / snr
        mus = [0.0, 0.25, 0.40, 0.53, 1.0]  # true share; P=1 so mu=r
        def r0(D, lo, hi, sig=sigma):
            return prs.verdict_causal(D, sig, P=1.0, kappa=0.5, mirror=False)
        def r1(D, lo, hi, sig=sigma):
            return prs.verdict_causal(D, sig, P=1.0, kappa=0.5, mirror=True)
        causal[f"SNR={snr}"] = {
            "R0": rates(r0, mus, sigma, seed=SEED),
            "R1": rates(r1, mus, sigma, seed=SEED + 1),
            "analytic_R0_pass": {str(r): round(prs.analytic_causal_pass(r, snr, mirror=False), 4) for r in mus},
            "analytic_R1_pass": {str(r): round(prs.analytic_causal_pass(r, snr, mirror=True), 4) for r in mus},
        }
    rec["families"]["causal"] = causal

    # B. HIT lo>0 / MISS hi<0.15, as in C3b H1 (and F1 K1c in spirit).
    # Wrong-pass = HIT | true mu in (0, 0.15), below the miss floor.
    floor, sigma = 0.15, 0.06
    mus = [0.0, 0.05, 0.10, 0.15, 0.25]
    rec["families"]["hit_zero_floor"] = {
        "sigma": sigma, "floor": floor,
        "locked": rates(lambda D, lo, hi: prs.verdict_hit_floor(D, lo, hi, floor, mirror=False), mus, sigma, seed=SEED + 10),
        "mirror": rates(lambda D, lo, hi: prs.verdict_hit_floor(D, lo, hi, floor, mirror=True), mus, sigma, seed=SEED + 11),
    }

    # C. Relative 15% band around pred=-1 (LEARNSIM exponent rule). sigma=0.136 (RA's SE).
    pred, frac, sigma = -1.0, 0.15, 0.136
    mus = [-1.0, -0.90, -0.80, -0.736, -0.50]  # -0.736 is RA's point; -0.80 is just outside the 15% band
    rec["families"]["relband"] = {
        "pred": pred, "frac": frac, "sigma": sigma,
        "point_pass": rates(lambda D, lo, hi: prs.verdict_relband(D, lo, hi, pred, frac=frac, tost=False), mus, sigma, seed=SEED + 20),
        "tost": rates(lambda D, lo, hi: prs.verdict_relband(D, lo, hi, pred, frac=frac, tost=True), mus, sigma, seed=SEED + 21),
    }

    # D. ONSET primary: pred=0, delta=0.267, sigma=0.051 (locked SE).
    pred, delta, sigma = 0.0, 0.267, 0.051
    mus = [0.0, 0.13, 0.1335, 0.20, 0.267]  # 0.1335 = delta/2
    rec["families"]["onset"] = {
        "pred": pred, "delta": delta, "sigma": sigma,
        "locked": rates(lambda D, lo, hi: prs.verdict_onset(D, lo, hi, pred, delta, tost_fail=False), mus, sigma, seed=SEED + 30),
        "tost_fail": rates(lambda D, lo, hi: prs.verdict_onset(D, lo, hi, pred, delta, tost_fail=True), mus, sigma, seed=SEED + 31),
    }

    # E. SELF-style: PASS if CI includes 0.5 and excludes 0; FAIL if CI excludes 0.5.
    # A true value of 0.30 (40% below the prediction) can still PASS when the CI is wide.
    pred, sigma = 0.5, 0.20
    mus = [0.0, 0.30, 0.50, 0.70]
    rec["families"]["includes_pred"] = {
        "pred": pred, "sigma": sigma,
        "locked": rates(lambda D, lo, hi: prs.verdict_includes_pred(lo, hi, pred, also_exclude=0.0), mus, sigma, seed=SEED + 40),
    }

    # F. KERNEL / TOST already-symmetric pair, delta=0.13, sigma=0.049 (realized).
    # Wrong-pass ≈ PASS | |mu| > 0.13. Should be small.
    delta, sigma = 0.13, 0.049
    mus = [0.0, 0.05, 0.13, 0.20]
    rec["families"]["kernel_tost"] = {
        "delta": delta, "sigma": sigma,
        "rule": rates(lambda D, lo, hi: prs.verdict_kernel(D, sigma, D, sigma, delta=delta, require_rivals=False),
                      mus, sigma, seed=SEED + 50),
    }

    rec["elapsed_s"] = round(time.time() - t0, 3)
    path = os.path.join(HERE, "rules_mc.json")
    with open(path, "w") as f:
        json.dump(rec, f, indent=2)
        f.write("\n")
    print(json.dumps({k: rec["families"][k] for k in rec["families"]}, indent=2)[:8000])
    print(f"\nwrote {path} in {rec['elapsed_s']}s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
