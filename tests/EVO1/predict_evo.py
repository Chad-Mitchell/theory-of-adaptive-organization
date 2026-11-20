#!/usr/bin/env python3
"""EVO1 J-prediction script: the theory's predicted design for each designed world, computed ONLY from the repository's
closed forms and optimizers (theory/layers_checks/stores.py, figures/face_hybrid.py, theory/STORE_NOISE.md Model S+).
It never runs the evolution simulator and never reads its output.  Run: nice -n 19 python3 predict_evo.py
Writes PREDICTIONS_EVO.json.  Time unit: one simulator step (dt = 1); sensing-noise density N = per-step noise variance."""
import os, sys, json, itertools
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'figures')); sys.path.insert(0, os.path.join(ROOT, 'theory', 'layers_checks'))
from face_hybrid import mse_fast, best_fast, _F0, _rates          # repo optimizer (B.11 / CT35-36 class)
import stores                                                      # repo Model S closed forms (CT21)

W = json.load(open(os.path.join(HERE, 'worlds.json')))

# ---------------------------------------------------------------- Model S / B.11 class (OU worlds, n units, common noise)
def J_ou(p, bl, bc):
    """Theory cost per step for a group: upkeep + speed price + stake x per-unit MSE (optimal static read-out)."""
    n = p.get('n', 1)
    e = mse_fast(p['a'], p['v'], p['N'], n, np.asarray(p['rho'], float), p.get('lead', 0.0), bl, bc, p.get('Nc', 0.0))
    up = n * p['h'] * len(bl) + p.get('hc', p['h']) * len(bc) + p.get('h1', 0.0) * (n * np.sum(bl) + np.sum(bc))
    return up + n * p['w'] * e, e

def best_design(p, kl, kc, starts=16, seed=0):
    """Minimize J over rates for a fixed store count (local kl, shared kc); multistart Nelder-Mead in log rate,
    the same parametrisation and safeguards as face_hybrid.best_fast, plus the speed price."""
    if kl + kc == 0: return J_ou(p, [], [])[0], [], []
    a = np.asarray(p['a'], float); rng = np.random.default_rng(seed)
    lo, hi = np.log(a.min()) - 3, np.log(a.max()) + 5
    f = lambda x: J_ou(p, _rates(x[:kl]), _rates(x[kl:]))[0]
    inits = [np.concatenate([np.linspace(lo + 2, hi - 2, kl), np.linspace(lo + 1, hi - 3, kc)])]
    inits += [rng.uniform(lo, hi, kl + kc) for _ in range(starts)]
    best = (np.inf, None)
    for x0 in inits:
        with np.errstate(all='ignore'):
            r = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-13, maxiter=4000 * (kl + kc)))
        if r.fun < best[0]: best = (r.fun, r.x)
    x = best[1]
    return best[0], list(_rates(x[:kl])), list(_rates(x[kl:]))

def hessian_logtau(fun, x, h=1e-3):
    """Diagonal second derivatives of J in log rate (= log tau up to sign)."""
    x = np.asarray(x, float); out = []
    f0 = fun(x)
    for i in range(len(x)):
        e = np.zeros_like(x); e[i] = h
        out.append((fun(x + e) - 2 * f0 + fun(x - e)) / h ** 2)
    return out

# ---------------------------------------------------------------- random walk (L1 closed form, Kalman-Bucy)
def rw_prediction(p):
    q, N, w, h, h1 = p['q'], p['N'], p['w'], p['h'], p.get('h1', 0.0)
    # one store on a random walk read in white noise: MSE(b) = q/(2b) + N b/2 (exact, continuous time); K*=1 by L1.
    Jb = lambda b: h + h1 * b + w * (q / (2 * b) + N * b / 2)
    bs = np.exp(np.linspace(np.log(1e-6), 0, 200001)); j = Jb(bs); i = int(np.argmin(j))
    b = float(bs[i]); Jst = float(j[i])
    H = (Jb(b * np.exp(1e-3)) - 2 * Jst + Jb(b * np.exp(-1e-3))) / 1e-6
    # two stores on a random walk: by L1 E_2 = E_1 (the Kalman-Bucy filter of a first-order state is one store), so
    # J(K=2) = J(K=1) + h at best; K=0 has unbounded error. Checked numerically below with a nearly-integrating OU (a -> 0).
    a_small = 1e-7; v_small = q / (2 * a_small)
    e1 = stores.E_K([a_small], [v_small], N, 1)[0]; e2 = stores.E_K([a_small], [v_small], N, 2)[0]
    return dict(K=1, b=[b], lam_tau=None, J_star=Jst, H_logb=[float(H)], E=float(q / (2 * b) + N * b / 2),
                check_E1_vs_E2_nearRW=dict(E1=float(e1), E2=float(e2), rel=float((e1 - e2) / e1)),
                rivals=dict(more_layers_K4=Jst + 3 * h, set_at=('undefined for a random walk (tau = infinity): the slowest '
                            'store allowed'), none=float('inf')))

# ---------------------------------------------------------------- Model S+ (store noise, STORE_NOISE.md E1)
def sp_J(p, taus):
    lam, s2, V0, t0, s, w, h = p['lam'], p['sigma2'], p['V0'], p['tau0'], p['s'], p['w'], p['h']
    taus = np.asarray(taus, float); b = 1 / taus
    C = s2 * _F0(lam, b[:, None], b[None, :]) + np.diag(V0 * (t0 / taus) ** (2 - 2 * s))
    c = s2 / (1 + lam * taus)
    EV = float(c @ np.linalg.solve(C, c))
    return h * len(taus) + w * (s2 - EV), s2 - EV

def sp_best(p, K, seed=0, starts=16):
    rng = np.random.default_rng(seed); lt = np.log(1 / p['lam'])
    f = lambda x: sp_J(p, np.exp(x))[0]
    best = (np.inf, None)
    for x0 in [np.full(K, lt) + np.linspace(-0.3, 0.3, K)] + [rng.uniform(lt - 3, lt + 3, K) for _ in range(starts)]:
        r = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-8, fatol=1e-14, maxiter=4000 * K))
        if r.fun < best[0]: best = (r.fun, np.sort(r.x))
    return best[0], list(np.exp(best[1]))

def merge3(rates):
    """Counting-rule merge (THEORY §3 step 4): poles of one class less than a factor 3 apart are one layer."""
    rs = sorted(rates); groups = []
    for r in rs:
        if groups and r / groups[-1][-1] < 3: groups[-1].append(r)
        else: groups.append([r])
    return [float(np.exp(np.mean(np.log(g)))) for g in groups], [len(g) for g in groups]


# ---------------------------------------------------------------- optimal static read-out weights of a design (same
# assembly as face_hybrid.mse_fast, which returns only the error; checked against it in readout_ou)
from face_hybrid import _Flag, _solve
def readout_ou(p, bl, bc):
    a = np.asarray(p['a'], float)[:, None, None]; v = np.asarray(p['v'], float); n = p.get('n', 1); N = p['N']; Nc = p.get('Nc', 0.0)
    rho = np.asarray(p['rho'], float); lead = p.get('lead', 0.0)
    vm = v * (rho + (1 - rho) / n); vv = v[:, None, None]; vmm = vm[:, None, None]
    bl = np.asarray(bl, float); bc = np.asarray(bc, float); kl, kc = len(bl), len(bc)
    M = np.zeros((kl + kc, kl + kc)); r = np.zeros(kl + kc)
    if kl:
        BK, BL = bl[None, :, None], bl[None, None, :]
        M[:kl, :kl] = (vv * _F0(a, BK, BL)).sum(0) + (N + Nc) * np.outer(bl, bl) / (bl[:, None] + bl[None, :])
        r[:kl] = (vv[:, :, 0] * bl[None, :] / (a[:, :, 0] + bl[None, :])).sum(0)
    if kc:
        BK, BL = bc[None, :, None], bc[None, None, :]
        M[kl:, kl:] = (vmm * _F0(a, BK, BL)).sum(0) + (N / n + Nc) * np.outer(bc, bc) / (bc[:, None] + bc[None, :])
        r[kl:] = (vmm[:, :, 0] * bc[None, :] * np.exp(-a[:, :, 0] * lead) / (a[:, :, 0] + bc[None, :])).sum(0)
    if kl and kc:
        B1, B2 = bl[None, :, None], bc[None, None, :]
        X = (vmm * _Flag(a, B1, B2, lead)).sum(0) + (N / n + Nc) * np.outer(bl, bc) * np.exp(-bl[:, None] * lead) / (bl[:, None] + bc[None, :])
        M[:kl, kl:] = X; M[kl:, :kl] = X.T
    g = _solve(M, r); e = float(v.sum() - r @ g)
    e2 = mse_fast(p['a'], p['v'], N, n, rho, lead, bl, bc, Nc)
    assert abs(e - e2) <= 1e-9 * max(1.0, abs(e2)), (e, e2)
    return list(map(float, g[:kl])), list(map(float, g[kl:]))

def readout_sp(p, taus):
    lam, s2, V0, t0, s = p['lam'], p['sigma2'], p['V0'], p['tau0'], p['s']
    taus = np.asarray(taus, float); b = 1 / taus
    C = s2 * _F0(lam, b[:, None], b[None, :]) + np.diag(V0 * (t0 / taus) ** (2 - 2 * s))
    return list(map(float, np.linalg.solve(C, s2 / (1 + lam * taus))))

# ---------------------------------------------------------------- main
def predict_ou(name, p, kmax_l, kmax_c):
    rows = {}
    for kl in range(kmax_l + 1):
        for kc in range(kmax_c + 1):
            J, bl, bc = best_design(p, kl, kc)
            rows[f'{kl}L{kc}S'] = dict(J=float(J), bl=[float(x) for x in bl], bc=[float(x) for x in bc])
    key = min(rows, key=lambda k: rows[k]['J']); r = rows[key]; Jst = r['J']
    kl, kc = len(r['bl']), len(r['bc'])
    fun = lambda x: J_ou(p, np.exp(x[:kl]), np.exp(x[kl:]))[0]
    H = hessian_logtau(fun, np.log(np.array(r['bl'] + r['bc']))) if kl + kc else []
    out = dict(design=key, J_star=Jst, bl=r['bl'], bc=r['bc'], H_logb=[float(x) for x in H], all_designs=rows)
    out['lam_tau_local'] = [[float(a_ / b_) for a_ in p['a']] for b_ in r['bl']]
    out['lam_tau_shared'] = [[float(a_ / b_) for a_ in p['a']] for b_ in r['bc']]
    return out

def interlaces(a, b):
    a = sorted(a); b = sorted(b)
    if len(a) != len(b): return None
    return bool(all(a[i] < b[i] for i in range(len(a))) and all(b[i] < a[i + 1] for i in range(len(a) - 1)))

if __name__ == '__main__':
    P = {}
    for name, p in W['worlds'].items():
        kind = p['kind']
        if kind == 'ou':
            o = predict_ou(name, p, p['kmax_local'], p['kmax_shared'])
            a = p['a']
            # rivals
            seta = J_ou(p, [x for x, r_ in zip(a, p['rho']) if (p.get('n', 1) == 1 or r_ < 1)],
                        [x for x, r_ in zip(a, p['rho']) if (p.get('n', 1) > 1 and r_ >= 1)])[0]
            one = min(v['J'] for k, v in o['all_designs'].items() if sum(int(c) for c in k.replace('L', ' ').replace('S', '').split()) == 1)
            kmL, kmC = p['kmax_local'], p['kmax_shared']
            more = o['all_designs'][f'{kmL}L{kmC}S']['J']
            o['rivals'] = dict(set_at=dict(J=float(seta), rates=a), one_layer=float(one), more_layers=float(more),
                               none=float(o['all_designs']['0L0S']['J']))
            if p.get('n', 1) > 1:
                o['rivals']['no_sharing'] = float(min(v['J'] for k, v in o['all_designs'].items() if k.endswith('L0S') and k != '0L0S'))
                o['rivals']['all_shared'] = float(min(v['J'] for k, v in o['all_designs'].items() if k.startswith('0L') and k != '0L0S'))
            if o['design'] in ('2L0S',) and len(a) == 2:
                o['interlacing'] = interlaces(a, o['bl'])
            o['gl'], o['gc'] = readout_ou(p, o['bl'], o['bc'])
            P[name] = o
        elif kind == 'rw':
            P[name] = rw_prediction(p)
        elif kind == 'storenoise':
            rows = {}
            for K in range(0, p['kmax'] + 1):
                if K == 0: rows['0'] = dict(J=float(p['w'] * p['sigma2']), taus=[])
                else:
                    J, t = sp_best(p, K); rows[str(K)] = dict(J=float(J), taus=[float(x) for x in t])
            key = min(rows, key=lambda k: rows[k]['J']); r = rows[key]
            distinct, copies = merge3([1 / x for x in r['taus']])
            K = len(r['taus'])
            fun = lambda x: sp_J(p, np.exp(x))[0]
            H = hessian_logtau(fun, np.log(np.array(r['taus']))) if K else []
            s = p['s']
            P[name] = dict(K_stores=K, distinct_time_constants=len(distinct), copies=copies,
                           taus=r['taus'], lam_tau=[p['lam'] * x for x in r['taus']], J_star=r['J'],
                           H_logtau=[float(x) for x in H], all_designs=rows,
                           closed_form_low_snr_lam_tau=(1 - s) / s,
                           slower_than_mode=bool(all(p['lam'] * x > 1 for x in r['taus'])),
                           g=readout_sp(p, r['taus']) if K else [],
                           rivals=dict(modelS_faster_than_mode='lam*tau < 1 (Model S interlacing, exogenous noise)',
                                       set_at=float(sp_J(p, [1 / p['lam']] * K)[0]) if K else None))
    # the counting rule (count_rule.py, THEORY §3) applied to each predicted design: the predicted COUNTED structure
    import count_rule as cr
    for name, o in P.items():
        p = W['worlds'][name]; band = tuple(p['count_band'])
        if p['kind'] == 'ou': d = dict(bl=o['bl'], gl=o['gl'], bc=o['bc'], gc=o['gc'])
        elif p['kind'] == 'rw': d = dict(bl=o['b'], gl=[1.0], bc=[], gc=[])
        else: d = dict(bl=[1 / x for x in o['taus']], gl=o['g'], bc=[], gc=[])
        o['counted'] = cr.count(d, band, lead=int(p.get('lead', 0)))
    json.dump(P, open(os.path.join(HERE, 'PREDICTIONS_EVO.json'), 'w'), indent=1, default=float)
    for k, v in P.items():
        print(k, json.dumps({kk: vv for kk, vv in v.items() if kk not in ('all_designs',)}, default=float)[:900])
