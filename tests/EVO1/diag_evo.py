#!/usr/bin/env python3
"""EVO1 post-lock diagnostics (DEVIATIONS_EVO.md D1).  Uses the locked simulator unchanged; changes are made from outside
(initial population, the new-store weight, or the buffer) and written into a separate worlds file under diag/.
Run: nice -n 19 python3 diag_evo.py D1a|D1b|D1c SEED"""
import os, sys, json, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import evo
which, seed = sys.argv[1], int(sys.argv[2])
D = os.path.join(HERE, 'diag', which); os.makedirs(D, exist_ok=True)
cfg = json.load(open(os.path.join(HERE, 'worlds.json')))
if which == 'D1c':
    cfg['worlds']['W3']['buffer_steps'] *= 10
json.dump(cfg, open(os.path.join(D, 'worlds.json'), 'w'), indent=1)
for f in ('evo.py',): shutil.copy(os.path.join(HERE, f), D)
evo.HERE = D                                       # the locked code, reading the diagnostic worlds file
world = 'W3' if which == 'D1c' else ('W4' if which == 'D2b' else 'W4b')
if which == 'D1a':
    PR = json.load(open(os.path.join(HERE, 'PREDICTIONS_EVO.json')))['W4b']
    def init_at_prediction(p, E, P, start, rng):
        pop = evo.Pop(P)
        pop.nl[:] = 1; pop.bl[:, 0] = PR['bl'][0]; pop.gl[:, 0] = PR['gl'][0]
        pop.nc[:] = 1; pop.bc[:, 0] = PR['bc'][0]; pop.gc[:, 0] = PR['gc'][0]
        return pop
    evo.init_pop = init_at_prediction
if which in ('D1b', 'D2b'):
    _mut = evo.mutate
    def mutate_new_store_weight(pop, p, E, rng):
        before_l, before_c = pop.nl.copy(), pop.nc.copy()
        pop = _mut(pop, p, E, rng)
        for nk, gk, b4 in (('nl', 'gl', before_l), ('nc', 'gc', before_c)):
            born = np.flatnonzero((b4 == 0) & (getattr(pop, nk) == 1) & (getattr(pop, gk)[:, 0] == 0.0))   # created from nothing (weight exactly 0), not a class switch
            getattr(pop, gk)[born, 0] = 0.3 * rng.standard_normal(len(born))
        return pop
    evo.mutate = mutate_new_store_weight
evo.run(world, seed, False, os.path.join(D, 'runs'))
