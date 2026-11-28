"""Independent reviewer Monte Carlo for PR #74 (CAUSAL-KAPPA-LENIENCY). Own code; imports nothing from the repo.
Model: K independent contrasts x_k (log input changes); design moves y_k = r * s * b * x_k + e_k, e ~ N(0, sd^2).
Scaled prediction per unit S: P = s_hat * b * S. Estimate D = beta_hat * S (OLS through origin), sigma = se * S (t residual se).
Optional plug-in error on s (log-sd ls), propagated into decision variance as (kappa*P*ls)^2 (delta method).
Rules (z = 1.96, kappa = 1/2):
  R0 (locked): FAIL iff D + z sig_F < kappa P ; PASS iff D - z sig > 0 (and not FAIL; FAIL takes precedence) ; else INC
  R1 (PR #74): FAIL same ; PASS iff D - z sig_P > kappa P
  R2: kappa = 1 with s error propagated (FAIL iff D + z sig2 < P)
  L : R1 PASS AND level match (|level_hat - level_opt| < z * se_level), level read with fixed proxy offset
"""
import numpy as np, sys
from scipy.stats import norm
rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 74074)
K, s, b, z, kap, R = 30, 0.63, 1.0, 1.96, 0.5, 40000

def run(r, snr, ls=0.0, offset_se=0.0, kap=kap):
    x = rng.normal(0, 1, (R, K)); x /= np.sqrt((x**2).sum(1, keepdims=True))     # S = 1 per rep
    Ptrue = s * b                                                                  # S = 1
    sd = Ptrue / snr                                                               # sigma of D = sd / S = sd
    y = r * Ptrue * x + rng.normal(0, sd, (R, K))
    D = (x * y).sum(1)                                                             # sum x^2 = 1
    res = y - D[:, None] * x
    sig = np.sqrt((res**2).sum(1) / (K - 1))
    shat = s * np.exp(rng.normal(0, ls, R)) if ls > 0 else np.full(R, s)
    P = shat * b
    sigd = np.sqrt(sig**2 + (kap * P * ls)**2)
    fail = D + z * sigd < kap * P
    p0 = (D - z * sig > 0) & ~fail
    p1 = D - z * sigd > kap * P
    sig2 = np.sqrt(sig**2 + (P * ls)**2)
    f2 = D + z * sig2 < P
    lev = offset_se + rng.normal(0, 1, R)                                          # level error in SE units
    L = p1 & (np.abs(lev) < z)
    both0 = (D - z * sig > 0) & fail                                               # R0 PASS and FAIL regions overlap
    return dict(F=fail.mean(), P0=p0.mean(), P1=p1.mean(), F2=f2.mean(), L=L.mean(), overlap0=both0.mean())

print("r     snr  ls   | FAIL  R0pass R1pass | R2fail | Lpass | R0 PASS&FAIL both true | analytic R1pass, FAIL")
for ls in (0.0, 0.3):
    for r in (1.0, 0.63, 0.53, 0.5, 0.4, 0.25, 0.0):
        for snr in (5.6, 9.7, 20.0):
            o = run(r, snr, ls)
            a1 = norm.cdf((r - kap) * snr - z); af = norm.cdf((kap - r) * snr - z)
            print(f"{r:4.2f} {snr:5.1f} {ls:4.1f} | {o['F']:.3f} {o['P0']:.3f} {o['P1']:.3f} | {o['F2']:.3f} | {o['L']:.3f} | {o['overlap0']:.3f} | {a1:.3f} {af:.3f}")
print("level offset 3 SE, r=1, snr 9.7:", run(1.0, 9.7, 0, 3.0))
# Over-response (Q2): R1 PASS rate when r = 2.5 (> 1/kappa)
print("over-response r=2.5 snr 9.7:", run(2.5, 9.7))
# kappa = 1/4 gate check
for kp in (0.25, 0.5):
    snr_gate = (z + norm.ppf(0.8)) / kp
    o = run(1.0, snr_gate, kap=kp); o0 = run(0.0, snr_gate, kap=kp)
    print(f"kappa {kp}: gate SNR {snr_gate:.2f}: P(R1 PASS|r=1)={o['P1']:.3f} (analytic {norm.cdf((1-kp)*snr_gate-z):.3f}); P(FAIL|r=0)={o0['F']:.3f}")
# Average wrong-pass rate over r ~ U(0, kappa) (designs truly below the kill line), and false kills over r ~ U(kappa, 1)
for snr in (5.6, 9.7, 20.0):
    wp0 = np.mean([run(r, snr)['P0'] for r in np.linspace(0.025, 0.475, 10)])
    wp1 = np.mean([run(r, snr)['P1'] for r in np.linspace(0.025, 0.475, 10)])
    fk = np.mean([run(r, snr)['F'] for r in np.linspace(0.525, 1.0, 10)])
    print(f"snr {snr}: mean wrong-pass over r in (0, kappa): R0 {wp0:.3f}  R1 {wp1:.4f}; mean false kill over r in [kappa,1]: {fk:.4f} (same for both rules)")
