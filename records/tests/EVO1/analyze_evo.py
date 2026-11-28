#!/usr/bin/env python3
"""EVO1 locked scoring.  Reads PREDICTIONS_EVO.json (frozen), worlds.json, runs/*.json; writes ANALYSIS_EVO.json.
Run: nice -n 19 python3 analyze_evo.py [RUNDIR]
Rules (PREREG_EVO.md §5-§7): per seed, miss_A = J(evolved design, theory formula, optimal read-out)/J* - 1 > EPS_BAND;
miss_B = counted structure (count_rule.py; genome structure for W4b) != predicted counted structure.  A seed misses if
miss_A or miss_B.  World: PASSED if misses <= 1 of 8, INCONCLUSIVE if 2, FAILED if >= 3 (P(Bin(8, 0.1) >= 3) = 0.038 < 0.05).
INVALID if the positive control is not PASSED (all worlds), if >= half of the world's null (drift) seeds meet both
criteria, if the nearest named rival has beta*P*gap < 10, if the final-window death fraction > 10%, or (per seed,
unscored) if the population is still improving at the end."""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import predict_evo as pe, count_rule as cr, stores
CFG = json.load(open(os.path.join(HERE, 'worlds.json'))); W = CFG['worlds']; EV = CFG['evolution']
PR = json.load(open(os.path.join(HERE, 'PREDICTIONS_EVO.json')))
EPS_BAND = 10.0 / (EV['beta'] * EV['P'])
GENOME_STRUCTURE_WORLDS = ('W4b',)          # declared before the run: the rule cannot resolve W4b's predicted design
TEST_WORLDS = ['PC', 'W1', 'W2', 'W3', 'W4', 'W4b', 'S031', 'S07']

def J_theory(name, d):
    p = W[name]
    if p['kind'] == 'ou': return pe.J_ou(p, d['bl'], d['bc'])[0]
    if p['kind'] == 'rw':
        b = np.asarray(d['bl'], float); K = len(b)
        if K == 0: return np.inf
        if K == 1: e = p['q'] / (2 * b[0]) + p['N'] * b[0] / 2
        else:
            a_s = 1e-7; e = stores.mse_given_b([a_s], [p['q'] / (2 * a_s)], b, p['N'])[0]
        return p['h'] * K + p.get('h1', 0.0) * b.sum() + p['w'] * e
    taus = [1 / x for x in d['bl']]
    return pe.sp_J(p, taus)[0] if taus else p['w'] * p['sigma2']

def pred_counted(name): return PR[name]['counted']

def rate_bands(name):
    """Allowed |d log rate| per predicted counted pole: sqrt(2 EPS J*/H), H the curvature of J moving that pole's
    store(s) together in log rate (THEORY §3, 'from a cost band to a design band')."""
    p = W[name]; o = PR[name]; Jst = o['J_star']
    if p['kind'] == 'ou':
        x0 = np.log(np.array(o['bl'] + o['bc'])); kl = len(o['bl'])
        f = lambda x: pe.J_ou(p, np.exp(x[:kl]), np.exp(x[kl:]))[0]
        groups = [[i] for i in range(len(x0))]
    elif p['kind'] == 'rw':
        x0 = np.log(np.array(o['b'])); f = lambda x: J_theory(name, dict(bl=list(np.exp(x)))); groups = [[0]]
    else:
        x0 = np.log(1 / np.array(o['taus'])); f = lambda x: J_theory(name, dict(bl=list(np.exp(x)))); groups = [list(range(len(x0)))]
    out = []
    for g in groups:
        e = np.zeros_like(x0); e[g] = 1e-3
        H = (f(x0 + e) - 2 * f(x0) + f(x0 - e)) / 1e-6
        out.append(float(np.sqrt(2 * EPS_BAND * Jst / H)))
    return out

def design_of(c):
    return dict(bl=c['bl'], gl=c['gl'], bc=c['bc'], gc=c['gc'])

def score_seed(name, r):
    p = W[name]; c = r['consensus']; d = design_of(c)
    gap = J_theory(name, d) / PR[name]['J_star'] - 1
    if name in GENOME_STRUCTURE_WORLDS:
        structure = c['structure']; counted = None
        pred_struct = PR[name]['design']
    else:
        counted = cr.count(d, tuple(p['count_band']), lead=int(p.get('lead', 0))); structure = counted['structure']
        pred_struct = pred_counted(name)['structure']
    L = r['log']; G = len(L); m = np.array([x['med_cost'] for x in L])
    w1, w2 = m[int(0.8 * G):int(0.9 * G)], m[int(0.9 * G):]
    se = np.sqrt(w1.var(ddof=1) / len(w1) + w2.var(ddof=1) / len(w2))
    improving = bool((w1.mean() - w2.mean()) > max(3 * se, EPS_BAND * PR[name]['J_star']))
    dead = float(np.mean([x['dead'] for x in L[int(0.9 * G):]]) / r['P'])
    out = dict(seed=r['seed'], start=r['start'], structure_genome=c['structure'], structure_frac=c['structure_frac'],
               counted=counted, structure_scored=structure, predicted_structure=pred_struct,
               J_gap=float(gap), miss_A=bool(gap > EPS_BAND), miss_B=bool(structure != pred_struct),
               bl=c['bl'], gl=c['gl'], bc=c['bc'], gc=c['gc'], improving_at_end=improving, final_dead_frac=dead)
    out['miss'] = out['miss_A'] or out['miss_B']
    # secondary: rates against the predicted counted poles (same structure only)
    if not out['miss_B']:
        if name in GENOME_STRUCTURE_WORLDS:
            ev = list(c['bl']) + list(c['bc']); pr = PR[name]['bl'] + PR[name]['bc']
        else:
            ev = counted['local'] + counted['shared']; pc = pred_counted(name); pr = pc['local'] + pc['shared']
        bands = rate_bands(name)
        if len(bands) != len(pr): bands = [min(bands)] * len(pr)
        dl = [float(np.log(e_ / p_)) for e_, p_ in zip(ev, pr)]
        out['rate_dlog'] = dl; out['rate_band'] = bands; out['rates_in_band'] = bool(all(abs(x) <= b for x, b in zip(dl, bands)))
        if name == 'W2':
            a = sorted(p['a']); b = sorted(ev); out['interlacing'] = bool(a[0] < b[0] < a[1] < b[1])
        if p['kind'] == 'storenoise':
            out['lam_tau'] = float(p['lam'] / ev[0]); out['slower_than_mode'] = bool(p['lam'] / ev[0] > 1)
    return out

def verdict(m):
    return 'PASSED' if m <= 1 else ('INCONCLUSIVE' if m == 2 else 'FAILED')

def main(rundir):
    res = {'EPS_BAND': EPS_BAND, 'worlds': {}}
    for name in TEST_WORLDS:
        runs = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(rundir, f'{name}_s*.json'))) if not f.endswith('_null.json')]
        nulls = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(rundir, f'{name}_s*_null.json')))]
        seeds = [score_seed(name, r) for r in runs]; nseeds = [score_seed(name, r) for r in nulls]
        scored = [s for s in seeds if not s['improving_at_end']]
        m = sum(s['miss'] for s in scored)
        o = PR[name]; Jst = o['J_star']
        rivals = {}
        for k, v in o['rivals'].items():
            J = v['J'] if isinstance(v, dict) else v
            if isinstance(J, (int, float)) and np.isfinite(J) and J > Jst * (1 + 1e-9):
                gap = J / Jst - 1; rivals[k] = dict(gap=float(gap), sNe=float(EV['beta'] * EV['P'] * gap), excluded_by_band=bool(gap > EPS_BAND))
        nearest = min((v['sNe'] for v in rivals.values()), default=np.inf)
        null_pass = sum((not s['miss']) for s in nseeds)
        invalid = []
        if len(scored) < 6: invalid.append(f'only {len(scored)} converged seeds (< 6)')
        if nseeds and null_pass >= len(nseeds) / 2: invalid.append(f'null (drift) control meets the criteria in {null_pass}/{len(nseeds)} seeds')
        if nearest < 10: invalid.append(f'nearest rival sNe = {nearest:.1f} < 10')
        if seeds and np.mean([s['final_dead_frac'] for s in seeds]) > 0.10: invalid.append('ruin binding (final-window deaths > 10%)')
        res['worlds'][name] = dict(n_seeds=len(seeds), n_scored=len(scored), misses=int(m), misses_A=int(sum(s['miss_A'] for s in scored)),
                                   misses_B=int(sum(s['miss_B'] for s in scored)), verdict_raw=verdict(m) if scored else 'NO RUNS',
                                   invalid_reasons=invalid, seeds=seeds, null_seeds=nseeds, null_meets_criteria=int(null_pass), rivals=rivals)
    pc = res['worlds']['PC']
    for name, w in res['worlds'].items():
        v = w['verdict_raw']
        if w['invalid_reasons']: v = 'INVALID'
        if name != 'PC' and (pc['verdict_raw'] != 'PASSED' or pc['invalid_reasons']): v = 'INVALID'; w['invalid_reasons'].append('positive control not PASSED')
        w['verdict'] = v
    # design moves with a change in its inputs (PREREG §6): PC -> W1 (speed price), S031 -> S07 (store-noise exponent)
    def med_lograte(name):
        xs = [np.log(s['counted']['local'][0]) for s in res['worlds'][name]['seeds'] if s['counted'] and s['counted']['local'] and not s['miss_B']]
        return (float(np.median(xs)) if xs else None), len(xs)
    moves = {}
    for a_, b_, pa, pb in (('PC', 'W1', PR['PC']['counted']['local'][0], PR['W1']['counted']['local'][0]),
                           ('S031', 'S07', PR['S031']['counted']['local'][0], PR['S07']['counted']['local'][0])):
        ma, na = med_lograte(a_); mb, nb_ = med_lograte(b_)
        pred = float(np.log(pb / pa)); tol = float(np.hypot(rate_bands(a_)[0], rate_bands(b_)[0]))
        if ma is None or mb is None: moves[f'{a_}->{b_}'] = dict(pred_dlog=pred, verdict='NO DATA'); continue
        obs = mb - ma
        moves[f'{a_}->{b_}'] = dict(pred_dlog=pred, obs_dlog=obs, tol=tol, n=(na, nb_),
                                    verdict='PASSED' if (np.sign(obs) == np.sign(pred) and abs(obs - pred) <= tol) else 'FAILED')
    res['moves'] = moves
    # store-noise threshold (PREREG §6): S031 slower than its mode, S07 faster, in >= 7 of 8 seeds each
    th = {}
    for name, want in (('S031', True), ('S07', False)):
        ss = [s for s in res['worlds'][name]['seeds'] if 'slower_than_mode' in s]
        k = sum(s['slower_than_mode'] == want for s in ss)
        th[name] = dict(want_slower=want, agree=k, n=len(ss), verdict='PASSED' if (ss and k >= len(ss) - 1 and len(ss) >= 6) else ('FAILED' if ss and len(ss) - k >= 3 else 'INCONCLUSIVE'))
    res['store_noise_threshold'] = th
    # interlacing (W2)
    ss = [s for s in res['worlds']['W2']['seeds'] if 'interlacing' in s]
    k = sum(s['interlacing'] for s in ss)
    res['W2_interlacing'] = dict(agree=k, n=len(ss), verdict='PASSED' if (ss and len(ss) - k <= 1) else ('FAILED' if ss and len(ss) - k >= 3 else 'INCONCLUSIVE'))
    json.dump(res, open(os.path.join(HERE, 'ANALYSIS_EVO.json'), 'w'), indent=1, default=float)
    for name, w in res['worlds'].items():
        print(f"{name}: {w['verdict']} (raw {w['verdict_raw']}; misses {w['misses']}/{w['n_scored']} [A {w['misses_A']}, B {w['misses_B']}]; "
              f"null meets {w['null_meets_criteria']}/{len(w['null_seeds'])}; invalid: {w['invalid_reasons']})")
    print('moves', json.dumps(moves)); print('threshold', json.dumps(th)); print('W2 interlacing', res['W2_interlacing'])
    return res

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'runs'))
