#!/usr/bin/env python3
"""Feasibility / power gate for GTAO preregs (QUEUE CAUSAL-POWER-GATE, merged with KG-FEASIBILITY-GATE; pick 19, ledger 92-95).

Rule (measurement/FRAMEWORK.md MV10): before a causal-form or optimality-form prereg is locked, it shows, on its own
planned data (planned n, span, input change and the noise measured before lock), that BOTH its PASS rule and its FAIL
rule are reachable with a stated probability pi (default 0.8):
    P(PASS | the locked prediction is true)  >= pi      and
    P(FAIL | the null the FAIL rule is meant to catch is true) >= pi,
and that each rule can fire at its own best-case data (the deterministic check that WIKIDATA-BAND's KG(a) failed).

Model (first principles). A causal-form test reads a contrast D whose expected value is the locked elasticity b times
the measured input change: E[D] = b * dlog x (x = stakes, q, N, alpha ...) -- for a causal-form test, b is the locked
elasticity scaled by the design's adjustment share s at the locked lag and by the input measurement's reliability lam
(THEORY v1.4.7 Sec. 1 N6; pass --scale s*lam, or an already scaled --effect / --b) -- and whose noise sigma is the year-to-year
(or unit-to-unit) sd of D when the inputs did not change (s_yr, which already contains sampling noise; add any extra
sampling se in quadrature). With K independent contrasts k with input changes d_k and common elasticity b, the least
squares slope through the origin has se = sigma / S, S = sqrt(sum d_k^2), so the signal-to-noise ratio is
    SNR = |b| * S / sigma            (S = |dlog x| for one contrast).
With PASS iff D - z*sigma > 0 (z = z_{1-a/2}) and FAIL iff D + z*sigma < kappa * b*S (data exclude kappa of the predicted move;
THEORY v1.4.7 Sec. 1 N6 requires 0 < kappa <= 1/2 for a causal kill, so the default is kappa = 1/2; kappa = 1 is a test of
size, kills an exactly optimal design at rate ~z-size even when s, lam are known and far more often when they or alpha are
estimated; it is kept only to reproduce numbers computed before v1.4.7, and the gate reports kappa_in_N6_range = false):
    P(PASS | true)  = Phi(SNR - z),      P(FAIL | null b = 0) = Phi(kappa*SNR - z).
Both >= pi  <=>  the minimal gate
    |b| * S  >=  (z_{1-a/2} + z_pi) * sigma / min(1, kappa)        [= 2.80 sigma / min(1, kappa) at a = 0.05, pi = 0.8]
i.e. the needed input change in log units is S_req = (z_{1-a/2} + z_pi) * sigma / (|b| * min(1, kappa)), a factor
exp(S_req). A FAIL rule with an ABSOLUTE margin eps (FAIL iff D + z*sigma < eps, as in STAKES-SHIFT-CAISO) is reachable
with probability pi under the null only if sigma <= eps / (z + z_pi), whatever the input change: no change in x can buy
it. An optimality-form test is the same with b*S replaced by the gap Delta between the locked optimum and the nearest
named rival (this is MV8(i), SE <= Delta/2.8, applied to both rules).

Commands (all print JSON; exit code 0 = gate met, 1 = not met):
  power_gate.py contrast --sigma S (--effect M | --b B --dlogx DX [DX ...]) [--scale SL] [--fail-eps E | --fail-kappa K]
                         [--form causal|optimality]
                         [--band-top T] [--alpha 0.05] [--power 0.8] [--noise-df DF] [--sims N] [--seed 1]
                         [--rival-effect R]   (report-only: P(FAIL | named same-loss rival true); PREREG-LOSS-LOCK)
  power_gate.py required --sigma S --b B [--scale SL] [--fail-kappa K (default 0.5)] [--alpha 0.05] [--power 0.8] [--per-contrast DX]
  power_gate.py zero-events --n N --years Y --bound L [--method wilson|poisson] [--z 1.96]
Defaults (v1.4.7 review, CAUSAL-KILL-MAGNITUDE-REVIEW): form = "causal" (THEORY Sec. 1 N6 causal kill): kappa = 1/2
wherever a FAIL threshold is relative and none is given, and a gate with fail_kappa outside (0, 1/2] is not met (reason
'kappa_outside_N6_range'). form = "optimality" (effect = gap Delta to the nearest named rival; MV10 "Delta >= 2.80 sigma",
i.e. kappa = 1): default kappa = 1 and no N6 range check, as before v1.4.7.
"""
import argparse, json, math, sys
from statistics import NormalDist

N01 = NormalDist()
Phi, zq = N01.cdf, N01.inv_cdf


def z_two_sided(alpha):
    return zq(1 - alpha / 2)


def snr(b, dlogx, sigma):
    """|b| * sqrt(sum d_k^2) / sigma for one or several independent contrasts."""
    d = [dlogx] if isinstance(dlogx, (int, float)) else list(dlogx)
    return abs(b) * math.sqrt(sum(x * x for x in d)) / sigma


DEFAULT_KAPPA = 0.5   # THEORY v1.4.7 Sec. 1 N6: 0 < kappa <= 1/2


def kappa_in_n6_range(kappa):
    return kappa is not None and 0.0 < kappa <= DEFAULT_KAPPA


def required_change(b, sigma, alpha=0.05, power=0.8, kappa=DEFAULT_KAPPA):
    """Minimal S = sqrt(sum dlog x_k^2) (log units) so that PASS|true and FAIL|null both have probability >= power."""
    return (z_two_sided(alpha) + zq(power)) * sigma / (abs(b) * min(1.0, kappa))


def required_contrasts(b, sigma, per_contrast, alpha=0.05, power=0.8, kappa=DEFAULT_KAPPA):
    """Independent contrasts of size |per_contrast| needed: K = ceil((S_req / |d|)^2)."""
    return math.ceil((required_change(b, sigma, alpha, power, kappa) / abs(per_contrast)) ** 2)


def default_kappa(form):
    if form not in ("causal", "optimality"):
        raise ValueError("form must be 'causal' or 'optimality'")
    return DEFAULT_KAPPA if form == "causal" else 1.0


def analytic(effect, sigma, alpha=0.05, fail_eps=None, fail_kappa=None, band_top=None, form="causal"):
    """Exact probabilities for D ~ N(mu, sigma^2) with sigma known, rules oriented so the predicted move is positive.
    PASS iff D - z sigma > 0 and (D <= band_top if given); FAIL iff D + z sigma < thr; thr = fail_eps or fail_kappa*effect."""
    z = z_two_sided(alpha)
    thr = fail_eps if fail_eps is not None else (fail_kappa if fail_kappa is not None else default_kappa(form)) * effect
    def p_pass(mu):
        hi = 1.0 if band_top is None else Phi((band_top - mu) / sigma)
        return max(0.0, hi - Phi(z - mu / sigma))
    def p_fail(mu):
        return Phi((thr - z * sigma - mu) / sigma)
    return {"z": z, "fail_threshold": thr,
            "P_pass_true": p_pass(effect), "P_fail_null": p_fail(0.0),
            "P_fail_true": p_fail(effect), "P_pass_null": p_pass(0.0),
            "pass_region_empty": band_top is not None and band_top <= z * sigma,
            "best_case_pass_fires": (effect - z * sigma > 0) and (band_top is None or effect <= band_top),
            "best_case_fail_fires": (0.0 + z * sigma) < thr}


def simulate(effect, sigma, alpha=0.05, fail_eps=None, fail_kappa=None, band_top=None, noise_df=None, sims=200_000,
             seed=1, noise_draws=None, form="causal"):
    """Monte Carlo of the locked decision on planned data. noise_df: the decision uses sigma_hat with
    sigma_hat^2 ~ sigma^2 chi2_df/df (sigma estimated from df+1 year pairs before lock). noise_draws: optional list of
    observed noise residuals (e.g. the year-pair D's minus their mean) resampled instead of Normal noise."""
    import numpy as np
    rng = np.random.default_rng(seed)
    z = z_two_sided(alpha)
    thr = fail_eps if fail_eps is not None else (fail_kappa if fail_kappa is not None else default_kappa(form)) * effect
    out = {}
    for name, mu in (("true", effect), ("null", 0.0)):
        if noise_draws is not None:
            r = np.asarray(noise_draws, float); r = (r - r.mean()) / r.std(ddof=1) * sigma
            e = rng.choice(r, sims)
        else:
            e = rng.normal(0, sigma, sims)
        d = mu + e
        s = sigma * np.sqrt(rng.chisquare(noise_df, sims) / noise_df) if noise_df else np.full(sims, sigma)
        p = (d - z * s > 0) & ((d <= band_top) if band_top is not None else True)
        f = d + z * s < thr
        out[f"P_pass_{name}"] = float(p.mean()); out[f"P_fail_{name}"] = float(f.mean())
    out.update({"sims": sims, "seed": seed, "noise_df": noise_df, "noise": "resampled" if noise_draws is not None else "normal"})
    return out


def rival_check(effect, rival_effect, sigma, alpha=0.05, power=0.8, fail_eps=None, fail_kappa=None, form="causal"):
    """Proposed MV10 discrimination line (QUEUE PREREG-LOSS-LOCK, pick 37; THEORY v1.4.16 author-only PR, not yet in force):
    a prereg that claims its test can tell the locked optimum from a named rival optimum (computed for the SAME loss)
    reports P(FAIL | the rival's predicted move is the truth) on its planned data. The FAIL rule fires iff
    D + z sigma < thr (thr = fail_eps or kappa*effect), so with D ~ N(rival_effect, sigma^2):
        P(FAIL | rival) = Phi((thr - z sigma - rival_effect) / sigma).
    If rival_effect >= thr the FAIL leg cannot reach the rival at any sample size (sigma -> 0 never helps):
    'rival_unreachable_any_n' (pick 35: a 0-1-best linear rival moves 70-81% of the Bayes move, above kappa_F = 1/2).
    Reporting only: gate_met is unchanged; 'discriminates_rival' is the proposed label condition."""
    z = z_two_sided(alpha)
    thr = fail_eps if fail_eps is not None else (fail_kappa if fail_kappa is not None else default_kappa(form)) * effect
    p = Phi((thr - z * sigma - rival_effect) / sigma)
    return {"rival_effect": rival_effect, "fail_threshold": thr, "P_fail_rival": p,
            "rival_unreachable_any_n": rival_effect >= thr,
            "best_case_rival_fail_fires": rival_effect + z * sigma < thr,
            "discriminates_rival": p >= power and rival_effect + z * sigma < thr}


def gate(effect, sigma, alpha=0.05, power=0.8, fail_eps=None, fail_kappa=None, band_top=None, noise_df=None,
         sims=0, seed=1, form="causal", rival_effect=None):
    a = analytic(effect, sigma, alpha, fail_eps, fail_kappa, band_top, form)
    res = {"inputs": {"effect": effect, "sigma": sigma, "alpha": alpha, "power": power, "fail_eps": fail_eps,
                      "fail_kappa": fail_kappa, "band_top": band_top, "noise_df": noise_df, "form": form},
           "SNR": effect / sigma, "analytic": a}
    probs = a
    if sims:
        res["simulated"] = simulate(effect, sigma, alpha, fail_eps, fail_kappa, band_top, noise_df, sims, seed, form=form)
        probs = res["simulated"]
    zp = z_two_sided(alpha) + zq(power)
    res["needed"] = {"effect_for_pass": zp * sigma,
                     "sigma_max_for_fail": (fail_eps / zp) if fail_eps is not None else None,
                     "effect_for_fail": (zp * sigma / k_) if (fail_eps is None and (k_ := (fail_kappa if fail_kappa is not None else default_kappa(form))) > 0) else None}
    res["pass_reachable"] = probs["P_pass_true"] >= power and a["best_case_pass_fires"]
    res["fail_reachable"] = probs["P_fail_null"] >= power and a["best_case_fail_fires"]
    res["gate_met"] = res["pass_reachable"] and res["fail_reachable"]
    if fail_eps is None:
        k = fail_kappa if fail_kappa is not None else default_kappa(form)
        res["kappa_used"] = k
        res["kappa_in_N6_range"] = kappa_in_n6_range(k) if form == "causal" else None
        if form == "causal" and not res["kappa_in_N6_range"]:
            res["gate_met"] = False
            res["reason"] = "kappa_outside_N6_range (THEORY v1.4.7 Sec. 1 N6: 0 < kappa <= 1/2)"
    else:
        res["kappa_in_N6_range"] = None   # absolute margin: not N6's causal form (MV10 corollary 1)
    if rival_effect is not None:
        res["rival"] = rival_check(effect, rival_effect, sigma, alpha, power, fail_eps, fail_kappa, form)
    return res


def zero_events_bound(n, years, method="wilson", z=1.96):
    """Upper bound on a per-item yearly change rate when ZERO of n items changed over `years` (the best case for a
    'negligible drift' / moot / known-groups-low bound). wilson: the Wilson binomial upper limit z^2/(n+z^2) mapped to a
    rate by -ln(1-p)/years (WIKIDATA-BAND analyze.py); poisson: -ln(alpha_one_sided)/(n*years), alpha = 1 - Phi(z)."""
    if method == "wilson":
        return math.log(1 + z * z / n) / years
    return -math.log(1 - Phi(z)) / (n * years)


def zero_events_min_n(bound, years, method="wilson", z=1.96):
    """Smallest n at which zero observed changes can meet `bound` (the deterministic best-case attainability check)."""
    if method == "wilson":
        return math.floor(z * z / math.expm1(bound * years)) + 1
    return math.ceil(-math.log(1 - Phi(z)) / (bound * years))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("contrast")
    c.add_argument("--sigma", type=float, required=True)
    c.add_argument("--effect", type=float)
    c.add_argument("--scale", type=float, default=1.0, help="s*lam: adjustment share x input reliability (N6)")
    c.add_argument("--b", type=float); c.add_argument("--dlogx", type=float, nargs="+")
    g = c.add_mutually_exclusive_group(); g.add_argument("--fail-eps", type=float); g.add_argument("--fail-kappa", type=float)
    c.add_argument("--band-top", type=float); c.add_argument("--alpha", type=float, default=0.05)
    c.add_argument("--form", default="causal", choices=["causal", "optimality"])
    c.add_argument("--power", type=float, default=0.8); c.add_argument("--noise-df", type=int)
    c.add_argument("--sims", type=int, default=200_000); c.add_argument("--seed", type=int, default=1)
    c.add_argument("--rival-effect", type=float, help="predicted move of the named rival optimum for the SAME loss, in "
                   "the units of --effect after --scale (report-only discrimination line; PREREG-LOSS-LOCK proposal)")
    r = sp.add_parser("required")
    r.add_argument("--sigma", type=float, required=True); r.add_argument("--b", type=float, required=True)
    r.add_argument("--scale", type=float, default=1.0, help="s*lam: adjustment share x input reliability (N6)")
    r.add_argument("--fail-kappa", type=float, default=DEFAULT_KAPPA); r.add_argument("--alpha", type=float, default=0.05)
    r.add_argument("--power", type=float, default=0.8); r.add_argument("--per-contrast", type=float)
    k = sp.add_parser("zero-events")
    k.add_argument("--n", type=int, required=True); k.add_argument("--years", type=float, required=True)
    k.add_argument("--bound", type=float, required=True); k.add_argument("--method", default="wilson", choices=["wilson", "poisson"])
    k.add_argument("--z", type=float, default=1.96)
    a = ap.parse_args(argv)
    if a.cmd == "contrast":
        eff = a.scale * (a.effect if a.effect is not None else abs(a.b) * math.sqrt(sum(x * x for x in a.dlogx)))
        riv = None if a.rival_effect is None else a.scale * a.rival_effect
        res = gate(eff, a.sigma, a.alpha, a.power, a.fail_eps, a.fail_kappa, a.band_top, a.noise_df, a.sims, a.seed, a.form,
                   rival_effect=riv)
        ok = res["gate_met"]
    elif a.cmd == "required":
        bs = a.b * a.scale
        s = required_change(bs, a.sigma, a.alpha, a.power, a.fail_kappa)
        res = {"S_req_log": s, "factor": math.exp(s), "factor_at_50pct_pass": math.exp(z_two_sided(a.alpha) * a.sigma / abs(bs)),
               "kappa_used": a.fail_kappa, "kappa_in_N6_range": kappa_in_n6_range(a.fail_kappa)}
        if a.per_contrast:
            res["K_contrasts"] = required_contrasts(bs, a.sigma, a.per_contrast, a.alpha, a.power, a.fail_kappa)
        ok = True
    else:
        ub = zero_events_bound(a.n, a.years, a.method, a.z)
        res = {"bound_at_zero_events": ub, "attainable": ub <= a.bound, "n_min": zero_events_min_n(a.bound, a.years, a.method, a.z)}
        ok = res["attainable"]
    print(json.dumps(res, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
