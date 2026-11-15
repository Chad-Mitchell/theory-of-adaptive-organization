"""POST HOC (after c1_data.py; descriptive only): paired sd of W(z) - W(ybar) on common rows; simulated sum of
kernel weights for the realized-mean-log response and for a noiseless best linear tracker (planned n)."""
import numpy as np, json, os
os.environ.pop('DRY', None)
import runpy
from plib import *
g = runpy.run_path('c1_data.py', run_name='lib')    # re-runs c1 (same seed) and exposes its objects
A = g['boot_fit'](g['X'], {'ybar': g['tgt']['ybar'], 'z': g['tgt']['z']}, g['rows'])
bz, bb = A['_boot']['z'], A['_boot']['ybar']
rng = np.random.default_rng(20261135); w = blp_weights(2000); sb, sm = [], []
for k in range(100):
    _, y = driver(9276 + 1000, rng); m = np.convolve(y, w)[:len(y)][1000:]; y = y[1000:]
    X, t = binmat(y); rows = t <= len(y) - H - 1
    sb.append(ols(X[rows], fut_mean(y)[t][rows])[1:].dot(np.diff(EDGES))); sm.append(ols(X, m[t])[1:].dot(np.diff(EDGES)))
out = {'Delta_z_ybar': A['z']['W21'] - A['ybar']['W21'], 'sd_paired': float(np.std(bz - bb, ddof=1)),
       'corr_boot_z_ybar': float(np.corrcoef(bz, bb)[0, 1]),
       'sim_sum_beta_ybar': [float(np.mean(sb)), float(np.std(sb, ddof=1))], 'sim_sum_beta_blp': [float(np.mean(sm)), float(np.std(sm, ddof=1))]}
json.dump(out, open('c3_posthoc.json', 'w'), indent=1); print(out)
