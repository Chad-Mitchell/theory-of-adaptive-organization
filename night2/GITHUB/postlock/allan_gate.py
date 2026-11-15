"""POST-OUTCOME IMPLEMENTATION of a PRE-OUTCOME TEXT RULE (declared).
The rule is reviews/night2/GITHUB_ADDENDUM_REGIME.md on main (commit bb7b571, 2026-11-15 09:02 ET, before run histories were pulled).
That file locked the rule in text but no code. This script was written on 2026-11-15 after results_real.json (P1/P2) had been
computed and read, by a different executor; the author therefore saw b-hat before writing it. Choices not fixed by the text are listed
in CHOICES and were made to follow the text literally, not tuned. Locked analysis code (code/analyze.py) is imported unchanged.
"""
import json, os, sys, math, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CODE = os.path.join(HERE, '..', 'code'); sys.path.insert(0, CODE)
import analyze as A
SEED = 20261115; B = 999; TS = [1, 2, 4, 8, 13]
CHOICES = ["Allan factor AF(T) = mean((N_{k+1}-N_k)^2) / (2 mean(N_k)) over consecutive non-overlapping T-week blocks of |dx| (standard definition)",
           "a block counts only if all its weekly change indicators are observed (no NaN); a pair counts only if both blocks count",
           "a unit enters AF(T) if it has >=1 valid block pair and mean count > 0",
           "pooling: median across flat units at each T; OLS of ln(median AF) on ln T over the T with a finite positive median",
           "CI: cluster bootstrap over primary upstream (u['pu']), B=999, SEED 20261115, percentile 95%"]
def af_unit(c, T):
    n = len(c) // T; blocks = []
    for k in range(n):
        seg = c[k*T:(k+1)*T]; blocks.append(np.nan if np.isnan(seg).any() else seg.sum())
    pairs = [(blocks[k], blocks[k+1]) for k in range(n-1) if not (np.isnan(blocks[k]) or np.isnan(blocks[k+1]))]
    valid = [b for b in blocks if not np.isnan(b)]
    if not pairs or not valid or np.mean(valid) <= 0: return None
    return float(np.mean([(b - a)**2 for a, b in pairs]) / (2 * np.mean(valid)))
def H_of(units):
    med = {}
    for T in TS:
        v = [af_unit(np.abs(np.diff(u['x'])), T) for u in units]; v = [x for x in v if x is not None]
        if v: med[T] = float(np.median(v))
    pts = [(math.log(T), math.log(m)) for T, m in med.items() if m > 0]
    if len(pts) < 3: return None, med
    s = np.polyfit([p[0] for p in pts], [p[1] for p in pts], 1)[0]
    return (s + 1) / 2, med
if __name__ == '__main__':
    wf, pinned, fu, fo, um = A.build_real(); units = A.to_units(wf, fu); flat = [u for u in units if not u['is_level']]
    H, med = H_of(flat)
    cl = collections.defaultdict(list)
    for i, u in enumerate(flat): cl[u['pu']].append(i)
    keys = list(cl); rng = np.random.default_rng(SEED); bs = []
    for _ in range(B):
        pick = rng.choice(len(keys), len(keys), replace=True)
        h, _ = H_of([flat[i] for k in pick for i in cl[keys[k]]])
        if h is not None: bs.append(h)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    main = json.load(open(os.path.join(HERE, '..', 'results_real.json'))); g = main['gate']
    if lo <= 0.5 <= hi and hi - lo <= 0.4: reg = 'A'
    elif hi < 0.5 or lo > 0.5: reg = 'NOT-A'
    else: reg = 'UNESTABLISHED'
    out = dict(H=H, H_ci=[float(lo), float(hi)], median_AF=med, n_boot=len(bs), regime=reg, choices=CHOICES)
    if reg == 'NOT-A':
        c = 1 / (1 + 2 * H); band = (c - 0.15, c + 0.15); out['band'] = band
        out['P1_vs_band'] = A.verdict_band(g['b'], g['b_ci'], band); out['P2_vs_band'] = A.verdict_band(g['a'], g['a_ci'], band)
    elif reg == 'A':
        out['P1_vs_band'] = main['P1_drift_matching']; out['P2_vs_band'] = main['P2_stakes_a']
    else:
        out['P1_vs_band'] = out['P2_vs_band'] = 'regime unestablished on the event-frequency proxy (no status change)'
    out['original_band'] = dict(P1=main['P1_drift_matching'], P2=main['P2_stakes_a'])
    json.dump(out, open(os.path.join(HERE, 'results_allan_gate.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
