"""Post-lock independent numerical check (own code, no import of common.py / analysis.py).
C1 D re-computed with a stacked interaction regression F = a_c + b_c x_{t-1} (condition dummies) and cluster-robust
(participant) covariance -> slope of b_c on rho with delta-method SE. C2 b_opt with a recursive-least-squares learner
(different algorithm from lstsq refits). C3 jackknife-by-participant SE of D."""
import csv, json, math
from collections import defaultdict
import numpy as np
rows = defaultdict(list)
with open("data/exp1_detail.csv") as f:
    for r in csv.DictReader(f):
        rows[r["assignmentid"]].append((int(r["round"]), float(r["actual"]), r["predictiona_value"], round(float(r["rho"]), 1)))
subj = []
for k, v in rows.items():
    v.sort(); x = np.array([a[1] for a in v]); rd = np.array([a[0] for a in v])
    F = np.array([float(a[2]) if a[2] not in ("", ".") else np.nan for a in v]); subj.append((k, v[0][3], rd, x, F))
rhos = sorted({s[1] for s in subj}); C = len(rhos)
def ip_by_cond(sl, which):
    out = {}
    for rho in rhos:
        X, Y = [], []
        for (k, r0, rd, x, F) in sl:
            if r0 != rho: continue
            yy = F if which == "F" else which[k]
            for i in range(1, len(x)):
                if rd[i] >= 1 and not np.isnan(yy[i]): X.append(x[i - 1]); Y.append(yy[i])
        X = np.array(X); Y = np.array(Y); Xc = X - X.mean()
        out[rho] = float((Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum())
    return out
def slope(ip):
    r = np.array(rhos); v = np.array([ip[q] for q in rhos]); rc = r - r.mean(); return float((rc * v).sum() / (rc ** 2).sum())
# C1 stacked regression with cluster-robust covariance
Xs, Ys, G = [], [], []
for gi, (k, r0, rd, x, F) in enumerate(subj):
    c = rhos.index(r0)
    for i in range(1, len(x)):
        if rd[i] >= 1 and not np.isnan(F[i]):
            z = np.zeros(2 * C); z[c] = 1; z[C + c] = x[i - 1]; Xs.append(z); Ys.append(F[i]); G.append(gi)
Xs = np.array(Xs); Ys = np.array(Ys); G = np.array(G)
XtX_inv = np.linalg.inv(Xs.T @ Xs); beta = XtX_inv @ Xs.T @ Ys; e = Ys - Xs @ beta
meat = np.zeros((2 * C, 2 * C))
for g in np.unique(G):
    s = Xs[G == g].T @ e[G == g]; meat += np.outer(s, s)
V = XtX_inv @ meat @ XtX_inv
r = np.array(rhos); w = (r - r.mean()) / ((r - r.mean()) ** 2).sum()
L = np.concatenate([np.zeros(C), w]); D1 = float(L @ beta); se1 = float(math.sqrt(L @ V @ L))
# C2 RLS learner
fl = {}
for (k, r0, rd, x, F) in subj:
    f = np.full(len(x), np.nan); P = np.eye(2) * 1e8; th = np.zeros(2)
    for i in range(1, len(x)):
        if rd[i] >= 1:
            f[i] = th[0] + th[1] * x[i - 1]
        # after observing x_i, update with pair (x_{i-1}, x_i) -> used for forecasts from round i+1 on
        phi = np.array([1.0, x[i - 1]]); K = P @ phi / (1 + phi @ P @ phi); th = th + K * (x[i] - phi @ th); P = P - np.outer(K, phi @ P)
    fl[k] = f
bopt2 = slope(ip_by_cond(subj, fl))
# C3 jackknife
D0 = slope(ip_by_cond(subj, "F")); jk = []
for j in range(len(subj)):
    jk.append(slope(ip_by_cond(subj[:j] + subj[j + 1:], "F")))
jk = np.array(jk); n = len(jk); sej = float(math.sqrt((n - 1) / n * ((jk - jk.mean()) ** 2).sum()))
out = {"C1_stacked_D": round(D1, 4), "C1_cluster_se": round(se1, 4), "C2_b_opt_RLS": round(bopt2, 4),
       "C3_D": round(D0, 4), "C3_jackknife_se": round(sej, 4),
       "verdict_C1": ("FAIL" if D1 + 1.96 * se1 < 0.5 * bopt2 else "PASS" if D1 - 1.96 * se1 > 0 else "INCONCLUSIVE"),
       "verdict_C3": ("FAIL" if D0 + 1.96 * sej < 0.5 * bopt2 else "PASS" if D0 - 1.96 * sej > 0 else "INCONCLUSIVE")}
json.dump(out, open("independent_check.json", "w"), indent=1); print(json.dumps(out, indent=1))
