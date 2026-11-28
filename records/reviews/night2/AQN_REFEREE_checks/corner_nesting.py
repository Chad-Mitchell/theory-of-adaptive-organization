"""Corner model in aqn.whittle_corner_fit truncates the alias sum at |k| <= 6 with no tail term; the base model adds
an Euler-Maclaurin tail. Size of the mismatch as w0 -> 0, relative to the signal at each frequency, and whether a white
noise term absorbs it (formula re-typed here from the source, compared with the exact Hurwitz-zeta sum)."""
import numpy as np, sys
sys.path.insert(0, '.')
from ownlib import alias_exact
w = np.linspace(0.01, np.pi, 400)
for a in (1.4, 2.0, 2.6):
    trunc = w**-a + sum((w + 2*np.pi*k)**-a + (2*np.pi*k - w)**-a for k in range(1, 7))
    ex = alias_exact(w, a); miss = ex - trunc
    print(f"alpha {a}: missing tail / exact sum: at w=0.01 {miss[0]/ex[0]:.2e}, at w=pi {miss[-1]/ex[-1]:.3f}; tail variation across band (max/min) {miss.max()/miss.min():.3f} (1.000 = exactly white, absorbed by s2)")
