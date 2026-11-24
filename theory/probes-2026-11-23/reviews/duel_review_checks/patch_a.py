"""Reviewer re-optimization of the classical N-state trackers per PREREG sec 4:
'Estimator theta_hat = 2 pi k/N + offset, offset optimized' (constant offset), plus a finer rate grid.
Exact bin arithmetic: error = U_bin + 2 pi t - 2 pi K/N - delta (+ common noise). Writes grid_patched.json."""
import json, numpy as np, sys
from multiprocessing import Pool
import duel_core as d
rows = json.load(open('../fresh/checks/grid_results.json'))
DEL = np.linspace(-np.pi, np.pi, 257)[:-1]
FAC = np.concatenate([[0.0], np.geomspace(0.02, 6, 40), [0.25,0.5,0.7,0.85,1.0,1.15,1.4,2.0,4.0]])
def stake_times(T): return np.unique(np.concatenate([np.linspace(0,T,4001), np.geomspace(1e-5*T,T,2000)]))
def tail_times(T, n=48): return np.unique(np.concatenate([[0.0], np.geomspace(1e-3*T,T,n), np.linspace(0,T,n)]))
def Lnoise_fn(N, v, k):
    mass = d.uniform_mix_density([0.0],[1.0],2*np.pi/N)
    mass = d.convolve_noise(mass, v, k)
    # tail prob as function of shift c: P(|wrap(c+X)|>pi/2), X~mass; = circular correlation of mass with TAILMASK
    F = np.fft.fft(mass); G = np.fft.fft(d.TAILMASK.astype(float))
    corr = np.real(np.fft.ifft(np.conj(F)*G))   # corr[j] = sum_i mass[i]*tail[i+j]
    return corr   # index j <-> shift c = 2 pi j / M
def eval_cfg(cfg):
    reg, T, s, k = cfg
    out = {}
    tt = tail_times(T); ts = stake_times(T)
    for N in [2,3,4,5,6,8,12,16,24,32,48,64]:
        rstar = 2*np.pi/np.sin(2*np.pi/N) if N>=3 else 2*np.pi*N
        Ls = [Lnoise_fn(N, s*t, k) for t in tt]
        g1 = d.noise_char(1, s*ts, k)
        res = []
        for f in FAC:
            r = f*rstar
            tails = np.zeros(len(DEL))
            for t, L in zip(tt, Ls):
                q = d.a_jump_dist(N, r, t) if r > 0 else np.eye(N)[0]
                cen = 2*np.pi*t - 2*np.pi*np.arange(N)/N
                c = (cen[:,None] - DEL[None,:])
                j = np.round((c % (2*np.pi))/(2*np.pi)*d.M).astype(int) % d.M
                tails = np.maximum(tails, (q[:,None]*L[j]).sum(0))
            z = np.exp(r*ts*(np.exp(-2j*np.pi/N)-1.0))*np.exp(2j*np.pi*ts)
            ch = np.sinc(1.0/N)*np.real(z[:,None]*np.exp(-1j*DEL[None,:]))*g1[:,None]
            stakes = 1 - np.trapezoid(ch, ts, axis=0)/(ts[-1]-ts[0])
            res.append((f, r, stakes, tails))
        out[N] = res
    return cfg, out
cfgs = sorted({(r['reg'], r['T'], r['s'], r['kobs']) for r in rows}, key=str)
with Pool(6) as p: allres = dict(p.map(eval_cfg, cfgs))
nch = 0; log = []
for row in rows:
    res = allres[(row['reg'], row['T'], row['s'], row['kobs'])][row['N']]; eps = row['eps']
    for name, sel in [('a1', lambda f: f == 0.0), ('a3', lambda f: f > 0.0)]:
        best = None; mintail = 9
        for f, r, st, tl in res:
            if not sel(f): continue
            ok = tl <= eps
            mintail = min(mintail, tl.min())
            if ok.any():
                i = np.argmin(np.where(ok, st, np.inf))
                if best is None or st[i] < best[2]: best = (f, r, float(st[i]), float(tl[i]), float(DEL[i]))
        old = row[name]
        new = dict(stake=best[2], tail=best[3], feas=True, r=best[1], delta=best[4]) if best else dict(stake=old['stake'], tail=float(mintail), feas=False)
        if new['feas'] != old['feas'] or (new['feas'] and new['stake'] < old['stake'] - 1e-9):
            nch += 1; log.append(f"{row['reg']} T={row['T']} s={row['s']} N={row['N']} eps={eps} {name}: feas {old['feas']}->{new['feas']} stake {old['stake']:.4f}->{new['stake']:.4f} delta={new.get('delta')} r/r*={new.get('r',0)/ (2*np.pi/np.sin(2*np.pi/row['N']) if row['N']>=3 else 4*np.pi):.3f}")
        row[name] = new
json.dump(rows, open('grid_patched.json','w'), indent=0, default=float)
print("\n".join(log)); print("changed entries:", nch)
