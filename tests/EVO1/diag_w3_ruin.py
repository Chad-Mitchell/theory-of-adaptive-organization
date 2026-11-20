#!/usr/bin/env python3
"""DEVIATIONS D1c, second part: who dies under the locked W3 ruin gate?  The evolved consensus design of each W3 seed and
300 one-step mutants of it (the locked mutate()) are run as fixed designs with the locked income and buffer over 40 worlds.
Run: nice -n 19 python3 diag_w3_ruin.py   (writes diag/D1c_ruin.json)"""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import evo
cfg = json.load(open(os.path.join(HERE, 'worlds.json'))); p = cfg['worlds']['W3']; E = dict(cfg['evolution']); E.update(p['evolution'])
out = []
for f in sorted(glob.glob(os.path.join(HERE, 'runs', 'W3_s[0-7].json'))):
    r = json.load(open(f)); c = r['consensus']; rng = np.random.default_rng([r['seed'], 99])
    P = 301; pop = evo.Pop(P); pop.nl[:] = len(c['bl']); pop.bl[:, :len(c['bl'])] = c['bl']; pop.gl[:, :len(c['gl'])] = c['gl']
    mut = evo.mutate(pop.take(np.arange(1, P)), p, E, rng)
    allp = pop.take(np.arange(P))
    for k in ('nl', 'nc', 'bl', 'gl', 'bc', 'gc'): getattr(allp, k)[1:] = getattr(mut, k)
    dead = np.zeros(P); T = p['burn'] + p['T_score']
    for rep in range(40):
        s, y, ybar = evo.make_world(p, T, rng)
        cost, alive, mse = evo.live(s, y, ybar, allp.nl, allp.bl, allp.gl, allp.nc, allp.bc, allp.gc, p['h'], p['h'], 0.0, p['w'], 0,
                                    p['burn'], False, 0.5, 0.0, 1.0, p['income'], p['buffer_steps'] * p['income'], int(rng.integers(1, 2**31 - P)))
        dead += ~alive
    dev = np.abs(allp.gl[:, :allp.nl.max()].sum(1) - 1.0)
    out.append(dict(seed=r['seed'], consensus_death_rate=float(dead[0] / 40), mutant_death_rate=float(dead[1:].mean() / 40),
                    death_rate_by_weight_sum_error={f'<{q}': float(dead[1:][dev[1:] < q].mean() / 40) if (dev[1:] < q).any() else None for q in (0.005, 0.01, 0.02)},
                    death_rate_weight_sum_error_ge_0p02=float(dead[1:][dev[1:] >= 0.02].mean() / 40) if (dev[1:] >= 0.02).any() else None))
    print(out[-1], flush=True)
json.dump(out, open(os.path.join(HERE, 'diag', 'D1c_ruin.json'), 'w'), indent=1)
