# pipeline smoke test on OUT-OF-DESIGN cells (rho=0.5, rho=0.7); prints only timing + structure, not outcomes.
import time, os, json, run_onset as ro
os.nice(19)
for arm in ['RR', 'AA']:
    t0 = time.time()
    r = ro.job((arm, 'smoke', 0.5, 1.0, 10.0 if arm == 'RR' else 200.0, 0, 'es'))
    print(arm, 'seconds', round(time.time() - t0, 1), 'keys', sorted(r.keys()), 'nrows', len(r['rows']))
