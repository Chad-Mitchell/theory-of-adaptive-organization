"""Base-model alias sum (aqn.alias_sum formula re-typed: |k|<=6 plus Euler-Maclaurin midpoint tail) vs exact Hurwitz zeta."""
import numpy as np, sys
sys.path.insert(0, '.')
from ownlib import alias_exact
w = np.linspace(0.001, np.pi, 2000)
for a in (1.02, 1.4, 2.0, 2.6, 2.98):
    s = w**-a + sum((w + 2*np.pi*k)**-a + (2*np.pi*k - w)**-a for k in range(1, 7))
    s += ((w + 2*np.pi*6.5)**-(a-1) + (2*np.pi*6.5 - w)**-(a-1))/(2*np.pi*(a-1))
    print(f"alpha {a}: max relative error {np.max(np.abs(s/alias_exact(w, a) - 1)):.2e}")
