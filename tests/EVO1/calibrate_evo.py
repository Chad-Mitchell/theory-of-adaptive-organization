#!/usr/bin/env python3
"""EVO1 pre-lock calibration (NO evolution, NO selection): evaluate the theory's predicted design and each rival design
as FIXED designs in the simulator over independent worlds, to check that the simulator charges the costs the world
specification states (cost level at the predicted design vs J*) and to measure fitness noise per generation.
It does not search the realized-cost landscape (that would pre-run the test).  Run: nice -n 19 python3 calibrate_evo.py
Writes CALIBRATION_EVO.json."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import evo
W = json.load(open(os.path.join(HERE, 'worlds.json')))['worlds']
PR = json.load(open(os.path.join(HERE, 'PREDICTIONS_EVO.json')))
REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 40
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'figures'))

def designs(name):
    p, o = W[name], PR[name]
    if p['kind'] == 'ou':
        import predict_evo as pe
        D = {'predicted': (o['bl'], o['gl'], o['bc'], o['gc'])}
        for k, v in o['all_designs'].items():
            if k in ('0L0S',): continue
            gl, gc = pe.readout_ou(p, v['bl'], v['bc']); D['alt_' + k] = (v['bl'], gl, v['bc'], gc)
        return D
    if p['kind'] == 'rw':
        b = o['b'][0]
        return {'predicted': ([b], [1.0], [], []), 'alt_2stores': ([b, 3 * b], [1.0, 0.0], [], []),
                'alt_half_rate': ([b / 2], [1.0], [], []), 'alt_double_rate': ([2 * b], [1.0], [], [])}
    import predict_evo as pe
    D = {'predicted': ([1 / x for x in o['taus']], o['g'], [], [])}
    for k, v in o['all_designs'].items():
        if v['taus']: D['alt_K' + k] = ([1 / x for x in v['taus']], pe.readout_sp(p, v['taus']), [], [])
    K = len(o['taus']); t = [1 / p['lam']] * K
    D['rival_set_at'] = ([p['lam']] * K, pe.readout_sp(p, t), [], [])
    return D

if __name__ == '__main__':
    out = {}
    for name in W:
        if 'income' not in W[name]: continue
        D = designs(name); keys = list(D)
        c = evo.evaluate(name, [D[k][0] for k in keys], [D[k][1] for k in keys], [D[k][2] for k in keys], [D[k][3] for k in keys], REPS, seed=11)
        Jst = PR[name]['J_star']; m = c.mean(0); se = c.std(0, ddof=1) / np.sqrt(REPS)
        diffs = c - c[:, [0]]
        out[name] = dict(J_star=Jst, reps=REPS, designs=keys,
                         realized_mean=m.tolist(), realized_se=se.tolist(),
                         delta_sim=float((m[0] - Jst) / Jst), delta_sim_se=float(se[0] / Jst),
                         paired_diff_mean_frac=(diffs.mean(0) / m[0]).tolist(),
                         paired_diff_sd_frac_per_generation=(diffs.std(0, ddof=1) / m[0]).tolist(),
                         realized_cost_sd_frac_per_generation=float(c[:, 0].std(ddof=1) / m[0]))
        print(name, json.dumps({k: (np.round(v, 5).tolist() if (isinstance(v, list) and v and not isinstance(v[0], str)) else v) for k, v in out[name].items()}), flush=True)
    json.dump(out, open(os.path.join(HERE, 'CALIBRATION_EVO.json'), 'w'), indent=1)
