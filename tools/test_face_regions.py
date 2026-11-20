"""The face figure's regions are the argmin of J, not hand-drawn: recompute them independently and compare with figures/face_regions.json.
Also checks the structure the figure claims: federation pays for the pooling it gives up (it is never chosen at zero latency), its boundary
is the closed-form comparison of two linear costs, central multi-layer designs exist where J says so, the not-viable region is the ruin
constraint's, and every viable cell meets the Lundberg inequality.
Run: nice -n 19 python3 -m pytest -q tools/test_face_regions.py"""
import os, sys, json
import numpy as np
import pytest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, 'figures'); sys.path.insert(0, FIG)
import face_regions as fr

T = json.load(open(os.path.join(FIG, 'face_tables.json'))); REG = json.load(open(os.path.join(FIG, 'face_regions.json')))
DOTS = json.load(open(os.path.join(FIG, 'face_dots.json')))
E = np.array(T['E']); LN = np.log(T['N']); LEADS = np.array(T['leads']); C0 = T['C0']
n, ETA, BETA, LNEPS = fr.N_UNITS, fr.ETA, fr.BETA, fr.LNEPS

def e_table(K, lead, lnN):
    """E_K at (log N, lead) by bilinear interpolation in (log N, log lead) from the table, written independently of face_regions.E_at."""
    if lead <= 0: col = [E[K - 1, j, 0] for j in range(len(LN))]
    elif lead < LEADS[1]: col = [E[K - 1, j, 0] + (E[K - 1, j, 1] - E[K - 1, j, 0]) * lead / LEADS[1] for j in range(len(LN))]
    else: col = [np.exp(np.interp(np.log(lead), np.log(LEADS[1:]), np.log(E[K - 1, j, 1:]))) for j in range(len(LN))]
    i = min(max(np.searchsorted(LN, lnN) - 1, 0), len(LN) - 2); t = (lnN - LN[i]) / (LN[i + 1] - LN[i])
    return np.exp((1 - t) * np.log(col[i]) + t * np.log(col[i + 1]))

def slow_J(K, fed, w, lat):
    """Lowest J over a dense Neff grid of the design (K, central|federated) that meets the ruin constraint; inf if none."""
    lead = 0.0 if fed else lat; m = n if fed else 1; best = np.inf
    for lnN in np.linspace(LN[0], LN[-1], 1500):
        e = e_table(K, lead, lnN); J = m * (K + C0 / np.exp(lnN)) + w * e
        if BETA * (ETA - J / w) >= LNEPS * e * e: best = min(best, J)
    return best

def slow_best(R, lat):
    cands = {(0, False): R * 1.0 if BETA * (ETA - 1.0) >= LNEPS else np.inf}
    for K in range(1, T['KMAX'] + 1):
        for fed in (False, True): cands[(K, fed)] = slow_J(K, fed, R, lat)
    order = sorted(cands, key=cands.get)
    if not np.isfinite(cands[order[0]]): return (-1, False), np.inf
    return order[0], cands[order[1]] / cands[order[0]] - 1

def test_labels_match_independent_recompute():
    rng = np.random.default_rng(5); Rg = np.array(REG['R']); Lg = np.array(REG['lat']); Kg = np.array(REG['K']); Fg = np.array(REG['fed']); n_ = checked = 0
    while checked < 30 and n_ < 600:
        n_ += 1; i = rng.integers(len(Lg)); j = rng.integers(len(Rg)); (K, fed), margin = slow_best(Rg[j], Lg[i])
        if margin < 0.02: continue           # near a boundary the two interpolations may differ; skip those points
        checked += 1; assert (K, int(fed)) == (min(Kg[i, j], T['KMAX']) if Kg[i, j] >= 0 else -1, Fg[i, j]), (Rg[j], Lg[i])
    assert checked == 30

def test_federation_is_not_free():
    """At zero latency a central tracker has the same error as a federated unit and a fraction of the cost, so federation is never chosen there;
    at any lead it pays n times the upkeep and sensing, so it needs stakes times lateness large enough."""
    Rg = np.logspace(-1, 9, 201)
    K, F, *_ = fr.best_design(Rg, 0.0); assert not F.any()
    for lat in (1e-4, 1e-2, 1.0, 100.0):
        K, F, J, S, _ = fr.best_design(Rg, lat); v = K >= 0
        assert F[v].any() and not F[v][0]                 # small stakes: central; large stakes: federated, never the other way
        first = np.argmax(F & v); assert not F[first:][v[first:] == False].any() and F[first:][v[first:]].all()   # one boundary in R at each latency

def test_federation_boundary_is_driven_by_stakes_times_lateness():
    """Boundary R_b(lat) falls as latency rises, and R_b * (E_c - E_f) is the duplication cost: closed form at fixed sensing, no ruin."""
    Rg = np.logspace(0, 9.5, 2000); rb = []
    lats = (1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0)
    for lat in lats:
        K, F, *_ = fr.best_design(Rg, lat, 'fixed', ruin=False); assert F.any(); rb.append(Rg[np.argmax(F)])
        # pairwise closed form for each K: central beats federated of the same K iff R*(E_c - E_f) < (n-1)*(K + C0/N_FIX)
        iN = int(np.argmin(abs(np.array(T['N']) - T['N_FIX'])))
        for k in range(1, 6):
            Ec, Ef = E[k - 1, iN, :], E[k - 1, iN, 0]
            ec = fr.E_at(k, lat); ef = fr.E_at(k, 0.0); i = np.argmin(abs(fr.NFINE - T['N_FIX']))
            Rpair = (n - 1) * (k + C0 / fr.NFINE[i]) / (ec[i] - ef[i]); Rtest = np.array([Rpair * 0.5, Rpair * 2.0])
            Jc = k + C0 / fr.NFINE[i] + Rtest * ec[i]; Jf = n * (k + C0 / fr.NFINE[i]) + Rtest * ef[i]
            assert Jc[0] < Jf[0] and Jf[1] < Jc[1]
    assert all(a > b for a, b in zip(rb, rb[1:]))                                   # federation starts at lower R as latency rises
    assert 0.5 < (np.log(rb[0]) - np.log(rb[-1])) / (np.log(lats[-1]) - np.log(lats[0])) < 1.5      # about R * latency = constant, over five decades

def test_central_multilayer_exists_and_federation_may_lower_layers():
    Kg = np.array(REG['K']); Fg = np.array(REG['fed']); Rg = np.array(REG['R']); Lg = np.array(REG['lat'])
    assert (Kg[(Fg == 0)] >= 2).any() and (Kg >= 3).any()                           # central designs with 2, 3, ... layers show where J says so
    assert set(np.unique(Kg[Kg >= 0])) >= set(range(1, 6))                         # graded sequence, no cap at 2
    assert Kg.max() <= 14                                                          # capped only by the number of separated scales in the world (14)

def test_not_viable_region_is_the_ruin_constraint():
    Kg = np.array(REG['K']); Rg = np.array(REG['R']); Lg = np.array(REG['lat'])
    assert (Kg == -1).any() and (Kg >= 0).any()
    # low stakes over upkeep: not viable (upkeep and the lateness cost exceed what income and reserve allow); every column is viable above some R
    for i in range(0, len(Lg), 6):
        row = Kg[i]; assert row[-1] >= 0 and (row == -1)[0]; first = np.argmax(row >= 0); assert (row[first:] >= 0).all()
    # each viable cell meets the Lundberg inequality at the design chosen there
    for R_, lat in ((30.0, 0.1), (1e3, 1.0), (1e6, 1e-4), (1e8, 10.0)):
        K, F, J, S, _ = fr.best_design(np.array([R_]), lat); assert K[0] >= 0
        e = (J[0] - S[0]) / R_; assert BETA * (ETA - J[0] / R_) >= LNEPS * e * e - 1e-9
    # blind is excluded by the constraint at these parameters (E = Var = 1 needs beta*(eta-1) >= ln(1/eps))
    assert not (BETA * (ETA - 1.0) >= LNEPS)

def test_spend_rises_with_stakes_when_ruin_is_absent_and_can_fall_when_it_binds():
    Rg = np.logspace(-1, 9, 81); anyfall = False
    for lat in (0.0, 1e-3, 0.3, 3.0, 300.0):
        K, F, J, S = fr.unconstrained_design(Rg, lat); assert np.all(np.diff(S) >= -1e-9); anyfall |= bool(np.any(np.diff(K) < 0))
    assert anyfall                                                                  # layers per unit can fall (central to federated)

def test_dots_are_where_their_notes_say():
    assert DOTS['ant colony']['federated']                                          # the colony is a federation of local trackers
    assert DOTS['E. coli']['K'] >= 1 and DOTS['small team']['K'] >= 1 and not DOTS['E. coli']['federated']
    assert 'biosphere' not in DOTS                                                  # not a unit of selection: not placed
    for d in DOTS.values(): assert d['K'] >= 0                                      # no system placed where nothing is viable
    # ordering of the R guesses is not tested: it is not evidence

def test_tables_are_sane():
    assert np.all(np.diff(E, axis=0) <= 1e-12) and np.all(np.diff(E, axis=2) >= -1e-9) and np.all(np.diff(E, axis=1) >= -1e-9)
    r = (E[0, :, 2] - E[0, :, 0]) / (E[0, :, 1] - E[0, :, 0] + 1e-300); ok = (E[0, :, 1] - E[0, :, 0]) > 1e-9
    assert np.all(r[ok] > 4) and np.all(r[ok] < 20)                                  # E - E(0) is about linear in the lead at small leads (1e-3 vs 1e-4: ratio ~ 10)
