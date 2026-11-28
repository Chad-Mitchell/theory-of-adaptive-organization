"""SENSE-CELL-REFEREE exploratory matched re-scoring (post hoc; outcomes known). nice 19.
Uses the locked formulas in prereg/SENSE-CELL/sensecell_calc.py. Premise ranges are stated in PRECOMP.md."""
import sys, json, math
sys.path.insert(0, 'prereg/SENSE-CELL')
import numpy as np, scipy.io as sio
import sensecell_calc as C
rng = np.random.default_rng(20261118)
N = 200000
DG0 = 29.0
d = sio.loadmat('prereg/SENSE-CELL/data/FIG1_keegstra2017.mat', squeeze_me=True, struct_as_record=False)['FIG1'].analysis
a0 = np.asarray(d.a0, float); P = np.asarray(d.precision, float); n = len(a0)
def beta(eps, eps0, alpha):
    w = np.log(eps0 / eps) / alpha
    return np.where(w > 0, DG0 / np.where(w > 0, w, 1), np.inf)
eps0 = np.exp(rng.uniform(math.log(0.18), math.log(0.70), N))
alpha = rng.uniform(0.70, 0.75, N)
def rep(name, eps):
    b = beta(eps, eps0, alpha)
    fin = np.isfinite(b)
    lo, med, hi = np.percentile(b, [2.5, 50, 97.5])
    return {"reading": name, "beta_2.5": float(lo), "beta_50": float(med), "beta_97.5": float(hi), "frac_inf": float(1 - fin.mean()),
            "label_mirrored_rule_edge10": C.verdict_band_upper(lo, hi, 10)}
out = []
# R1 Lan Fig 5c ~95%: eps uniform [0.03, 0.08]
out.append(rep("R1 Lan own WT whole-cell FRET ~95% (eps U[0.03,0.08])", rng.uniform(0.03, 0.08, N)))
out.append(rep("R1b same, eps fixed 0.05", np.full(N, 0.05)))
# R2 Tar text ~99%: eps U[0.005, 0.02]
out.append(rep("R2 Tar anchor ~99% (eps U[0.005,0.02]); circular", rng.uniform(0.005, 0.02, N)))
# R3 Keegstra ratio of means with bootstrap
e = []
for _ in range(N // 20):
    i = rng.integers(0, n, n); e.append(1 - (P[i] * a0[i]).sum() / a0[i].sum())
e = np.array(e); idx = rng.integers(0, len(e), N)
out.append(rep("R3 Keegstra 500 uM mixed array, ratio of means (eps boot)", e[idx]))
# R4 Neumann-like low-stimulus eps U[0.0,0.1]: beta <1 means eps below what BP line allows at DG0 (flag)
epsr4 = rng.uniform(0.005, 0.10, N)
out.append(rep("R4 Neumann low stimulus eps U[0.005,0.10] (unresolved)", epsr4))
# threshold: eps at which beta=10 and 1, by premise draw
def eps_at_beta(bt):
    return eps0 * np.exp(-alpha * DG0 / bt)
out.append({"eps_at_beta10_pctl_2.5_50_97.5": [float(x) for x in np.percentile(eps_at_beta(10), [2.5, 50, 97.5])],
            "eps_at_beta1_pctl": [float(x) for x in np.percentile(eps_at_beta(1), [2.5, 50, 97.5])]})
# also: observed-eps-over-eps0 for Keegstra (is it above the equilibrium error?)
out.append({"frac_draws_where_Keegstra_eps_ge_eps0": float(np.mean(e[idx] >= eps0)), "keegstra_eps_ratio_of_means_point": float(1 - (P * a0).sum() / a0.sum())})
# point values for the table
tab = {}
for e0 in (0.18, 0.25, 0.33, 0.5, 0.64, 0.70):
    tab[str(e0)] = {str(x): float(beta(np.array(x), np.array(e0), 0.727)) for x in (0.01, 0.02, 0.05, 0.08, 0.10, 0.21)}
out.append({"point_beta_table_alpha0.727": tab})
json.dump(out, open('reviews/night2/SENSE_CELL_REVIEW_checks/referee_results.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
