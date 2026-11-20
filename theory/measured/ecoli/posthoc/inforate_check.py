#!/usr/bin/env python3
"""POST HOC unit check of arm B's noise referral (written after the run; does not change any verdict).
Low-SNR information rate with white input-referred noise N_s: I = sigma_u^2 / (2 ln2 N_s) bits/s,
to compare with Mattingly et al.'s beta = 0.225 +- 0.032 bits/s/mm^-2 (their N(w) is OU-shaped, not white)."""
import math
G, t1, t2, sn, tn, av = 1.73, 0.22, 9.9, 0.092, 11.75, 157.1
for t1 in (0.22, 0.017):
    K0 = G * t2 * t2 / (t1 + t2)
    Ns = 2 * sn * sn * tn / K0 ** 2
    beta = av * 1e-6 / (2 * math.log(2) * Ns)   # per (1/mm)^2
    print(f"tau1={t1}: N_s={Ns:.3e} 1/s, beta_white={beta:.3f} bits/s/mm^-2 (measured 0.225 +- 0.032)")
