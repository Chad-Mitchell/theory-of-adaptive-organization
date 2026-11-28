"""Helpers for the BICAUSAL Route A follow-up (theory/bicausal-a-2026-11-27/PREREG.md).

Two linear additive-noise classes, each coordinate with its own bath.

W2 (theory/two-route-2026-11-25/PREREG.md section 2.1, unchanged): unit mobility, kT_i = D_i,
  dx = -a(x - g m) dt + sqrt(2D) dW_x,  dm = -gamma(m - c x) dt + sqrt(2 D_M) dW_m,
  heat into bath i: Qdot_i = E[f_i^2] + D_i E[d_i f_i]   (energy units).

LINK (this prereg, section 3): every bath at kT = 1, mobility of each memory coordinate free (noise D_i is a design),
  heat into bath i in units of kT: Qdot_i = E[f_i^2]/D_i + E[d_i f_i]   (theory/INFO_PHYSICS_ATTAINABILITY.md section 4).
  World X: f_X = -a X, D_X = a v (equilibrium OU, variance v). Level M0: f_0 = -b0 (M0 - X), noise D0.
  Member M1 linked to the level: f_1 = -b1 (M1 - M0), noise D1. Direct member: f_1 = -b1 (M1 - X), noise D1.
  (Gains c0 = c1 = 1 without loss of generality: rescaling a memory coordinate rescales its noise and leaves every
  heat and every decision error unchanged.)
  Decision error of a member: E[Var(X | M1)] = v - C_X1^2 / C_11 (Gaussian; the action is the conditional mean).
"""
import numpy as np
from scipy.linalg import solve_continuous_lyapunov


def lyap(F, Dvec):
    """Stationary covariance of dz = F z dt + sqrt(2 diag(D)) dW: F S + S F^T + 2 diag(D) = 0."""
    F = np.asarray(F, float)
    if np.max(np.linalg.eigvals(F).real) >= 0:
        raise ValueError("unstable drift")
    S = solve_continuous_lyapunov(F, -2.0 * np.diag(np.asarray(Dvec, float)))
    return 0.5 * (S + S.T)


# ---------------------------------------------------------------- W2
def w2_cov(a, g, gamma, c, D=1.0, DM=1.0):
    F = np.array([[-a, a * g], [gamma * c, -gamma]])
    return lyap(F, [D, DM])


def w2_heats(a, g, gamma, c, D=1.0, DM=1.0):
    S = w2_cov(a, g, gamma, c, D, DM)
    sxx, sxm, smm = S[0, 0], S[0, 1], S[1, 1]
    e_x = sxx - 2 * g * sxm + g * g * smm      # E[(x - g m)^2]
    e_m = smm - 2 * c * sxm + c * c * sxx      # E[(m - c x)^2]
    QX = a * a * e_x - D * a
    QM = gamma * gamma * e_m - DM * gamma
    return dict(QX=QX, QM=QM, sxx=sxx, sxm=sxm, smm=smm, e_x=e_x, e_m=e_m,
                track=sxx - 2 * sxm + smm)   # E[(x - m)^2]


# ---------------------------------------------------------------- LINK
def link_member(a, v, b0, D0, b1, D1, linked=True):
    """Return dict with level heat Q0, member heat Q1, world heat QX, member decision error eps1, level decision
    error eps0. linked=False gives a direct member (reads X), with no level (Q0 = 0, eps0 = nan)."""
    if linked:
        F = np.array([[-a, 0.0, 0.0], [b0, -b0, 0.0], [0.0, b1, -b1]])
        S = lyap(F, [a * v, D0, D1])
        # E[f0^2] = b0^2 E[(M0 - X)^2]
        e0 = S[1, 1] - 2 * S[0, 1] + S[0, 0]
        e1 = S[2, 2] - 2 * S[1, 2] + S[1, 1]
        Q0 = b0 * b0 * e0 / D0 - b0
        Q1 = b1 * b1 * e1 / D1 - b1
        QX = a * a * S[0, 0] / (a * v) - a
        eps1 = v - S[0, 2] ** 2 / S[2, 2]
        eps0 = v - S[0, 1] ** 2 / S[1, 1]
        return dict(Q0=Q0, Q1=Q1, QX=QX, eps1=eps1, eps0=eps0, S=S)
    F = np.array([[-a, 0.0], [b1, -b1]])
    S = lyap(F, [a * v, D1])
    e1 = S[1, 1] - 2 * S[0, 1] + S[0, 0]
    Q1 = b1 * b1 * e1 / D1 - b1
    QX = a * a * S[0, 0] / (a * v) - a
    eps1 = v - S[0, 1] ** 2 / S[1, 1]
    return dict(Q0=0.0, Q1=Q1, QX=QX, eps1=eps1, eps0=float("nan"), S=S)


def pooled_cost(K, w, a, v, b0, D0, b1, D1):
    """Per-member cost of one level shared by K linked members: Q0/K + Q1 + w eps1 (kT = 1)."""
    r = link_member(a, v, b0, D0, b1, D1, linked=True)
    return r["Q0"] / K + r["Q1"] + w * r["eps1"], r


def direct_infimum(w, a=1.0, v=1.0):
    """Infimum over bipartite memories of heat + w * decision error for one equilibrium OU signal (IP11 frontier,
    theory/INFO_PHYSICS_ATTAINABILITY.md section 0): w v if w <= a/v, else 2 sqrt(a v w) - a (kT = 1)."""
    return w * v if w <= a / v else 2.0 * np.sqrt(a * v * w) - a


def level_heat_closed_form(a, v, b0, D0):
    """Derived on paper (PREREG section 3.2): Q0 = b0^2 a v / ((a + b0) D0) for f0 = -b0 (M0 - X)."""
    return b0 * b0 * a * v / ((a + b0) * D0)
