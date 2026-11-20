"""The face figure's regions are the argmin of J, not hand-drawn: recompute them independently and compare with figures/face_regions.json.
Run: nice -n 19 python3 -m pytest -q tools/test_face_regions.py"""
import os, sys, json
import numpy as np
import pytest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'figures'); sys.path.insert(0, FIG)
import face_regions as fr

T = json.load(open(os.path.join(FIG, 'face_tables.json'))); REG = json.load(open(os.path.join(FIG, 'face_regions.json')))
E = np.array(T['E']); LN = np.log(T['N']); LEADS = np.array(T['leads']); C0, HF = T['C0'], T['HF']

def slow_J(K, fed, w, lat):
    """J = h*K + [hf] + min_N ( w*E_K(N, lead) + C0/N ), h = 1, brute force over a dense N grid; E from the table by bilinear interpolation in (log N, log lead)."""
    lead = 0.0 if fed else lat
    la = np.log(np.where(np.array(lead) > 0, lead, 10 ** -2.5)); axis = np.log(np.where(LEADS > 0, LEADS, 10 ** -2.5))
    best = np.inf
    for lnN in np.linspace(LN[0], LN[-1], 3000):
        i = min(max(np.searchsorted(LN, lnN) - 1, 0), len(LN) - 2); t = (lnN - LN[i]) / (LN[i + 1] - LN[i])
        e = [np.interp(la, axis, np.log(E[K - 1, j])) for j in (i, i + 1)]
        # PCHIP in the figure code vs linear here: agree to a fraction of a percent, far below the margins tested below
        eK = np.exp((1 - t) * e[0] + t * e[1]); best = min(best, w * eK + C0 / np.exp(lnN))
    return K + (HF if fed else 0) + best

def slow_best(R, lat):
    cands = {(0, False): R * 1.0}
    for K in range(1, T['KMAX'] + 1):
        for fed in (False, True): cands[(K, fed)] = slow_J(K, fed, R, lat)
    order = sorted(cands, key=cands.get); return order[0], cands[order[1]] / cands[order[0]] - 1

def test_labels_match_independent_recompute():
    rng = np.random.default_rng(5); Rg = np.array(REG['R']); Lg = np.array(REG['lat']); Kg = np.array(REG['K']); Fg = np.array(REG['fed']); n = checked = 0
    while checked < 30 and n < 400:
        n += 1; i = rng.integers(len(Lg)); j = rng.integers(len(Rg)); (K, fed), margin = slow_best(Rg[j], Lg[i])
        if margin < 0.01: continue           # near a boundary the two interpolations may differ; skip those points
        checked += 1; assert (K, int(fed)) == (min(Kg[i, j], T['KMAX']), Fg[i, j]), (Rg[j], Lg[i])
    assert checked == 30

def test_structure_follows_from_J():
    Kg = np.array(REG['K']); Fg = np.array(REG['fed']); Rg = np.array(REG['R']); Lg = np.array(REG['lat'])
    assert Kg.min() == 0 and Kg.max() >= 6                                   # graded sequence 0,1,2,...,6+ with no cap at 2
    assert set(np.unique(Kg)) >= set(range(0, 7))
    assert Rg[-1] / Rg[0] > 1e10 and Kg[:, -1].min() >= 5                    # extends past R = 1e9 and keeps adding layers: no size ceiling
    on = [Rg[np.argmax(Fg[i] > 0)] for i in range(len(Lg)) if Fg[i].any()]; lat_on = [Lg[i] for i in range(len(Lg)) if Fg[i].any()]
    assert len(on) > 10 and lat_on[0] < 1.0 and on[0] > on[-1] * 3          # federation is driven by latency: it starts at lower R as latency rises
    assert on[0] > on[len(on) // 2] > on[-1]                                  # monotone in latency over the range
    assert all(v in range(0, T['KMAX'] + 1) for v in np.unique(Kg))          # only layer counts: there is no 'not viable' region in the model

def test_fixed_sensing_boundaries_are_closed_form():
    """With sensing fixed at N_FIX and lead 0 the K -> K+1 boundary is R = h/(E_K - E_{K+1}) and 0 -> 1 is R = (h + C0/N)/(Var - E_1)."""
    iN = int(np.argmin(abs(np.array(T['N']) - T['N_FIX']))); e = E[:, iN, 0]; Rg = np.logspace(0, 9, 3000)
    K, _, _ = fr.best_design(Rg, 0.0, 'fixed')
    pred = {1: (1 + C0 / T['N'][iN]) / (1.0 - e[0])}; pred.update({k + 1: 1.0 / (e[k - 1] - e[k]) for k in range(1, 7)})
    for k in range(1, 8):
        # the argmin is K >= k exactly when R exceeds the first crossing of K=k-1 with K=k, which is the pairwise formula once it is the active one
        got = Rg[np.argmax(K >= k)]
        assert abs(np.log(got / pred[k])) < 0.05 or k > 1 and pred[k] < pred[k - 1], (k, got, pred[k])

def test_spend_rises_everywhere_but_layers_need_not():
    Rg = np.logspace(-1, 9, 81); anyfall = False
    for lat in (0.0, 0.3, 3.0, 300.0):
        K, F, J, S = fr.best_with_spend(Rg, lat); assert np.all(np.diff(S) >= -1e-9); anyfall |= bool(np.any(np.diff(K) < 0))
    assert anyfall                                                            # layers per unit can fall (federation shortens the lead each layer covers)

def test_tables_are_sane():
    assert np.all(np.diff(E, axis=0) <= 1e-12) and np.all(np.diff(E, axis=2) >= -1e-9) and np.all(np.diff(E, axis=1) >= -1e-9)
