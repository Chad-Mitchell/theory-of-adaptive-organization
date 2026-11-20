"""How large can the flat-vs-layered penalty get? Two OU modes tau=1 and 1e4; scan slow-variance share, noise, lead.
Run: nice -n 19 python3 maxgain.py > maxgain.out"""
import numpy as np
from lead import E_opt, E_K_lead
best = []
a = 1/np.array([1., 1e4])
for share in [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    v = np.array([1-share, share])
    for N in [1e-4, 1e-3, 1e-2, 1e-1, 1, 10]:
        for k in [0, 0.3, 1, 3]:
            eo = E_opt(a, v, N, k); e1 = E_K_lead(a, v, N, 1, k, starts=6)
            best.append((e1/eo-1, share, N, k, eo))
best.sort(reverse=True)
for b in best[:8]: print("excess %.1f%%  slow share %.2f  noise %g  lead %g  optMSE %.4f" % (b[0]*100, *b[1:]))
