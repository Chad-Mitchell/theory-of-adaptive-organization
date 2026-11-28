"""C3: does the noise treatment or the band choice drive the prediction? Refit (alpha, log q) in band at fixed noise
levels along the profile, and the full-band fit; planned-n W21 for each (60 reps, common seeds). Joint-covariance
sigma_pred for the locked fit."""
import json, math, numpy as np, rlib
y, z, _ = rlib.load(); B = 2 * math.pi / 21
N_PLAN, BURN, WIN = 9276, 2000, 2000
def planned(a, lq, ls, reps, seed):
    w = rlib.kernel(a, math.exp(lq), math.exp(ls), Lw=WIN); rng = np.random.default_rng(seed); v = []
    for _ in range(reps):
        yy = rlib.sim_y(N_PLAN + BURN, a, math.exp(lq), math.exp(ls), rng)
        f = rlib.apply_kernel(yy, w)[BURN:]; v.append(rlib.fit_w21(f, yy[BURN:])['W21'])
    v = np.array(v); return float(v.mean()), float(v.std(ddof=1) / math.sqrt(reps))
out = {'profile': {}}
for ls in [-30.0, -3.0, -1.5, -1.2, -1.08, -0.94, -0.9005, -0.7, -0.5]:
    f = rlib.whittle(y, wmax=B, fix_logs2=ls)
    m, se = planned(f['alpha'], f['logq'], ls, 60, 7)
    out['profile'][f'{ls}'] = {'alpha': f['alpha'], 'logq': f['logq'], 'nll': f['nll'], 'W21_planned': m, 'se': se}
    print(ls, round(f['alpha'], 4), round(f['logq'], 4), round(f['nll'], 3), round(m, 4), flush=True)
fb = rlib.whittle(y)
out['fullband'] = {'alpha': fb['alpha'], 'logq': fb['logq'], 'logs2': fb['logs2']}
out['fullband']['W21_planned'], _ = planned(fb['alpha'], fb['logq'], fb['logs2'], 60, 7)
print('fullband', out['fullband'], flush=True)
# joint covariance of (alpha, logq) at fixed noise from Whittle Fisher information, plus noise uncertainty via the profile
w, I = rlib.pgram_diff(y); k = w <= B; w = w[k]
p = np.array([1.2587444912685188, -1.8115698083116092]); ls0 = -0.9004691544466353; h = 1e-5; g = []
for i in range(2):
    e = np.zeros(2); e[i] = h
    g.append((np.log(rlib.f_model(w, *(p + e), ls0)) - np.log(rlib.f_model(w, *(p - e), ls0))) / (2 * h))
g = np.array(g); C = np.linalg.inv(g @ g.T)
out['cov_alpha_logq'] = C.tolist(); out['corr_alpha_logq'] = float(C[0, 1] / math.sqrt(C[0, 0] * C[1, 1]))
json.dump(out, open('c3.json', 'w'), indent=1, default=float); print(json.dumps({k: out[k] for k in ('cov_alpha_logq', 'corr_alpha_logq')}))
