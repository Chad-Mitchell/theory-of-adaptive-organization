"""PREREG_2 predictions from MEASURED inputs only (LEVEL_CLASS.json, MEASURED_AB.json); no onset outcome.
Measured cost laws: phi_hat(W,q) = exp(c0) W^a q^b fitted on realized costs of learned trackers
  level tech: from level-alone runs (level range); member tech: from Stage A lone runs (member range).
Prediction (level-class): onset N*(rho) = root of N phi_m(1,q_g+q_u) - phi_L(N,q_g) - N phi_m(1,q_u) = 0, slope over gated rho.
Rival (members'-class sets e_g): same with the level's law replaced by the member technology's law."""
import json, numpy as np
from scipy.optimize import brentq

LC = json.load(open('LEVEL_CLASS.json')); MAB = json.load(open('MEASURED_AB.json'))

def costfit(rows):
    X = np.column_stack([np.ones(len(rows)), np.log([r['W'] for r in rows]), np.log([r['q'] for r in rows])])
    y = np.log([r['cost'] for r in rows]); return np.linalg.lstsq(X, y, rcond=None)[0]

LAW = {('level', t): costfit([r for r in LC['level_rows'] if r['tech'] == t]) for t in 'RA'}
LAW.update({('member', t): costfit([r for r in MAB['rows'] if r['tech'] == t]) for t in 'RA'})
phi = lambda law, W, q: float(np.exp(law[0] + law[1] * np.log(W) + law[2] * np.log(q)))

def nstar(levlaw, memlaw, qg, qu=1.0):
    f = lambda l: np.exp(l) * phi(memlaw, 1, qg + qu) - phi(levlaw, np.exp(l), qg) - np.exp(l) * phi(memlaw, 1, qu)
    hi = np.log(1e13)
    if f(hi) <= 0: return None
    return float(np.exp(brentq(f, np.log(1e-3), hi)))

# selection gate (framework 3.10): prize b_m * rho > eps_hat(member tech); b_m = member cost elasticity
GATE = {t: LC['member'][t]['eps_hat'] / MAB[t]['b'] for t in 'RA'}
RHO_MAIN = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]; RHO_EXT = [0.64, 1.28]
ARMS = {'RR': ('R', 'R'), 'AA': ('A', 'A'), 'AR': ('A', 'R'), 'RA': ('R', 'A')}
out = {'law': {'%s_%s' % k: v.tolist() for k, v in LAW.items()}, 'gate_rho_min': GATE, 'arms': {}}
for arm, (L, M) in ARMS.items():
    rhos = [r for r in RHO_MAIN + RHO_EXT if r > GATE[M]]
    if M == 'R': rhos = [r for r in rhos if r in RHO_MAIN]   # R-member arms: main scan already has >=4 gated rho
    ns = [nstar(LAW[('level', L)], LAW[('member', M)], r) for r in rhos]
    nr = [nstar(LAW[('level', M)], LAW[('member', M)], r) for r in rhos]   # rival: level behaves like members' tech
    sl = lambda y: float(np.polyfit(np.log(rhos), np.log(y), 1)[0])
    aL, bL = LC['level'][L]['effort_elasticities']['a'], LC['level'][L]['effort_elasticities']['b']
    am, bm = LC['member'][M]['effort_elasticities']['a'], LC['member'][M]['effort_elasticities']['b']
    out['arms'][arm] = dict(gated_rhos=rhos, Nstar_pred=ns, Nstar_rival=nr, e_pred_window=sl(ns), e_rival_window=sl(nr),
                            e_asym_level_class=-(1 - bL) / (1 - aL), e_asym_member_class=-(1 - bm) / (1 - am))
json.dump(out, open('PREDICTIONS_2.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
