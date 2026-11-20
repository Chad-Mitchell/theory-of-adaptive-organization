"""Summaries for theory/HT_INDEX.md from arm_*.json; adds the plug-in K* (Whittle fit -> repo optimizer). nice -n 19 python3 analyse.py"""
import json, os, sys
import numpy as np
from multiprocessing import Pool
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'layers_checks'))
from stores import E_K, E_inf

Rs = ['10', '100', '1000', '10000', '1000000']
DT = 0.1


def plugin(fit):
    taus, vs, N = np.array(fit['taus'], float), np.array(fit['vs'], float), fit['N']
    if taus.size == 0:
        return {R: 0 for R in Rs}
    a = 1 / taus; Nc = N * DT
    ei = E_inf(a, vs, Nc); rows = []
    for K in range(1, min(4, len(a) + 1) + 1):
        e, _ = E_K(a, vs, Nc, K, starts=6)
        rows.append((K, (e - ei) / ei))
    return {R: min(rows, key=lambda r: r[0] + float(R) * (1 + r[1]))[0] for R in Rs}


def main():
    B = json.load(open(os.path.join(HERE, 'arm_B.json')))
    Kt = {(tuple(r['taus']), r['noise']): r['kstar'] for r in json.load(open(os.path.join(HERE, 'arm_K.json')))}
    ou = [r for r in B if r['kind'] == 'ou']
    for r in ou:
        r['J'] = len(r['par']); r['kstar'] = Kt[(tuple(float(t) for t in r['par']), r['noise'])]
    big = [r for r in ou if r['n'] == 200000]
    with Pool(6) as p:
        pk = p.map(plugin, [r['whittle_fit'] for r in big])
    for r, k in zip(big, pk):
        r['plugin_kstar'] = k
    est = ['ht_absdy', 'ht_absdy_t05', 'ht_absy', 'ht_per', 'ht_cross', 'whittle', 'peaks', 'dfa_h', 'mf_width']
    out = {'per_n': {}}
    for n in (20000, 200000):
        sub = [r for r in ou if r['n'] == n]; J = np.array([r['J'] for r in sub]); res = {}
        for e in est:
            x = np.array([r[e] for r in sub], float)
            rho_J = spearmanr(x, J).statistic if np.std(x) > 0 else float('nan')
            res[e] = dict(spearman_J=None if np.isnan(rho_J) else round(float(rho_J), 3),
                          exact_J=round(float(np.mean(x == J)), 3),
                          spearman_kstar={R: (None if np.std(x) == 0 else round(float(spearmanr(x, [r['kstar'][R] for r in sub]).statistic), 3)) for R in Rs},
                          exact_kstar={R: round(float(np.mean(x == np.array([r['kstar'][R] for r in sub]))), 3) for R in Rs})
        out['per_n'][str(n)] = res
    out['plugin_exact_kstar'] = {R: round(float(np.mean([r['plugin_kstar'][R] == r['kstar'][R] for r in big])), 3) for R in Rs}
    out['whittle_as_kstar_exact_n200k'] = {R: round(float(np.mean([min(r['whittle'], 99) == r['kstar'][R] for r in big])), 3) for R in Rs}
    out['plugin_detail'] = [dict(par=r['par'], noise=r['noise'], kstar=r['kstar'], plugin=r['plugin_kstar'], whittle=r['whittle']) for r in big]
    # scale-free controls: pole count vs n
    out['scalefree_poles'] = {}
    for r in B:
        if r['kind'] != 'ou':
            out['scalefree_poles'].setdefault(f"{r['kind']} {r['par']} n={r['n']}", []).append(r['whittle'])
    # ht growth with n (OU worlds, 0.5 threshold) by J
    out['ht_t05_by_J_n'] = {f"J={j} n={n}": float(np.mean([r['ht_absdy_t05'] for r in ou if r['J'] == j and r['n'] == n])) for j in (1, 2, 3, 4) for n in (20000, 200000)}
    json.dump(out, open(os.path.join(HERE, 'summary.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'plugin_detail'}, indent=1))


if __name__ == '__main__':
    main()
