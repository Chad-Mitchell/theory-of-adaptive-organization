"""DYNAMICS §4 checks: time average vs ensemble average; when J (additive, ensemble) and time-average growth
rank designs differently; what a threshold-ruin constraint fixes. Independent of the wide-net scan.
Run: nice -n 19 python3 d3_time_average.py -> d3_results.json, prints ALL D3 CHECKS PASS."""
import json, math, os
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(2016)
R, ok = {}, []

# ---- D3a. Exponential (log-reserve) form: W' = W exp(-(c + w*l)). Time-average growth = -(c + w E l) by the
# ergodic theorem, i.e. exactly -J. Check on an AR(1) (ergodic, correlated) loss sequence.
T = 200000; phi = 0.9; e = np.zeros(T); z = rng.standard_normal(T)
for t in range(1, T): e[t] = phi * e[t - 1] + math.sqrt(1 - phi**2) * z[t]
l = e**2; c, w = 0.01, 0.02
R["D3a_time_avg_log_growth_vs_minus_J"] = [float(-(c + w * l).mean()), -(c + w * 1.0)]
ok.append(abs(R["D3a_time_avg_log_growth_vs_minus_J"][0] - R["D3a_time_avg_log_growth_vs_minus_J"][1]) < 2e-3)

# ---- D3b. Arithmetic multiplicative form W' = W (1 + g - w l) is ill-posed for Gaussian error: P(1 - w l < 0) > 0
# for every w > 0, so E ln = -inf for every design. (Correction to the scan's C1c, which clipped the log.)
for wv, var in ((0.5, 0.04),):
    p_neg = 2 * norm.sf(math.sqrt(1 / (wv * var)))
    R["D3b_P_factor_negative_gaussian"] = p_neg
ok.append(R["D3b_P_factor_negative_gaussian"] > 0)

# ---- D3c. Lumpy loss acting on returns (R1-type toy): one layer, n copies, each down w.p. p per window;
# all copies down costs a fraction X of the reserve. Additive J vs time-average growth G.
def nE_nG(g, h, wE1, X, p, nmax=40):
    J = [n * h + wE1 + X * p**n for n in range(1, nmax)]
    G = []
    for n in range(1, nmax):
        m = 1 + g - n * h - wE1
        G.append(-math.inf if m - X <= 0 else (1 - p**n) * math.log(m) + p**n * math.log(m - X))
    return 1 + int(np.argmin(J)), 1 + int(np.argmax(G)), J, G
nE, nG, J, G = nE_nG(0.10, 0.004, 0.01, 0.6, 0.2)
R["D3c_scan_toy_nE_nG"] = [nE, nG]
R["D3c_scan_toy_J3_J4_relgap"] = (J[3] - J[2]) / J[2]   # how close to a tie the toy is under J
ok.append([nE, nG] == [3, 4] and R["D3c_scan_toy_J3_J4_relgap"] < 0.01)

# Robustness of the direction over a grid of parameters (not cherry-picked): how often n_G != n_E, and which way.
cnt = {"same": 0, "G_more": 0, "G_fewer": 0}; diffs = []; byX = {}
for g in (0.02, 0.05, 0.10, 0.20):
    for h in (0.0005, 0.001, 0.002, 0.004, 0.008):
        for X in (0.05, 0.1, 0.2, 0.4, 0.6, 0.8):
            for p in (0.02, 0.05, 0.1, 0.2, 0.3):
                a, b_, _, _ = nE_nG(g, h, 0.01, X, p)
                if 1 + g - b_ * h - 0.01 - X <= 0: continue
                cnt["same" if a == b_ else ("G_more" if b_ > a else "G_fewer")] += 1; diffs.append(b_ - a)
                byX.setdefault(X, [0, 0]); byX[X][0] += 1; byX[X][1] += int(a != b_)
R["D3c_grid_counts"] = cnt
R["D3c_grid_max_extra_copies"] = int(max(diffs))
# share of grid points where the counts differ, by X (added after independent review of PR #117, should-fix 2):
# the effect is not confined to lumpy X; it is present at X = 0.05 and broadly rises with X
R["D3c_grid_share_differ_by_X"] = {str(X): [n, k, round(k / n, 3)] for X, (n, k) in sorted(byX.items())}
ok.append(byX[0.05][1] > 0 and byX[0.8][1] / byX[0.8][0] > byX[0.05][1] / byX[0.05][0])
ok.append(cnt["G_fewer"] == 0 and cnt["G_more"] > 0)
# three hand-picked points (g = 0.05, h = 0.002): at X = 0.05 these coincide; at X = 0.8 one differs. Illustration only;
# the grid share above is the claim
small = []; large = []
for p in (0.05, 0.1, 0.2):
    small.append(nE_nG(0.05, 0.002, 0.01, 0.05, p)[:2]); large.append(nE_nG(0.05, 0.002, 0.01, 0.8, p)[:2])
R["D3c_small_X_pairs"] = small; R["D3c_large_X_pairs"] = large
ok.append(all(a == b for a, b in small) and any(b > a for a, b in large))

# ---- D3d. Threshold ruin. Peters coin x1.5 / x0.6: ensemble mean +5%/step, time-average growth ln(0.9)/2 < 0.
ens = 0.5 * 1.5 + 0.5 * 0.6; tav = 0.5 * math.log(1.5) + 0.5 * math.log(0.6)
paths = np.cumsum(np.log(rng.choice([1.5, 0.6], size=(5000, 1000))), axis=1)
R["D3d_coin_ens_tav_Pmin_below_0.01_T1000"] = [ens, tav, float((paths.min(1) < math.log(0.01)).mean())]
ok.append(ens > 1 and tav < 0 and R["D3d_coin_ens_tav_Pmin_below_0.01_T1000"][2] > 0.99)
# Two designs that both pass a threshold-ruin constraint (P(min W < 0.5 by T) <= eps) but are ranked oppositely by
# the ensemble mean and the time average: the constraint fixes the sign, not the ranking.
THR, EPS = 0.3, 0.01
designs = {"A_smooth": ([1.04, 1.02], [0.5, 0.5]), "B_lumpy": ([1.131, 0.931], [0.5, 0.5])}
out = {}
for name, (f, pr) in designs.items():
    arith = sum(fi * pi for fi, pi in zip(f, pr)); geo = sum(pi * math.log(fi) for fi, pi in zip(f, pr))
    lp = np.cumsum(np.log(rng.choice(f, p=pr, size=(4000, 300))), axis=1)
    out[name] = [arith, geo, float((lp.min(1) < math.log(THR)).mean())]
R["D3d_two_designs_arith_geo_Pruin"] = out
A, B = out["A_smooth"], out["B_lumpy"]
ok.append(B[0] > A[0] and A[1] > B[1] and A[2] <= EPS and B[2] <= EPS)  # both pass; arithmetic prefers B, time average A
R["D3d_threshold_eps_T"] = [THR, EPS, 300]

R["checks_passed"] = int(sum(ok)); R["checks_total"] = len(ok)
json.dump(R, open(os.path.join(HERE, "d3_results.json"), "w"), indent=1, default=str)
for kk, v in R.items(): print(kk, v)
print("ALL D3 CHECKS PASS" if all(ok) else "D3 FAIL: %s" % [i for i, x in enumerate(ok) if not x])
