"""C2: theory kernel (own null-space kriging), direct S(21), like-with-like W21 from the binned estimator on simulated
planned-n data (100 reps) and a long noiseless-tracker sim; dW21/dalpha; consistent free-noise prediction; bias under
independent AR(1) tracker noise."""
import json, math, sys, numpy as np, rlib
A, LQ, LS = 1.2587444912685188, -1.8115698083116092, -0.9004691544466353
AF, LQF, LSF = 1.1902, -1.5307, -30.25          # in-band free-noise fit (noise at the boundary, ~0)
N_PLAN, BURN, WIN = 9276, 2000, 2000
out = {}
def krn(a, lq, ls, Lw): return rlib.kernel(a, math.exp(lq), math.exp(ls), Lw=Lw)
for lab, (a, lq, ls) in {'locked': (A, LQ, LS), 'free_consistent': (AF, LQF, LSF), 'free_alpha_only': (AF, LQ, LS)}.items():
    w504 = krn(a, lq, ls, 504); w2000 = krn(a, lq, ls, 2000)
    out[f'S21_direct_504_{lab}'] = rlib.survival(w504); out[f'S21_direct_2000_{lab}'] = rlib.survival(w2000)
    out[f'w0_{lab}'] = float(w2000[0])
print({k: round(v, 4) for k, v in out.items()}, flush=True)

def planned(a, lq, ls, reps, seed, n=N_PLAN, r=0.0, phi=0.95):
    w = krn(a, lq, ls, WIN); rng = np.random.default_rng(seed); vals = []
    for _ in range(reps):
        y = rlib.sim_y(n + BURN, a, math.exp(lq), math.exp(ls), rng)
        f = rlib.apply_kernel(y, w)[BURN:]; yy = y[BURN:]
        if r > 0:
            e = np.empty(n); sd = r * np.nanstd(f); e[0] = rng.normal(0, sd)
            inn = rng.normal(0, sd * math.sqrt(1 - phi ** 2), n)
            for t in range(1, n): e[t] = phi * e[t - 1] + inn[t]
            f = f + e
        vals.append(rlib.fit_w21(-3 + f, yy)['W21'])
    v = np.array(vals); return {'mean': v.mean(), 'sd': v.std(ddof=1), 'se_mean': v.std(ddof=1) / math.sqrt(reps)}
out['planned_locked'] = planned(A, LQ, LS, 100, 101); print('planned_locked', out['planned_locked'], flush=True)
out['planned_a+0.1'] = planned(A + 0.1, LQ, LS, 100, 102); out['planned_a-0.1'] = planned(A - 0.1, LQ, LS, 100, 103)
out['dW21_dalpha'] = (out['planned_a+0.1']['mean'] - out['planned_a-0.1']['mean']) / 0.2
print('dW/da', out['dW21_dalpha'], flush=True)
out['planned_lq+0.2'] = planned(A, LQ + 0.2, LS, 100, 104); out['planned_ls+0.2'] = planned(A, LQ, LS + 0.2, 100, 105)
out['planned_free_consistent'] = planned(AF, LQF, LSF, 100, 106)
out['planned_free_alpha_only'] = planned(AF, LQ, LS, 100, 107)
print('free', out['planned_free_consistent'], out['planned_free_alpha_only'], flush=True)
out['planned_locked_r0.45'] = planned(A, LQ, LS, 60, 108, r=0.45)
out['long_200k'] = planned(A, LQ, LS, 1, 109, n=200000)
json.dump(out, open('c2.json', 'w'), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
