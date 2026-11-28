"""CAUSAL-POWER-GATE check against STAKES-SHIFT-CAISO (pick 15). Own code; reads only tests/STAKES_SHIFT_CAISO/results.json.
Run: nice -n 19 python3 reviews/night2/CAUSAL_POWER_GATE_checks/verify_caiso.py > reviews/night2/CAUSAL_POWER_GATE_checks/verify_caiso.out"""
import json, math, os, sys
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import power_gate as pg

R = json.load(open(os.path.join(ROOT, "tests", "STAKES_SHIFT_CAISO", "results.json")))
pairs = np.array(list(R["year_pairs"].values()))
s_yr = pairs.std(ddof=1); se_boot = R["primary"]["se_boot"]; se_tot = math.hypot(s_yr, se_boot)
dlw = R["stakes_clean"]["dlogw_2025_vs_2024"]["est"]; b = 1 / 3
Dp = -b * dlw; band = R["prediction"]["band"][1]
print(f"recomputed: s_yr {s_yr:.4f} (results {R['noise']['s_yr']:.4f}); se_tot {se_tot:.4f} ({R['noise']['se_tot']:.4f}); "
      f"D_pred {Dp:.4f} ({R['prediction']['D_pred']:.4f}); band top {band:.4f}; z*se_tot {1.96*se_tot:.4f}")

print("\n1) Pick 15 as locked (FAIL iff D + 1.96 se < 0.05; PASS iff D - 1.96 se > 0 and D <= band top)")
print(json.dumps(pg.analytic(Dp, se_tot, fail_eps=0.05, band_top=band), indent=1))
for nd, lab in ((None, "normal, sigma known"), (5, "normal, sigma_hat from 6 pairs (df 5)")):
    print(lab, json.dumps(pg.simulate(Dp, se_tot, fail_eps=0.05, band_top=band, noise_df=nd, sims=400_000, seed=11)))
print("resampled year-pair noise", json.dumps(pg.simulate(Dp, se_tot, fail_eps=0.05, band_top=band, sims=400_000, seed=12,
                                                       noise_draws=pairs)))

print("\n2) Needed input change, one contrast, b = 1/3, sigma = se_tot (pi = 0.8, alpha = 0.05)")
for k in (1.0, 0.5):
    S = pg.required_change(b, se_tot, kappa=k)
    print(f"   kappa {k}: |dlog w| >= {S:.3f} -> factor x{math.exp(S):.1f}")
print(f"   50% PASS point (D_pred = 1.96 se_tot, the item's '~7x'): x{math.exp(1.96*se_tot/b):.2f}; with s_yr only x{math.exp(1.96*s_yr/b):.2f}")
print(f"   absolute-eps FAIL (eps 0.05) needs sigma <= {0.05/2.8016:.4f}, i.e. {(se_tot/(0.05/2.8016))**2:.0f} independent contrasts' averaging")
print(f"   at the observed like-for-like change ({dlw:.3f}): P(PASS|true) = {pg.Phi(-b*dlw/se_tot - 1.96):.3f} without band")

print("\n3) Same gate with sigma estimated from 6 pairs (df 5): effect at which both rules reach 0.8 (bisection, sims)")
def both(eff, df):
    s = pg.simulate(eff, se_tot, fail_kappa=1.0, noise_df=df, sims=200_000, seed=13)
    return min(s["P_pass_true"], s["P_fail_null"])
lo, hi = 0.5, 3.0
for _ in range(30):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if both(mid, 5) < 0.8 else (lo, mid)
print(f"   effect {hi:.3f} (sigma known: {2.8016*se_tot:.3f}); |dlog w| {hi/b:.3f} -> x{math.exp(hi/b):.1f}")

print("\n4) STAKES-SHIFT-MULTIYEAR planning: K independent contrasts of the observed size, slope through origin")
for d in (abs(dlw), 0.25, 0.7):
    # kappa=1.0 explicit since v1.4.7 (tool default became 1/2) so this reproduces verify_caiso.out
    print(f"   |dlog w| per contrast {d:.2f}: K >= {pg.required_contrasts(b, se_tot, d, kappa=1.0)}  (s_yr-only sigma: K >= {pg.required_contrasts(b, s_yr, d, kappa=1.0)})")
