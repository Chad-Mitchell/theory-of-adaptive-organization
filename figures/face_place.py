"""Compute each hypothesized placement's coordinates, uncertainty and design from the input ranges in face_systems.py.
nice -n 19 python3 figures/face_place.py      (about 1-3 minutes)      writes figures/face_dots.json"""
import os, sys, json
import numpy as np
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import face_map as fm
from face_hybrid import best_fast
from face_systems import SYSTEMS

def measured(c, t):
    """E. coli: X_L from the measured proxy log-range (log-uniform), n = 1."""
    XL = 10 ** (c['logXL'][0] + t * (c['logXL'][1] - c['logXL'][0])) if t is not None else 10 ** c['logXL_c']
    return dict(XL=float(XL), XS=float('nan'), nu=1.0, kL=1.0, kS=0.0, d=int(XL > 1), ell_tau=float('nan'), pi=1.0)
NDRAW = 400

def coords(c, u):
    """u in [0,1]^7 -> (X_L, X_S or nan, nu, kL, kS, design).  Log-uniform in every range except rho (uniform)."""
    lg = lambda r, t: float(np.exp(np.log(r[0]) + t * (np.log(r[1]) - np.log(r[0]))))
    tau, lead, n = lg(c['tau'], u[0]), lg(c['lead'], u[1]), int(round(lg(c['n'], u[2])))
    rho = c['rho'][0] + u[3] * (c['rho'][1] - c['rho'][0]); snr, R, hc = lg(c['snr'], u[4]), lg(c['R'], u[5]), lg(c['hc'], u[6])
    a, v = 1 / tau, 1.0; N = 2 * v / (snr * a)
    GL, GS, pi = fm.gains_ou(v, a, N, n, rho, lead); XL = R * GL / v
    if n == 1:
        return dict(XL=float(XL), XS=float('nan'), nu=1.0, kL=1.0, kS=0.0, d=int(XL > 1), ell_tau=lead / tau, pi=1.0)
    XS = (n / hc) * R * GS / v; nu = n / hc
    eB = best_fast([a], [v], N, n, rho, lead, 1, 1, starts=2)[0]; GB = max(v - eB, GL, GS)
    kS = (GB - GL) / GS if GS > 1e-12 * GL else 0.0; kL = (GB - GS) / GL
    return dict(XL=float(XL), XS=float(XS), nu=nu, kL=float(kL), kS=float(kS), d=int(fm.decide(XL, XS, nu, kL, kS)), ell_tau=lead / tau, pi=float(pi))

def job(args):
    si, ci = args; S = SYSTEMS[si]; c = S['comps'][ci]; rng = np.random.default_rng(100 * si + ci)
    if S.get('measured'):
        centre = measured(c, None); draws = [measured(c, t) for t in rng.uniform(size=NDRAW)]
    else:
        centre = coords(c, np.full(7, 0.5))
        draws = [coords(c, rng.uniform(size=7)) for _ in range(NDRAW)]
    lx = np.log10([d['XL'] for d in draws]); ly = np.log10([max(d['XS'], 1e-300) for d in draws]) if c['n'][1] > 1 else None
    out = dict(system=S['name'], strong=S['strong'], measured=bool(S.get('measured')), degree=c.get('degree', 1), lab=c['lab'], inputs={k: c[k] for k in c if k != 'lab'}, centre=centre,
               design_share={fm.VALUE_NAMES[k]: float(np.mean([d['d'] == k for d in draws])) for k in range(4)},
               logXL_mean=float(lx.mean()), logXL_sd=float(lx.std()))
    if ly is not None:
        ly = np.maximum(ly, -6.0)                 # far below the band: X_S < 1e-6, the shared layer is worthless
        C = np.cov(lx, ly); out.update(logXS_mean=float(ly.mean()), cov=C.tolist(), logXS_q=[float(np.quantile(ly, q)) for q in (0.05, 0.5, 0.95)])
    out['logXL_q'] = [float(np.quantile(lx, q)) for q in (0.05, 0.5, 0.95)]
    return out

if __name__ == '__main__':
    jobs = [(si, ci) for si, s in enumerate(SYSTEMS) for ci in range(len(s['comps']))]
    with Pool(5) as p: res = p.map(job, jobs)
    json.dump(res, open(os.path.join(HERE, 'face_dots.json'), 'w'), indent=1)
    for r in res:
        c = r['centre']
        print(f"{r['system']:15s} {r['lab']:15s} XL={c['XL']:9.3g} XS={c['XS']:9.3g} nu={c['nu']:7.3g} l/tau={c['ell_tau']:8.3g} pi={c['pi']:6.3g} kL={c['kL']:.2f} kS={c['kS']:.2f} -> {fm.VALUE_NAMES[c['d']]:6s}",
              {k: round(v, 2) for k, v in r['design_share'].items() if v > 0})
