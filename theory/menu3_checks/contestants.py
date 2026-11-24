"""Computed contestants for the tilted menu.

G, the odd-momentum witness, Gmin, and Gmax are each built from their own
model. The shared-bit mixture is a sensitivity, not a lock contestant.
No random seed: every start is a fixed vector.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize

S2 = math.sqrt(2.0)
S3 = math.sqrt(3.0)
MENU = np.array(
    [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [1.0 / S2, 0.0, 1.0 / S2],
        [-1.0 / S2, 0.0, 1.0 / S2],
        [1.0 / S3, 1.0 / S3, 1.0 / S3],
    ],
    dtype=np.float64,
)
T = -(MENU @ MENU.T)
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Z = np.diag([1.0, -1.0])
Y = np.array([[0.0, -1j], [1j, 0.0]])


def pauli(u: np.ndarray) -> np.ndarray:
    return u[0] * X.astype(complex) + u[1] * Y + u[2] * Z.astype(complex)


def singlet() -> np.ndarray:
    s = np.zeros(4, dtype=np.complex128)
    s[1] = 1.0 / S2
    s[2] = -1.0 / S2
    return s


def mean_loss(C: np.ndarray) -> float:
    d = C - T
    return float(np.sum(d * d) / 25.0)


def project_ball(v: np.ndarray) -> np.ndarray:
    nrm = float(np.linalg.norm(v))
    if nrm <= 1.0:
        return v
    return v / nrm


def g_model(eta: float = 0.0) -> tuple[float, float, np.ndarray]:
    """Holistic state (singlet density, eta). Product Paulis ignore eta.

    The joint effect (1+eta)/2 is computed and is not part of the loss.
    """
    psi = singlet()
    rho = np.outer(psi, psi.conj())
    C = np.zeros((5, 5))
    for a in range(5):
        for b in range(5):
            op = np.kron(pauli(MENU[a]), pauli(MENU[b]))
            C[a, b] = float(np.real(np.trace(rho @ op)))
    joint = 0.5 * (1.0 + float(eta))
    return mean_loss(C), joint, C


def odd_momentum_witness() -> float:
    """Two-point momentum. f(p) = p. The mirror sends p to -p.

    The recorded value is the mean of f(p) f(-p). It does not enter J.
    """
    acc = 0.0
    points = (1.0, -1.0)
    for p in points:
        f_here = p
        f_mirror = -p
        acc += f_here * f_mirror
    return acc / float(len(points))


def _rank1_loss(n: np.ndarray, m: np.ndarray) -> float:
    return mean_loss(np.outer(MENU @ project_ball(n), MENU @ project_ball(m)))


def _gmin_starts() -> list[np.ndarray]:
    starts = []
    for i in range(3):
        for s in (1.0, -1.0):
            for j in range(3):
                for t in (1.0, -1.0):
                    x = np.zeros(6)
                    x[i] = s
                    x[3 + j] = t
                    starts.append(x)
    frame = MENU.T @ MENU
    _, axes = np.linalg.eigh(frame)
    axis = axes[:, -1]
    x = np.zeros(6)
    x[:3] = axis
    x[3:] = -axis
    starts.append(x)
    x = np.zeros(6)
    x[:3] = axis
    x[3:] = axis
    starts.append(x)
    return starts


def gmin_loss() -> float:
    """Minimal tensor product: a product of two Bloch balls.

    Local unitaries and the swap keep a product a product, so the correlator
    is (n·u)(m·v) with both Bloch vectors inside the unit ball.
    """

    def objective(x: np.ndarray) -> float:
        return _rank1_loss(x[:3], x[3:])

    best = math.inf
    for x0 in _gmin_starts():
        res = minimize(objective, x0, method="Powell", options={"maxiter": 80, "ftol": 1e-16})
        if float(res.fun) < best:
            best = float(res.fun)
    return best


def _sphere(theta: float, phi: float) -> np.ndarray:
    return np.array(
        [math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)],
        dtype=np.float64,
    )


def gmax_loss() -> float:
    """Maximal tensor product, local rotations only.

    The granted group is SO(3) x SO(3) and the swap, applied to a product.
    A rotation of the pole (0, 0, 1), then a radius in {1, 1/2} for local
    mixedness, is the reachable correlator. The swap exchanges the two wings.
    """
    best = math.inf
    polar = [math.pi * i / 7 for i in range(8)]
    azimuth = [2.0 * math.pi * i / 8 for i in range(8)]
    for theta in polar:
        for phi in azimuth:
            n = _sphere(theta, phi)
            for th2 in polar:
                for ph2 in azimuth:
                    m = _sphere(th2, ph2)
                    for radius_n in (1.0, 0.5):
                        for radius_m in (1.0, 0.5):
                            val = _rank1_loss(radius_n * n, radius_m * m)
                            if val < best:
                                best = val
                            swapped = _rank1_loss(radius_m * m, radius_n * n)
                            if swapped < best:
                                best = swapped

    def objective(x: np.ndarray) -> float:
        return _rank1_loss(x[:3], x[3:])

    frame = MENU.T @ MENU
    _, axes = np.linalg.eigh(frame)
    axis = axes[:, -1]
    x0 = np.concatenate([-axis, axis])
    res = minimize(objective, x0, method="Nelder-Mead", options={"maxiter": 400, "xatol": 1e-14, "fatol": 1e-16})
    if float(res.fun) < best:
        best = float(res.fun)
    return best


def shared_bit_loss() -> float:
    """Real singlet, one shared bit. Not a lock contestant.

    Weight sqrt(2/3) on sharp xz projections. The rest reads y as +I on one
    wing and -I on the other.
    """
    psi = singlet()
    rho = np.outer(psi, psi.conj())
    p = math.sqrt(2.0 / 3.0)

    def proj_angle(u: np.ndarray) -> float:
        return math.atan2(float(u[2]), float(u[0]))

    def planar(u: np.ndarray) -> np.ndarray:
        ang = proj_angle(u)
        return math.cos(ang) * X + math.sin(ang) * Z

    def corr(ops_a, ops_b) -> np.ndarray:
        C = np.zeros((5, 5))
        for a in range(5):
            for b in range(5):
                C[a, b] = float(np.real(np.trace(rho @ np.kron(ops_a[a], ops_b[b]))))
        return C

    ops = [planar(MENU[i]) for i in range(5)]
    C1 = corr(ops, ops)
    ops_a = list(ops)
    ops_b = list(ops)
    ops_a[4] = np.eye(2)
    ops_b[4] = -np.eye(2)
    C2 = corr(ops_a, ops_b)
    return mean_loss(p * C1 + (1.0 - p) * C2)


def pair(jc: float, fc: bool, jx: float, fx: bool) -> str:
    if fc and not fx:
        return "WIN"
    if fx and not fc:
        return "LOSE"
    if not fc and not fx:
        return "EXCLUDED"
    delta = jx - jc
    band = 0.01 * max(jc, jx) + 1e-12
    if delta > band:
        return "WIN"
    if delta < -band:
        return "LOSE"
    return "TIE"


def cell(labels: list[str]) -> str:
    used = [z for z in labels if z != "EXCLUDED"]
    if any(z == "LOSE" for z in used):
        return "LOSE"
    if used and all(z == "WIN" for z in used):
        return "WIN"
    return "TIE"
