"""Continuous-time closed form (reset reads, cost K q^(1/alpha) per unit stakes): onset solves
N^(1/a-1) rho^(1/a) = (1+rho)^(1/a) - 1 (bundled loss, no cross term). Never imported by world.py."""
import numpy as np
from scipy.optimize import brentq
def nstar(alpha, rho):
    a = 1 / alpha
    f = lambda lnN: (a - 1) * lnN + a * np.log(rho) - np.log((1 + rho) ** a - 1)
    return float(np.exp(brentq(f, -20, 40)))
def window_exponent(alpha, rhos):
    return float(np.polyfit(np.log(rhos), np.log([nstar(alpha, r) for r in rhos]), 1)[0])
if __name__ == '__main__':
    R = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
    for al in (1.5, 2.0, 2.5):
        print(al, [round(nstar(al, r), 1) for r in R], round(window_exponent(al, R), 4))
