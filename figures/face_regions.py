"""Region labels of the face figure, computed from J and the tables of face_model.py (no hand-drawn boundaries).
best_design(R, lat, sensing='optimized'|'fixed') -> (K, federated)  with K = 0..KMAX layers."""
import os, json
import numpy as np
from scipy.interpolate import PchipInterpolator
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'face_tables.json')))
KMAX, VAR, C0, HF, N_FIX = T['KMAX'], 1.0, T['C0'], T['HF'], T['N_FIX']
LN = np.log(np.array(T['N'])); LEADS = np.array(T['leads']); E = np.array(T['E'])      # E[K-1, iN, ilead]
LEAD_LO = 10 ** -2.5                                                                      # lead 0 sits at this point of the log axis
NFINE = np.exp(np.linspace(LN[0], LN[-1], 400))

def _lead_axis(lead):
    return np.log(np.where(lead > 0, lead, LEAD_LO))
_LA = _lead_axis(LEADS)

def E_at(K, lead):
    """E_K(N, lead) on NFINE: interpolate log E in log lead (linear), then in log N (PCHIP)."""
    la = _lead_axis(np.array(lead))
    col = np.array([np.interp(la, _LA, np.log(E[K - 1, i])) for i in range(len(LN))])
    return np.exp(PchipInterpolator(LN, col)(np.log(NFINE)))

def design_costs(w, lead, sensing='optimized'):
    """J of every design at stakes w (h = 1) and latency lead: returns dict name -> J (arrays over w)."""
    w = np.atleast_1d(np.asarray(w, float)); out = {0: w * VAR}
    for fed in (False, True):
        ld = 0.0 if fed else lead
        for K in range(1, KMAX + 1):
            e = E_at(K, ld)
            if sensing == 'optimized':
                J = (K + (HF if fed else 0) + (w[:, None] * e[None, :] + C0 / NFINE[None, :]).min(1))
            else:
                i = np.argmin(abs(NFINE - N_FIX)); J = K + (HF if fed else 0) + w * e[i] + C0 / NFINE[i]
            out[('F' if fed else 'C', K)] = J
    return out

def best_design(R, lead, sensing='optimized'):
    w = np.asarray(R, float) * 1.0 / VAR          # h = 1, so w = R/Var
    c = design_costs(w, lead, sensing); names = list(c); M = np.vstack([c[n] for n in names]); i = M.argmin(0)
    K = np.array([0 if names[j] == 0 else names[j][1] for j in i]); F = np.array([names[j] != 0 and names[j][0] == 'F' for j in i])
    return K, F, M.min(0)

def sensing_spend(R, lead, sensing='optimized'):
    pass

if __name__ == '__main__':
    R = np.logspace(-1, 9, 21)
    for lead in (0.0, 0.1, 1.0, 10.0, 100.0, 1000.0):
        K, F, _ = best_design(R, lead); print('lead', lead, 'K', K.tolist(), 'fed', F.astype(int).tolist())
    print('fixed sensing')
    for lead in (0.0, 1.0, 100.0):
        K, F, _ = best_design(R, lead, 'fixed'); print('lead', lead, 'K', K.tolist(), 'fed', F.astype(int).tolist())

def best_with_spend(R, lead, sensing='optimized'):
    """Like best_design but also returns the judgment spend S* = J* - w*E* (upkeep + federation overhead + sensing) of the argmin."""
    w = np.asarray(R, float); names = [0]; Js = [w * VAR]; Ss = [0 * w]
    for fed in (False, True):
        ld = 0.0 if fed else lead
        for K in range(1, KMAX + 1):
            e = E_at(K, ld)
            tot = w[:, None] * e[None, :] + C0 / NFINE[None, :]; j = tot.argmin(1)
            Jk = K + (HF if fed else 0) + tot[np.arange(len(w)), j]
            Sk = K + (HF if fed else 0) + C0 / NFINE[j]
            names.append(('F' if fed else 'C', K)); Js.append(Jk); Ss.append(Sk)
    Js = np.vstack(Js); Ss = np.vstack(Ss); i = Js.argmin(0); idx = np.arange(len(w))
    K = np.array([0 if names[j] == 0 else names[j][1] for j in i]); F = np.array([names[j] != 0 and names[j][0] == 'F' for j in i])
    return K, F, Js[i, idx], Ss[i, idx]
