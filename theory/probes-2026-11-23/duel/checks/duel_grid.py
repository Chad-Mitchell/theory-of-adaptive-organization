"""Preregistered grid (PREREG.md sec 5-6). Writes grid_results.json and decisions.txt."""
import json, itertools, numpy as np
import duel_core as d

NS = [2,3,4,5,6,8,12,16,24,32,48,64]
LAMS = [0, 1e-4, 1e-3, 1e-2, 1e-1]
EPSS = [0.05, 1e-2, 1e-3]
TS = [0.25, 1, 10, 100, 1000]
SS = [0.001, 0.01]
TAUS = [1/8, 1, 8]
KOBS = 100.0
RFAC = [0.25, 0.5, 0.7, 0.85, 1.0, 1.15, 1.4, 2.0, 4.0]

def stake_times(T):
    t = np.unique(np.concatenate([np.linspace(0, T, 4001), np.geomspace(1e-5*T, T, 2000)]))
    return t
def tail_times(T, n=48):
    return np.unique(np.concatenate([[0.0], np.geomspace(1e-3*T, T, n), np.linspace(0, T, n)]))
def tavg(t, y):
    return np.trapezoid(y, t)/(t[-1]-t[0])

def configs():
    for T in TS: yield dict(reg='D', T=T, s=0.0, kobs=None)
    for T in TS:
        for s in SS: yield dict(reg='S1', T=T, s=s, kobs=None)
    for tau in TAUS:
        for s in SS: yield dict(reg='S2', T=tau, s=s, kobs=KOBS)

def a_eval(N, cfg, eps, r=None, ticks=False):
    T, s, k = cfg['T'], cfg['s'], cfg['kobs']
    ts = stake_times(T); g1 = d.noise_char(1, s*ts, k)
    if ticks:
        ch = d.a_char1(N, 0, ts, shift=d.tick_shift(N, ts))
    else:
        ch = d.a_char1(N, r, ts)
    stake = 1 - tavg(ts, ch*g1)
    tt = tail_times(T)
    tails = [d.a_tail_fourier(N, 0 if ticks else r, t, s*t, k, shift=(d.tick_shift(N, t) if ticks else None)) for t in tt]
    return stake, max(tails)

def b_eval(N, cfg, eps):
    T, s, k = cfg['T'], cfg['s'], cfg['kobs']
    R, tl, c = d.best_state(N, eps, s*T, k)
    if R is None:
        return None, tl, None
    tt = tail_times(T)
    tails = [d.b_tail(c, s*t, k) for t in tt]
    ts = stake_times(T); g1 = d.noise_char(1, s*ts, k)
    stake = 1 - R*tavg(ts, g1)
    return stake, max(tails), c

def run_cfg(cfg):
    rows = []
    for N in NS:
        # classical records do not depend on eps: evaluate once
        s1, t1 = a_eval(N, cfg, None, r=0.0)
        rstar = 2*np.pi/np.sin(2*np.pi/N) if N >= 3 else 2*np.pi*N
        allr = [(f*rstar,)+a_eval(N, cfg, None, r=f*rstar) for f in RFAC]
        s2, t2 = a_eval(N, cfg, None, ticks=True)
        for eps in EPSS:
            row = dict(cfg); row.update(N=N, eps=eps)
            sb, tb, c = b_eval(N, cfg, eps)
            row['b'] = dict(stake=sb, tail=tb, feas=bool(sb is not None and tb <= eps*(1+1e-6)))
            if c is not None:
                ths = np.linspace(0, 2*np.pi, 4*N+3, endpoint=False)
                vecs = []
                for th in ths:
                    psi = c*np.exp(-1j*np.arange(N)*th); rho = np.outer(psi, psi.conj())
                    vecs.append(np.concatenate([rho.real.ravel(), rho.imag.ravel()]))
                row['b']['K_used'] = int(np.linalg.matrix_rank(np.array(vecs), tol=1e-9))
            row['a1'] = dict(stake=s1, tail=t1, feas=bool(t1 <= eps))
            feas = [x for x in allr if x[2] <= eps]
            if feas:
                best = min(feas, key=lambda x: x[1]); row['a3'] = dict(r=best[0], stake=best[1], tail=best[2], feas=True)
            else:
                best = min(allr, key=lambda x: x[2]); row['a3'] = dict(r=best[0], stake=best[1], tail=best[2], feas=False)
            row['a2'] = dict(stake=s2, tail=t2, feas=bool(t2 <= eps))
            rows.append(row)
    print('done', cfg, flush=True)
    return rows

def main():
    from multiprocessing import Pool
    cfgs = list(configs())
    with Pool(6) as pool:
        out = pool.map(run_cfg, cfgs, chunksize=1)
    rows = [r for rs in out for r in rs]
    json.dump(rows, open('grid_results.json', 'w'), indent=0, default=float)

if __name__ == '__main__':
    main()
