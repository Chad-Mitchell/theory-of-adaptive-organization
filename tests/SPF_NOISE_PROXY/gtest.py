#!/usr/bin/env python3
"""Overidentification test of the white-sensing-noise premise, calibrated by parametric bootstrap under H0.
G = ln K-hat_L3 - ln K-hat_L0 (level-normalised dispersion at h=3 vs h=0, same environment fit). Under H0 (pure noisy
information, THEORY §2.2 memory-time premise "white observation noise") G ~ its simulated null: panels simulated from the
fitted environment with K = K-hat_L0 and the observed panel layout size (T, ~nf forecasters), environment re-fitted in every
simulation. One-sided p = (1 + #{G_sim >= G_obs}) / (1 + NSIM).
"""
import numpy as np
import common, model
import synth_dryrun as sd

def g_stat(pan, xenv):
    k, aux = sd.proxies(pan, xenv)
    return float(np.log(k["L3"][0] / k["L0"][0])), k, aux

def g_light(pan, xenv):
    """Same G as g_stat (identical L3/L0 computations), skipping the unused candidates."""
    fit = model.whittle_fit(xenv); var_x = common.env_scale(xenv, fit)
    S = model.env_grid(fit["tauE"], fit["alpha"], fit["phi"])
    st = {h: common.panel_stats(*pan[h], h) for h in (0, 3)}
    nf = st[0]["nf"]
    k3 = common.invert_lower(common.level_curve(S, 3, nf), st[3]["D_raw"] / var_x)[0]
    k0 = common.invert_lower(common.level_curve(S, 0, nf), st[0]["D_raw"] / var_x)[0]
    return float(np.log(k3 / k0))

def null_G(fit, K0, T, nf, nsim, rng):
    out = []
    for _ in range(nsim):
        pan, xenv = common.synth_panel(fit, K0, "a", 0.0, rng, T=T, active=int(round(nf)))
        out.append(g_light(pan, xenv))
    return np.array(out)

def pval(G, null):
    return float((1 + np.sum(null >= G)) / (1 + len(null)))
