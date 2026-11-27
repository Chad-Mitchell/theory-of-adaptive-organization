# Gate reader v3 diagnostic of the locked run_t2_v2 minimizer settings. NOT a scored run:
# no --execute, no run_setting(), no labels; non-locked seeds; J and A values are not printed.
import os
for k in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"): os.environ[k]="1"
import sys, time, collections
sys.path.insert(0, os.getcwd())
import numpy as np
from scipy.optimize import minimize
import run_t2_v2 as t2
w, wx = 10, 1
opts = {"ftol": t2.FTOL, "gtol": t2.GTOL, "maxiter": t2.MAXITER, "maxfun": t2.MAXFUN}
half = {"ftol": t2.FTOL/2, "gtol": t2.GTOL/2, "maxiter": t2.MAXITER, "maxfun": t2.MAXFUN}
rng = np.random.default_rng(424242)            # not a locked seed
starts = [("uniform", t2.draw_stable(rng)) for _ in range(8)]
c = t2.C_SYM[(w, wx)]; base = t2.pack(np.full(8,5.0), np.full(8,c), np.full(8,c))
rp = np.random.default_rng(777)                # not a locked seed
starts += [("near-uniform", t2.clip_box(base + rp.uniform(-0.05,0.05,24))) for _ in range(2)]
T0 = time.process_time(); tally = collections.Counter(); conv = []
for n,(kind,x0) in enumerate(starts):
    t = time.process_time()
    r = minimize(lambda v: t2.Jtot(v,w,wx), x0, method="L-BFGS-B", bounds=t2.BOUNDS, options=opts)
    lim = t2.stopped_on_limit(r); tally[(int(r.status), lim)] += 1
    if not lim: conv.append(x0)
    print(f"start {n:2d} {kind:12s} status={r.status} nit={r.nit:4d} nfev={r.nfev:5d} stopped_on_limit={lim} cpu={time.process_time()-t:5.2f}s msg={r.message}")
for n,x0 in enumerate(conv[:2]):
    t = time.process_time()
    r = minimize(lambda v: t2.Jtot(v,w,wx), x0, method="L-BFGS-B", bounds=t2.BOUNDS, options=half)
    print(f"half-tol rerun {n} status={r.status} nit={r.nit} nfev={r.nfev} stopped_on_limit={t2.stopped_on_limit(r)} cpu={time.process_time()-t:5.2f}s msg={r.message}")
print("tally (status, stopped_on_limit):", dict(tally), " total probe CPU %.1f s" % (time.process_time()-T0))
