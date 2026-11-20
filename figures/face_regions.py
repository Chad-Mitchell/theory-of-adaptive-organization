"""Region labels of the face figure, computed from J and the tables of face_model.py (no hand-drawn boundaries).

Designs (h = 1, so w = R/Var):
  blind                 J = w*Var                                         S = 0
  central K = 1..14     J = K + C0/Neff + w*E_K(Neff, lead)              Neff = N/n pooled, reads travel (lead)
  federated K = 1..14   J = n*(K + C0/Neff) + w*E_K(Neff, 0)             n units, each its own tracker, lead 0, no pooling
(see face_model.py).  Sensing (Neff) is optimized for every design.
RUIN (the master equation's constraint, diffusion form; assumptions, not measurements): the system earns y = ETA*w per unit time, holds a
reserve B = BETA*w, and its realized cost fluctuates with variance sigma^2 = 2*(w*E)^2 per unit time.  Lundberg: P(ruin) <= EPS iff
theta*B >= ln(1/EPS), theta = 2*(y - J)/sigma^2, i.e.   BETA*(ETA - J/w) >= ln(1/EPS) * E^2.
A design is feasible only if it meets this; the best design is the cheapest feasible one; if none is feasible the cell is NOT VIABLE
(label -1).  With ETA, BETA, EPS scaled to the stake the constraint depends on R and E only, never on size.
best_design(R, lat, sensing='optimized'|'fixed', ruin=True) -> (K, federated, J, S, ruin_binds)."""
import os, json
import numpy as np
from scipy.interpolate import PchipInterpolator
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'face_tables.json')))
KMAX, VAR, C0, N_FIX = T['KMAX'], 1.0, T['C0'], T['N_FIX']
N_UNITS = 10                                  # n: units pooled by a central tracker / split by federation
ETA, BETA, EPS = 1.5, 5.0, 1e-3               # income per unit stake-time, reserve in stake-times, ruin probability
LNEPS = float(np.log(1 / EPS))
LN = np.log(np.array(T['N'])); LEADS = np.array(T['leads']); E = np.array(T['E'])      # E[K-1, iN, ilead]
NFINE = np.exp(np.linspace(LN[0], LN[-1], 400))
POS = LEADS[1:]                                  # tabulated positive leads; LEADS[0] = 0

def E_at(K, lead):
    """E_K(Neff, lead) on NFINE.  lead = 0: the table; 0 < lead < POS[0]: linear in the lead from lead 0 (E is smooth in the lead there);
    otherwise log E linear in log lead between table nodes; then PCHIP in log Neff."""
    lead = float(lead)
    if lead <= 0: col = np.log(E[K - 1, :, 0])
    elif lead < POS[0]: col = np.log(E[K - 1, :, 0] + (E[K - 1, :, 1] - E[K - 1, :, 0]) * lead / POS[0])
    else: col = np.array([np.interp(np.log(lead), np.log(POS), np.log(E[K - 1, i, 1:])) for i in range(len(LN))])
    return np.exp(PchipInterpolator(LN, col)(np.log(NFINE)))

def _candidates(lead, n=N_UNITS):
    """list of (name, upkeep multiplier m, error curve e(Neff) on NFINE): J = m*(K + C0/Neff) + w*e."""
    out = []
    for K in range(1, KMAX + 1):
        out.append((('C', K), 1, K, E_at(K, lead)))
        out.append((('F', K), n, K, E_at(K, 0.0)))
    return out

def best_design(R, lead, sensing='optimized', ruin=True, n=N_UNITS, eta=ETA, beta=BETA):
    w = np.atleast_1d(np.asarray(R, float)) / VAR; nw = len(w); idx = np.arange(nw)
    names = [0]; J = [w * VAR]; S = [0 * w]
    feas0 = beta * (eta - 1.0) >= LNEPS * 1.0 if ruin else True                           # blind: E = Var = 1
    if not feas0: J[0] = np.full(nw, np.inf)
    bind = [np.zeros(nw, bool)]
    for name, m, K, e in _candidates(lead, n):
        if sensing == 'fixed':
            i = np.argmin(abs(NFINE - N_FIX)); Jk = m * (K + C0 / NFINE[i]) + w * e[i]; Sk = m * (K + C0 / NFINE[i]) + 0 * w; bd = np.zeros(nw, bool)
        else:
            Sn = m * (K + C0 / NFINE)[None, :]; tot = Sn + w[:, None] * e[None, :]
            if ruin:
                ok = beta * (eta - tot / w[:, None]) >= LNEPS * e[None, :] ** 2
                tot_f = np.where(ok, tot, np.inf)
            else:
                tot_f = tot
            j = tot_f.argmin(1); Jk = tot_f[idx, j]; Sk = Sn[0, j]
            bd = (tot.argmin(1) != j) & np.isfinite(Jk)                                      # ruin forced a different N than the unconstrained argmin
        names.append(name); J.append(Jk); S.append(Sk); bind.append(bd)
    J = np.vstack(J); S = np.vstack(S); bind = np.vstack(bind); i = J.argmin(0)
    viable = np.isfinite(J[i, idx])
    K = np.array([0 if names[j] == 0 else names[j][1] for j in i]); F = np.array([names[j] != 0 and names[j][0] == 'F' for j in i])
    K = np.where(viable, K, -1); F = F & viable
    # does ruin change the answer?  compare with the unconstrained argmin
    return K, F, np.where(viable, J[i, idx], np.nan), S[i, idx], bind[i, idx]

def unconstrained_design(R, lead, n=N_UNITS):
    K, F, J, S, _ = best_design(R, lead, ruin=False, n=n); return K, F, J, S

if __name__ == '__main__':
    R = np.logspace(-1, 9, 21)
    for lead in (0.0, 0.1, 1.0, 10.0, 100.0, 1000.0):
        K, F, *_ = best_design(R, lead); print('lead', lead, 'K', K.tolist(), 'fed', F.astype(int).tolist())
