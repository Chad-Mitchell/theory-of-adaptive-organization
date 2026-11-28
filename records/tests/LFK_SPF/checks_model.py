#!/usr/bin/env python3
"""Pre-lock dry run on synthetic truth (MV7 known-groups, MV9). Not an outcome computation."""
import numpy as np, json, sys
from model import *
out = {}
# 1. AR(1)/Markov check: alpha=2, phi=0, continuous OU sampled -> AR(1) with rho=exp(-1/tauE). Noisy-info theory:
#    beta=(1-G)/G with G the steady-state Kalman gain of x_t=rho x_{t-1}+e, y=x+v.
for tau in (1.0, 4.0, 16.0):
    for K in (0.1, 1.0):
        rho = np.exp(-1 / tau); q = 1 - rho ** 2
        P = 1.0
        for _ in range(10000):
            Pm = rho ** 2 * P + q; G = Pm / (Pm + K); P = (1 - G) * Pm
        b = moments(env_grid(tau, 2.0, 0.0), K)[0]
        out[f"ar1_tau{tau}_K{K}"] = dict(beta=b, theory=(1 - G) / G)
        print(f"AR(1) tau={tau:5.1f} K={K}: beta={b:.4f}  (1-G)/G={(1-G)/G:.4f}")
# grid refinement for tauE >= 200 (the analysis grid M=2^13 resolves corners only for tauE <~ 1000/2pi; real-data E3 keeps tauE < 60)
import model as _m
_m.M = 2 ** 17; _m._W = 2 * np.pi * np.arange(_m.M) / _m.M; _m._Wsym = np.where(_m._W > np.pi, _m._W - 2 * np.pi, _m._W)
from model import _W
# 2. Prop. 5 in-model: slope of log beta on log tauE (phi=0, small K, large tauE) vs 1-1/alpha
for a in (1.5, 2.0, 2.5, 3.0):
    taus = np.array([200., 400., 800., 1600.])
    bs = np.array([moments(env_grid(t, a, 0.0), 0.3)[0] for t in taus])
    sl = np.polyfit(np.log(taus), np.log(bs), 1)[0]
    out[f"prop5_alpha{a}"] = dict(slope=sl, theory=1 - 1 / a)
    print(f"Prop5 asymptotic: alpha={a}: slope(log beta, log tauE)={sl:.3f}  1-1/alpha={1-1/a:.3f}")
json.dump(out, open("results/checks_model.json", "w"), indent=1)
# 3. Fixed high-frequency level q (referee): scale variance so that q is constant while tauE moves -> slope ~ 0
for a in (1.5, 2.5):
    taus = np.array([200., 400., 800., 1600.]); bs = []
    for t in taus:
        S = env_grid(t, a, 0.0); qrel = t ** (1 - a)          # q of the unit-variance world, up to c_a
        bs.append(moments(S, 0.3 * qrel / 200. ** (1 - a))[0])  # noise in units of var: K scales with q -> fixed N/q
    sl = np.polyfit(np.log(taus), np.log(bs), 1)[0]
    out[f"fixed_q_alpha{a}"] = dict(slope=sl, theory=0.0)
    print(f"Fixed q: alpha={a}: slope={sl:.3f} (referee: 0)")
json.dump(out, open("results/checks_model.json", "w"), indent=1)
