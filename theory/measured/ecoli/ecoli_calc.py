#!/usr/bin/env python3
"""ECOLI-MEM: locked calculation (written before it was ever run; see PREREG.md).

Theory's predicted memory time of E. coli's slow (methylation) layer, from the
measured world statistics and noise, under the locked arms, and the verdicts by
the locked rules. Stdlib + numpy only. Run: nice -n 19 python3 ecoli_calc.py
"""
import itertools, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- measured inputs: Mattingly, Kamino, Machta & Emonet 2021, Nat Phys 17:1426, Supp. Table S1
LAM = (0.862, 0.005)        # 1/s, decay rate of x-velocity autocorrelation (1/tau_v)
AV = (157.1, 0.5)           # um^2/s^2, prefactor of V(t)
G = (1.73, 0.03)            # kinase gain (a per unit ln c)
TAU1_FIT = (0.22, 0.01)     # s, fitted rise incl. switching/CheY-CheZ binding
TAU1_KIN = (0.017, 0.004)   # s, kinase response time (lit.)
TAU2 = (9.9, 0.3)           # s, adaptation time  <-- THE OUTCOME
SIGN = (0.092, 0.002)       # kinase-noise s.d. (a units)
TAUN = (11.75, 0.04)        # s, kinase-noise correlation time
G_LAB = [0.1, 0.2, 0.3, 0.4]  # 1/mm, gradients used for drift measurements (same paper)
C_BG = 100e-6               # M, MeAsp background of every measurement
# ---- assumed ranges (stated in PREREG section 3; not measured in the source)
D_LIG = [500.0, 1000.0]     # um^2/s, small-molecule diffusion coefficient in water
A_CELL = [0.5, 1.0]         # um, effective sensing radius of the cell
K_BP = [1 / (4 * math.pi), 1 / math.pi]  # prefactor: (dc/c)^2 * T = K_BP/(D a c)
NA = 6.02214076e23

def conc_um3(c_molar):
    return c_molar * NA * 1e-15  # molecules per um^3 (1 um^3 = 1e-15 L)

def arm_a_poles(lam, sig_u2, r):
    """Steady-state Kalman-Bucy filter for x' = u, u' = -lam u + sqrt(2 lam sig_u2) w,
    y = x + white noise of density r. Returns filter poles (eigenvalues of A - L C)."""
    # closed-loop characteristic: p^4 - lam^2 p^2 + Q/r = 0 (stable roots), Q = 2 lam sig_u2
    Q = 2 * lam * sig_u2
    roots = np.roots([1, 0, -lam ** 2, 0, Q / r])
    stable = sorted([z for z in roots if z.real < 0], key=lambda z: -z.real)
    return [-z for z in stable]  # as positive-real-part rates

def arm_a_poles_riccati(lam, sig_u2, r):
    """Independent check of arm_a_poles by solving the filter Riccati equation numerically."""
    A = np.array([[0, 1], [0, -lam]]); C = np.array([[1.0, 0]])
    Qm = np.array([[0, 0], [0, 2 * lam * sig_u2]])
    P = np.eye(2)
    dt = 1e-3 / max(lam, 1.0)
    for _ in range(400000):
        dP = A @ P + P @ A.T + Qm - P @ C.T @ C @ P / r
        P = P + dt * dP
        if np.max(np.abs(dP)) < 1e-13:
            break
    L = P @ C.T / r
    ev = np.linalg.eigvals(A - L @ C)
    return sorted([-e for e in ev], key=lambda z: z.real)

def k0(G_, t1, t2):
    return G_ * t2 * t2 / (t1 + t2)  # integral of G e^{-t/t2}(1-e^{-t/t1})

def arm_b_tau(lam, sig_u2, Ns):
    snr = 2 * sig_u2 / (lam * Ns)
    return 1.0 / (lam * math.sqrt(1 + snr)), snr

def arm_c_tau(lam, sig_u2, V0, t2):
    """Diagnostic arm C: store noise of fixed stationary variance in activity units, so the
    input-referred noise variance on the low-passed signal scales as V0 (t2/tau)^2.
    Best single-store memory with free output gain (instantaneous linear readout)."""
    taus = np.logspace(-3, 3, 6001)
    A = 1 / (1 + lam * taus)
    var_z = sig_u2 * A + V0 * (t2 / taus) ** 2
    score = (sig_u2 * A) ** 2 / var_z          # explained variance of u
    i = int(np.argmax(score))
    return float(taus[i]), float(1 - score[i] / sig_u2)

def main():
    out = {"inputs": {}, "arms": {}, "structure": {}, "premise": {}, "verdicts": {}}
    lam = LAM[0]; tau_v = 1 / lam
    c = conc_um3(C_BG)
    # ---------- Arm A: Berg-Purcell read noise at the physical floor
    A_taus = []; A_fast = []; A_detail = []
    for g_mm, D, a, kbp, av, lm in itertools.product(G_LAB, D_LIG, A_CELL, K_BP,
                                                    [AV[0] - 2 * AV[1], AV[0] + 2 * AV[1]],
                                                    [LAM[0] - 2 * LAM[1], LAM[0] + 2 * LAM[1]]):
        g = g_mm * 1e-3
        sig_u2 = g * g * av
        r = kbp / (D * a * c)
        poles = arm_a_poles(lm, sig_u2, r)
        re = sorted([p.real for p in poles])
        A_taus.append(1 / re[0]); A_fast.append(1 / re[-1])
        A_detail.append(dict(g=g_mm, D=D, a=a, kbp=kbp, r=r, sig_u2=sig_u2,
                             poles=[[p.real, p.imag] for p in poles]))
    # independent Riccati check at the box centre
    gc = 0.25e-3; rc = (1 / (2 * math.pi)) / (750 * 0.75 * c)
    p1 = arm_a_poles(lam, gc * gc * AV[0], rc); p2 = arm_a_poles_riccati(lam, gc * gc * AV[0], rc)
    out["arms"]["A"] = dict(tau_slow_range=[min(A_taus), max(A_taus)],
                            tau_fast_range=[min(A_fast), max(A_fast)],
                            check_quartic=[[z.real, z.imag] for z in p1],
                            check_riccati=[[z.real, z.imag] for z in p2],
                            n_corners=len(A_taus))
    # ---------- Arm B: measured kinase noise referred to the signal as white noise
    B_taus = []; B_snr = []
    for g_mm, Gv, t1, sn, tn, lm, av in itertools.product(
            G_LAB, [G[0] - 2 * G[1], G[0] + 2 * G[1]], [TAU1_FIT[0], TAU1_KIN[0]],
            [SIGN[0] - 2 * SIGN[1], SIGN[0] + 2 * SIGN[1]], [TAUN[0] - 2 * TAUN[1], TAUN[0] + 2 * TAUN[1]],
            [LAM[0] - 2 * LAM[1], LAM[0] + 2 * LAM[1]], [AV[0] - 2 * AV[1], AV[0] + 2 * AV[1]]):
        g = g_mm * 1e-3
        Ns = 2 * sn * sn * tn / k0(Gv, t1, TAU2[0]) ** 2
        t, snr = arm_b_tau(lm, g * g * av, Ns)
        B_taus.append(t); B_snr.append(snr)
    out["arms"]["B"] = dict(tau_range=[min(B_taus), max(B_taus)], snr_range=[min(B_snr), max(B_snr)])
    # ---------- Arm C (diagnostic only; no verdict)
    C_taus = []
    for g_mm in G_LAB:
        g = g_mm * 1e-3
        V0 = SIGN[0] ** 2 / k0(G[0], TAU1_FIT[0], TAU2[0]) ** 2
        t, e = arm_c_tau(lam, g * g * AV[0], V0, TAU2[0])
        C_taus.append(t)
    out["arms"]["C_diagnostic"] = dict(tau_by_g=dict(zip(map(str, G_LAB), C_taus)))
    # ---------- premise checks
    ratio = TAUN[0] / TAU2[0]
    out["premise"]["tau_n_over_tau_2"] = ratio
    out["premise"]["store_noise_dominates"] = abs(math.log(ratio)) <= math.log(1.5)
    # BP-referred share of measured kinase noise variance (activity units), box centre
    # white x-noise r through x->a transfer i w K_u(w): variance = r * int |w K(w)|^2 dw/2pi
    w = np.linspace(-2000, 2000, 400001); dw = w[1] - w[0]
    def Kw(t1, t2, Gv):
        return Gv * (1 / (1 / t2 + 1j * w) - 1 / (1 / t2 + 1 / t1 + 1j * w))
    shares = []
    for t1 in [TAU1_FIT[0], TAU1_KIN[0]]:
        for D, a, kbp in itertools.product(D_LIG, A_CELL, K_BP):
            r = kbp / (D * a * c)
            var_bp = r * np.sum(np.abs(w * Kw(t1, TAU2[0], G[0])) ** 2) * dw / (2 * math.pi)
            shares.append(var_bp / SIGN[0] ** 2)
    out["premise"]["bp_share_of_kinase_noise_range"] = [min(shares), max(shares)]
    # ---------- structure
    out["structure"] = dict(world_degree=2, measured_stores=2,
                            measured_poles=[1 / TAU2[0], 1 / TAU2[0] + 1 / TAU1_FIT[0], 1 / TAU2[0] + 1 / TAU1_KIN[0]],
                            lam=lam)
    # ---------- verdicts by the locked rules
    M = [TAU2[0] - 2 * TAU2[1], TAU2[0] + 2 * TAU2[1]]
    def verdict(L, U):
        lo2, hi2, lo3, hi3 = L / 2, 2 * U, L / 3, 3 * U
        inside = lo2 <= M[0] and M[1] <= hi2
        rival_inside = lo2 <= tau_v <= hi2
        if inside:
            return "PASS" if not rival_inside else "PASS-NONDISCRIMINATING"
        if M[1] < lo3 or M[0] > hi3:
            return "FAIL"
        return "INCONCLUSIVE"
    for k in ["A", "B"]:
        L, U = out["arms"][k]["tau_slow_range" if k == "A" else "tau_range"]
        out["verdicts"][k] = verdict(L, U)
    out["verdicts"]["A_label"] = ("INVALID as a test of the claim (premise: read noise binds) -- reported, not scored"
                                  if out["premise"]["store_noise_dominates"] or max(shares) < 0.1 else "valid")
    out["verdicts"]["B_label"] = "conditional on store noise independent of store speed (not checkable here)"
    out["verdicts"]["rival_R1_tau_equals_tau_v"] = dict(tau_v=tau_v, ratio_measured_over_rival=TAU2[0] / tau_v,
                                                         verdict="FAIL" if TAU2[0] / tau_v > 3 or TAU2[0] / tau_v < 1 / 3 else
                                                         ("PASS" if 0.5 <= TAU2[0] / tau_v <= 2 else "INCONCLUSIVE"))
    sfast_pred = out["arms"]["A"]["tau_fast_range"]
    out["verdicts"]["S1_layer_count"] = "PASS (structural; non-discriminating vs 'set at the world scales')"
    out["inputs"] = dict(c_per_um3=c, tau_v=tau_v)
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))

if __name__ == "__main__":
    main()
