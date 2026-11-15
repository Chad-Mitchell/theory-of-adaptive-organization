"""LEARNSIM theory predictions.  Computed ONLY from GTAO's continuous-time closed forms
(FORMAL/THEOREMS.md T1, T1.8, T3, T5; REVIEW/math/REPORT.md section 4 exact V; P10).
The simulator (world.py / run_*.py) never imports this file, and this file never imports the simulator.
World constants are duplicated here by hand from PREREG.md section 2.
"""
import json, numpy as np
from scipy.optimize import brentq

C_R = 800.0      # cost per complete read (tech R)
C_A = 1.0        # cost per unit sample-rate (tech A); precision bought linearly (theta = 1)
SIG2 = 1.0e4     # per-sample noise variance (tech A)
W = 1.0          # stakes per member
Q_U = 1.0        # private drift variance per step (base)
RHOS = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
H_UP = 40.0      # upkeep per step in arm RRh (h' = 1 in member-cost units, sqrt(2 C_R W Q_U) = 40)

def phi(tech, Wt, q):
    if tech == 'R':
        return np.sqrt(2 * C_R * Wt * q)
    return 3 * C_A ** (1 / 3) * (Wt * np.sqrt(q * SIG2) / 2) ** (2 / 3)

def effort(tech, Wt, q):  # reads per step (R) or samples per step (A)
    if tech == 'R':
        return np.sqrt(Wt * q / (2 * C_R))
    return (Wt * np.sqrt(q * SIG2) / (2 * C_A)) ** (2 / 3)

AB = {'R': (0.5, 0.5), 'A': (2 / 3, 1 / 3)}

def gain(N, lev, mem, qg, qu, h):
    return N * phi(mem, W, qg + qu) - phi(lev, N * W, qg) - N * phi(mem, W, qu) - h

def nstar(lev, mem, qg, qu, h=0.0):
    f = lambda lnN: gain(np.exp(lnN), lev, mem, qg, qu, h)
    lo, hi = np.log(1e-3), np.log(1e12)
    if f(hi) <= 0:
        return np.inf
    # G<0 at small N (h>0 or a>0); find the crossing
    return float(np.exp(brentq(f, lo, hi, xtol=1e-12)))

ARMS = {'RR': ('R', 'R', 0.0), 'RRh': ('R', 'R', H_UP), 'AA': ('A', 'A', 0.0),
        'AR': ('A', 'R', 0.0), 'RA': ('R', 'A', 0.0)}  # (level tech, member tech, upkeep)

def slope(xs, ys):
    return float(np.polyfit(np.log(xs), np.log(ys), 1)[0])

def main():
    out = {'arms': {}}
    for arm, (lev, mem, h) in ARMS.items():
        ns = [nstar(lev, mem, r * Q_U, Q_U, h) for r in RHOS]
        aL, bL = AB[lev]; am, bm = AB[mem]
        rec = {'level': lev, 'members': mem, 'h': h, 'Nstar': ns,
               'e_g_window': slope(RHOS, ns),
               'e_g_asym': -(1 - bL) / (1 - aL),
               'rival_member_tech_e_g': -(1 - bm) / (1 - am),
               'rival_tech_independent_e_g': -1.0,
               'e_u_asym': (1 - bm) / (1 - aL),
               'Nstar_rho_product': [n * r for n, r in zip(ns, RHOS)]}
        if lev == mem:
            rec['V_at_Nstar'] = [effort(lev, n * W, r * Q_U) / effort(mem, W, (1 + r) * Q_U) for n, r in zip(ns, RHOS)]
        if arm == 'RR':
            rec['V_exact_math_review'] = [1 + (1 + r) ** -0.5 for r in RHOS]
        if arm == 'RRh':
            hp = H_UP / np.sqrt(2 * C_R * W * Q_U)
            rec['V_exact_math_review'] = [0.5 * (1 + (1 + r) ** -0.5) * (1 + np.sqrt(1 + 4 * hp * (np.sqrt(1 + r) - 1) / r)) for r in RHOS]
        out['arms'][arm] = rec
    # T3 / T1.7 factorial: base rho0 = 0.04, factors x2
    fac = {}
    for arm in ['RR', 'RRh', 'AR', 'RA']:
        lev, mem, h = ARMS[arm]
        qg0, qu0 = 0.04, 1.0
        cells = {'base': (qg0, qu0), 'shared_x2': (2 * qg0, qu0), 'private_x2': (qg0, 2 * qu0), 'both_x2': (2 * qg0, 2 * qu0)}
        ns = {k: nstar(lev, mem, a, b, h) for k, (a, b) in cells.items()}
        fac[arm] = {'cells': cells, 'Nstar': ns,
                    'dlnN_shared': float(np.log(ns['shared_x2'] / ns['base'])),
                    'dlnN_private': float(np.log(ns['private_x2'] / ns['base'])),
                    'dlnN_both': float(np.log(ns['both_x2'] / ns['base']))}
    out['factorial'] = fac
    # P10 relative-resolution threshold (common tech b), N -> infinity
    out['P10'] = {str(e): {'R': (1 - e) ** (-1 / 0.5) - 1, 'A': (1 - e) ** (-1 / (1 / 3)) - 1} for e in [0.003, 0.01, 0.03]}
    print(json.dumps(out, indent=1, default=float))
    json.dump(out, open('THEORY_PREDICTIONS.json', 'w'), indent=1, default=float)

if __name__ == '__main__':
    main()
