"""Calibration of tA_discrete.py's definition in the near-continuous limit (t_A >> 1 step)."""
import numpy as np
from tA_discrete import run, EG
for sig, lam in ((6.0, 0.0005), (10.0, 0.0002)):
    N = sig**2; f = N/2*(np.log(2/(lam*N)) - EG - 1); m, se = run(sig, lam, nsw=600, seed=11)
    print(f"sigma {sig} lam {lam}: plug-in t_A {f:7.2f}; discrete crossing {m:7.2f} +- {se:.2f}; ratio {m/f:.3f}")
