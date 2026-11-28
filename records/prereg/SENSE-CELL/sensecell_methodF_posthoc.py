"""Method F (sensitivity, pre-specified in PREREG sec 2) and post-hoc sensitivity. nice 19.
Method F: eps0 read from Lan Fig 4a: Tar curve at the SAM x20% point (dW = 5.8 kT) sits at eps/eps0 ~ 0.03 (read by eye, range 0.02-0.04);
the text gives eps ~ 0.01 there, so eps0 = 0.01/0.03 = 0.33 (range 0.25-0.5). Fig 4a BP line slope read: ln(1e9)/28.5 kT = 0.73 (cf alpha from Keegstra a0 = 0.717)."""
import json, math
import numpy as np, scipy.io as sio
import sensecell_calc as C
rng = np.random.default_rng(20261118); B = 2000
d = sio.loadmat('data/FIG1_keegstra2017.mat', squeeze_me=True, struct_as_record=False)['FIG1'].analysis
a0 = np.asarray(d.a0, float); Pi = np.asarray(d.precision, float); ok = np.isfinite(a0) & np.isfinite(Pi); a0, Pi = a0[ok], Pi[ok]; n = len(a0)
idx = [rng.integers(0, n, n) for _ in range(B)]
def run(eps0_fixed):
    beta, tlo, thi = [], [], []
    for i in idx:
        al = C.alpha_from_a0(a0[i].mean()); e = abs(1 - Pi[i].mean())
        e0 = C.eps0_anchor(al) if eps0_fixed is None else eps0_fixed
        beta.append(C.beta_phys(e, e0, al))
        th = [C.theta_eff(x, e0) for x in (0.01, 0.05)]; tlo.append(min(th)); thi.append(max(th))
    b = np.array(beta); bl, bh = float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
    tl, th = float(np.percentile(tlo, 2.5)), float(np.percentile(thi, 97.5))
    return {"beta_ci": [bl, bh], "H2": C.verdict_band_upper(bl, bh, 10), "H3": C.verdict_band_upper(bl, bh, 1000),
            "theta_ci": [tl, th], "H1": C.verdict_band_upper(tl, th, 0.5)}
out = {"methodF": {str(e0): run(e0) for e0 in (0.25, 0.33, 0.5)}}
# post hoc: what eps_obs would be needed (Method A, point alpha 0.717): beta at literature accuracies and Keegstra median
al = C.alpha_from_a0(a0.mean()); e0 = C.eps0_anchor(al)
out["posthoc_A_beta_by_eps"] = {str(e): C.beta_phys(e, e0, al) for e in (0.01, 0.05, 0.1, 1 - float(np.median(Pi)), abs(1 - Pi.mean()))}
out["posthoc_eps_at_beta10_A"] = float(e0 * math.exp(-al * C.DG0 / 10))
out["posthoc_eps_at_beta10_F033"] = float(0.33 * math.exp(-al * C.DG0 / 10))
out["posthoc_alpha_from_Lan_fig4a_BP"] = math.log(1e9) / 28.5
json.dump(out, open('results_F_posthoc.json', 'w'), indent=1); print(json.dumps(out, indent=1))
