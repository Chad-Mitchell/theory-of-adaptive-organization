#!/usr/bin/env python3
"""Measured coordinates for E. coli chemotaxis (written after ECOLI-MEM; a measurement summary, not a test).
Every input is cited in README.md section E.5; assumptions are marked ASSUMED. Writes measured.json."""
import json, math
lam, lam_se = 0.862, 0.005                      # Mattingly 2021 Table S1
tau_v = 1 / lam; tau_v_lo, tau_v_hi = 1 / (lam + 2 * lam_se), 1 / (lam - 2 * lam_se)
ell_c, ell_lo, ell_hi = 0.20, 0.04, 0.30        # s: Segall 1982 0.23+-0.07 (iontophoresis); Jasuja 1999 0.07+-0.03 (photorelease)
y = dict(central=ell_c / tau_v, lo=ell_lo / tau_v_hi, hi=ell_hi / tau_v_lo)
y_log = {k: math.log10(v) for k, v in y.items()}
# upkeep: proteome share of the chemotaxis signalling machinery (receptor array + Che proteins)
L = dict(rec=552, cheA=654, cheW=167, cheY=129, cheZ=214, cheB=349, cheR=286)   # UniProt P07017/P02942 (avg), P07363, ...
def aa(rec, cheA):                                  # Li & Hazelbauer 2004: ratios per CheA monomer / per core complex
    core = cheA / 2
    n = dict(rec=rec, cheA=cheA, cheW=1.2 * cheA, cheY=2.4 * core, cheZ=2 * 0.5 * core, cheB=0.08 * core, cheR=0.05 * core)
    return sum(n[k] * L[k] for k in n)
aa_rich, aa_min = aa(14000, 6700), aa(24000, 7700)
tot_lo, tot_hi = 2e6 * 300, 4e6 * 300               # ASSUMED: 2-4 million proteins/cell x ~300 aa
share_lo, share_hi = aa_rich / tot_hi, aa_min / tot_lo
# stakes proxy (Ni et al. 2020): benefit of chemotaxis in poor carbon exceeds the cost of motility ("several percent",
# Ni citing refs 9,10) and is at most of order the whole growth rate ("almost twice as fast" in one phase on ribose).
ben_lo, ben_hi = 0.02, 1.0                          # lower = "several percent" read as >= 2%; upper = order one
R_lo, R_hi = ben_lo / share_hi, ben_hi / share_lo
out = dict(
    system="E. coli chemotaxis (lab strain RP437-type, MeAsp, Mattingly et al. 2021 conditions)",
    current_map=dict(
        loglat=dict(central=y_log["central"], lo=y_log["lo"], hi=y_log["hi"],
                    definition="l / tau_fast, l = stimulus-to-motor latency, tau_fast = 1/lambda_tot (signal correlation time)"),
        logR_proxy=dict(lo=math.log10(R_lo), hi=math.log10(R_hi), central_for_plotting=0.5 * (math.log10(R_lo) + math.log10(R_hi)),
                        definition="PROXY, not w*Var/h: fitness benefit of chemotaxis (Ni 2020, poor carbon) / proteome share of the signalling machinery",
                        rich_medium="benefit ~ 0 on glucose (Ni 2020): R_proxy < 1; the cell cuts motility investment there"),
        guess_it_replaces=dict(logR=1.0, loglat=-0.5)),
    raw_dimensionless=dict(
        lambda_tau2=dict(value=9.9 * lam, lo=(9.9 - 0.6) * (lam - 2 * lam_se), hi=(9.9 + 0.6) * (lam + 2 * lam_se),
                         meaning="slow-layer memory / world signal correlation time"),
        tau1_over_tau_v=dict(fit=0.22 * lam, kinase=0.017 * lam, meaning="fast-layer time / world signal correlation time"),
        taun_over_tau2=dict(value=11.75 / 9.9, meaning="noise correlation time / memory: ~1 means the noise is the store's own"),
        bp_share_of_noise=dict(lo=1.0e-6, hi=2.2e-4, meaning="Berg-Purcell counting noise / measured kinase-noise variance (ecoli/results.json)"),
        snr_armB=dict(lo=0.0043, hi=0.103, meaning="2 sigma_u^2/(lambda N_s) at g = 0.1-0.4 /mm; scales as g^2"),
        stores_measured=2, world_degree=2,
        upkeep_share_proteome=dict(lo=share_lo, hi=share_hi, meaning="signalling-machinery amino acids / all protein amino acids (ASSUMED total)"),
        adaptation_power=dict(value_kT_per_s=3e4, meaning="Lan 2012: ~3x10^4 kT/s (~10^3 ATP/s), 5-10% of one flagellar motor's cost"),
        benefit_fraction=dict(lo=ben_lo, hi=ben_hi, meaning="relative fitness benefit of chemotaxis, poor carbon, Ni 2020 (read from text, not figures)")),
)
json.dump(out, open("measured.json", "w"), indent=1)
print(json.dumps(out, indent=1))
