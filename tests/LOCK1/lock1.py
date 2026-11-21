"""LOCK1 runner. Preregistration: tests/LOCK1/PREREG.md (sha256 in PREREG.sha256; locked before this file existed).
Run: nice -n 19 python3 tests/LOCK1/lock1.py   -> tests/LOCK1/lock1.json, printed table."""
import sys, os, math, json, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'core', 'keystone_checks'))
sys.path.insert(0, os.path.join(ROOT, 'theory', 'layers_checks'))
import resonant_layers as rl
from rhythm_rule import osc_world
from stores import mse_given_b, E_K, scalefree_world

lock = open(os.path.join(HERE, 'PREREG.sha256')).read().split()[0]
assert hashlib.sha256(open(os.path.join(HERE, 'PREREG.md'), 'rb').read()).hexdigest() == lock, "prereg changed"
out = {}
N = 0.01

# ---------- (a) rational-ratio rhythm worlds ----------
A = {}
for rho in [2.0, 3.0, 1.5]:
    om = [1.0, rho]
    a, v, _ = osc_world(om, [0.05, 0.05], [0.5, 0.5], N)
    d = rl.optimize_design(a, v, N, 0, 2, seed=1)
    lo = sorted(abs(r[1]) for r in d['resonants'])
    errs = [abs(lo[0] - 1.0), abs(lo[1] - rho) / rho]
    ratio_err = abs(lo[1] / lo[0] - rho) / rho
    A[str(rho)] = dict(layer_omegas=lo, errs=errs, ratio_err=ratio_err, E=d['E'])
    print(f"(a) rho={rho}: layer omegas {np.round(lo,4)}, rel errs {np.round(errs,4)}, ratio err {ratio_err:.4f}")
out['A'] = A
A1 = all(max(x['errs']) < 0.05 for x in A.values()); A2 = all(x['ratio_err'] < 0.05 for x in A.values())

# ---------- (b) phase layers, no world rhythm ----------
def red(r, Kc, D=1e-4, seed=0, n=4000, burn=500):
    rng = np.random.default_rng(seed)
    Om = r % 1.0
    th = 0.0; s = math.sqrt(2 * D)
    xs = np.empty(n)
    noise = rng.normal(0, 1, n + burn)
    for i in range(n + burn):
        th = th + Om - Kc / (2 * math.pi) * math.sin(2 * math.pi * th) + s * noise[i]
        if i >= burn:
            xs[i - burn] = th
    return max(abs(np.mean(np.exp(2j * math.pi * q * xs))) for q in range(1, 7))

def dist_rational(r, qmax=4):
    return min(abs(r - round(r * q) / q) for q in range(1, qmax + 1))
def dioph(r, qmax=20):
    return min(q * abs(q * r - round(q * r)) for q in range(1, qmax + 1))

rng = np.random.default_rng(20261121)
r0s = rng.uniform(3, 4, 150)
B = {}
for Kc in [0.3, 0.6, 0.9]:
    # Red(r) depends on r only through frac(r): tabulate once on a fine grid of frac values
    fr = np.arange(0, 1, 1e-3)
    R = np.array([red(f, Kc, seed=int(1e4 * f)) for f in fr])
    opt = []
    for r0 in r0s:
        rs = np.arange(0.7 * r0, 1.4 * r0, 1e-3)
        Rr = np.interp(rs % 1.0, fr, R, period=1.0)
        J = (np.log(rs) - math.log(r0)) ** 2 / (2 * 0.1 ** 2) + 1.0 * Rr
        opt.append(rs[np.argmin(J)])
    opt = np.array(opt)
    dr_opt = np.mean([dist_rational(x) for x in opt]); dr_0 = np.mean([dist_rational(x) for x in r0s])
    dp_opt = np.mean([dioph(x) for x in opt]); dp_0 = np.mean([dioph(x) for x in r0s])
    f = opt % 1.0
    gold = np.mean((np.abs(f - 0.381966) < 0.02) | (np.abs(f - 0.618034) < 0.02))
    B[str(Kc)] = dict(dist_rat_opt=dr_opt, dist_rat_r0=dr_0, dioph_opt=dp_opt, dioph_r0=dp_0, golden_share=gold,
                      mean_shift=float(np.mean(np.abs(opt - r0s))),
                      red_locked_share=float(np.mean(R > 0.5)))
    print(f"(b) Kc={Kc}: dist to p/q(q<=4) opt {dr_opt:.4f} vs r0 {dr_0:.4f}; Diophantine opt {dp_opt:.4f} vs r0 {dp_0:.4f}; "
          f"golden share {gold:.3f} (uniform 0.08); mean |shift| {np.mean(np.abs(opt-r0s)):.3f}; share of frac grid with Red>0.5 {np.mean(R>0.5):.3f}")
out['B'] = B
B1 = all(x['dist_rat_opt'] > x['dist_rat_r0'] for x in B.values())
B2 = all(x['dioph_opt'] >= 1.10 * x['dioph_r0'] for x in B.values())
B3 = all(x['golden_share'] >= 0.24 for x in B.values())

# B4: linear class, fresh scan
B4v = {}
for alpha in [1.0, 1.4]:
    a, v = scalefree_world(alpha, 1e4, per_decade=6)
    e2, lb2 = E_K(a, v, N, 2, starts=10); gm = lb2.mean()
    rs = np.linspace(1.2, 60, 3000)
    es = np.array([mse_given_b(a, v, np.exp([gm - math.log(r) / 2, gm + math.log(r) / 2]), N)[0] for r in rs])
    d2 = np.abs(np.diff(es, 2)); near = np.zeros(len(rs) - 2, bool)
    for s_ in [1.5, 2, 2.5, 3, 4, 5, 6]:
        near |= np.abs(rs[1:-1] - s_) < 0.02
    B4v[str(alpha)] = float(d2[near].mean() / d2[~near & (rs[1:-1] < 7)].mean())
    print(f"(b-linear) alpha={alpha}: roughness near p/q / elsewhere = {B4v[str(alpha)]:.3f}")
out['B4'] = B4v
B4 = all(0.8 <= x <= 1.25 for x in B4v.values())

# ---------- (c) mixed world ----------
a1, v1, _ = osc_world([1.0], [0.05], [0.5], N)
a = np.concatenate([a1, np.array([0.01, 0.1], complex)]); v = np.concatenate([v1, np.array([0.25, 0.25], complex)])
d = rl.optimize_design(a, v, N, 1, 1, seed=2)
om_res = abs(d['resonants'][0][1])
print(f"(c) mixed: resonant layer omega {om_res:.4f}; first-order rate {d['first']}")
out['D1'] = dict(omega=om_res, first=d['first'], E=d['E'])
D1 = abs(om_res - 1.0) < 0.05
D2 = B['0.6']['dist_rat_opt'] > B['0.6']['dist_rat_r0']

verdict = dict(A1=A1, A2=A2, B1=B1, B2=B2, B3=B3, B4=B4, D1=D1, D2=D2)
out['verdict'] = {k: ('PASS' if v_ else 'FAIL') for k, v_ in verdict.items()}
print(out['verdict'])
json.dump(out, open(os.path.join(HERE, 'lock1.json'), 'w'), indent=1, default=float)
