"""Menu without an all-orthogonal axis. Locked by theory/composite-contest-2026-11-24/PREREG_3.md."""
from __future__ import annotations

import hashlib
import itertools
import math
from pathlib import Path

import numpy as np
from scipy.optimize import LinearConstraint, Bounds, linprog, milp, minimize

from contestants import (
    cell,
    g_model,
    gmax_loss,
    gmin_loss,
    odd_momentum_witness,
    pair,
    shared_bit_loss,
)

HERE = Path(__file__).resolve().parent
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
LAMBDAS = (0.0, 1e-4, 1e-3, 1e-2, 1e-1)


def fmt(x: float) -> str:
    return format(float(x), ".16e")


def pauli(u: np.ndarray) -> np.ndarray:
    return u[0] * X.astype(complex) + u[1] * Y + u[2] * Z.astype(complex)


def singlet() -> np.ndarray:
    s = np.zeros(4, dtype=np.complex128)
    s[1] = 1.0 / S2
    s[2] = -1.0 / S2
    return s


def op_from(kind: int, ang: float, bias: float) -> np.ndarray:
    if kind == 0:
        return np.eye(2)
    if kind == 1:
        return -np.eye(2)
    c = math.tanh(bias)
    rad = max(0.0, 1.0 - abs(c))
    return c * np.eye(2) + rad * (math.cos(ang) * X + math.sin(ang) * Z)


def corr(rho: np.ndarray, ops_a, ops_b) -> np.ndarray:
    C = np.zeros((5, 5))
    for a in range(5):
        for b in range(5):
            C[a, b] = float(np.real(np.trace(rho @ np.kron(ops_a[a], ops_b[b]))))
    return C


def mean_loss(C: np.ndarray) -> float:
    d = C - T
    return float(np.sum(d * d) / 25.0)


def chol_rho(x: np.ndarray) -> np.ndarray:
    L = np.zeros((4, 4))
    k = 0
    for i in range(4):
        for j in range(i + 1):
            L[i, j] = x[k]
            k += 1
    S = L @ L.T
    tau = float(np.trace(S))
    if tau < 1e-18:
        return np.eye(4) / 4.0
    return S / tau


def proj_angle(u: np.ndarray) -> float:
    return math.atan2(float(u[2]), float(u[0]))


def pattern_loss_singlet(pattern: tuple[int, ...], psi_rho: np.ndarray) -> float:
    angs = [proj_angle(MENU[i]) for i in range(5)]
    ops = [op_from(pattern[i], angs[i], 0.0) for i in range(5)]
    return mean_loss(corr(psi_rho, ops, ops))


def powell(pattern: tuple[int, ...]) -> float:
    # x: 10 chol, then for each planar slot on A and on B: bias, angle
    planar = [i for i, k in enumerate(pattern) if k == 2]
    nfree = 10 + 4 * len(planar)  # A bias, A ang, B bias, B ang per planar slot

    def unpack(x):
        rho = chol_rho(x[:10])
        ops_a, ops_b = [], []
        p = 10
        for i, k in enumerate(pattern):
            if k == 2:
                ops_a.append(op_from(2, x[p + 1], x[p]))
                ops_b.append(op_from(2, x[p + 3], x[p + 2]))
                p += 4
            else:
                ops_a.append(op_from(k, 0.0, 0.0))
                ops_b.append(op_from(k, 0.0, 0.0))
        return rho, ops_a, ops_b

    x0 = np.zeros(nfree)
    s = 1.0 / S2
    x0[0], x0[1], x0[3], x0[6] = 0.0, s, -s, 0.0
    p = 10
    for i, k in enumerate(pattern):
        if k == 2:
            ang = proj_angle(MENU[i])
            x0[p + 1] = ang
            x0[p + 3] = ang
            p += 4

    def fun(x):
        rho, oa, ob = unpack(x)
        return mean_loss(corr(rho, oa, ob))

    r = minimize(fun, x0, method="Powell", options={"maxiter": 40, "ftol": 1e-10})
    return float(r.fun)


def vertices() -> np.ndarray:
    signs = np.ones((32, 5))
    for k in range(32):
        for i in range(5):
            if (k >> i) & 1:
                signs[k, i] = -1.0
    C = np.empty((1024, 25))
    p = 0
    for a in range(32):
        for b in range(32):
            C[p] = np.outer(signs[a], signs[b]).ravel()
            p += 1
    return C


def classical_minimax(Cv: np.ndarray) -> tuple[float, int, int]:
    n = Cv.shape[0]
    t = T.ravel()
    cost = np.zeros(n + 1)
    cost[-1] = 1.0
    CT = Cv.T
    ones = np.ones((25, 1))
    A_ub = np.vstack([np.hstack([CT, -ones]), np.hstack([-CT, -ones])])
    b_ub = np.concatenate([t, -t])
    A_eq = np.zeros((1, n + 1))
    A_eq[0, :n] = 1.0
    res = linprog(
        cost, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=np.array([1.0]),
        bounds=[(0.0, None)] * n + [(0.0, None)], method="highs",
    )
    if not res.success:
        raise RuntimeError(res.message)
    s = float(res.x[-1])
    c_z = np.concatenate([np.zeros(n), np.ones(n)])
    A1 = np.hstack([CT, np.zeros((25, n))])
    A2 = np.hstack([-CT, np.zeros((25, n))])
    Ap = np.hstack([np.eye(n), -np.eye(n)])
    A_card = np.vstack([A1, A2, Ap])
    b_card = np.concatenate([t + s, -t + s, np.zeros(n)])
    A_sum = np.zeros((1, 2 * n))
    A_sum[0, :n] = 1.0
    card = milp(
        c_z,
        integrality=np.concatenate([np.zeros(n), np.ones(n)]),
        bounds=Bounds(np.zeros(2 * n), np.ones(2 * n)),
        constraints=[
            LinearConstraint(A_card, -np.inf, b_card),
            LinearConstraint(A_sum, np.array([1.0]), np.array([1.0])),
        ],
        options={"time_limit": 60.0},
    )
    if not card.success:
        raise RuntimeError(card.message)
    p = np.clip(card.x[:n], 0.0, None)
    alphas, betas = set(), set()
    for k in np.flatnonzero(p > 1e-8):
        alphas.add(int(k) // 32)
        betas.add(int(k) % 32)
    k_prod = len(alphas) * len(betas)
    return s * s, int(np.sum(card.x[n:] > 0.5)), k_prod


def r4c_loss(psi: np.ndarray) -> float:
    # real encoding of complex Born for product Pauli measurements
    def plus(u):
        x, y, z = u
        if z > -1 + 1e-14:
            den = math.sqrt(2 * (1 + z))
            return np.array([math.sqrt((1 + z) / 2), (x + 1j * y) / den])
        return np.array([0.0, 1.0])

    C = np.zeros((5, 5))
    for a in range(5):
        for b in range(5):
            acc = 0.0
            for sa in (1, -1):
                for sb in (1, -1):
                    ua = plus(sa * MENU[a])
                    ub = plus(sb * MENU[b])
                    phi = np.kron(ua, ub)
                    acc += sa * sb * abs(np.vdot(phi, psi)) ** 2
            C[a, b] = acc
    return mean_loss(C)


def main() -> int:
    psi = singlet()
    rho_s = np.outer(psi, psi.conj())
    Cq = np.zeros((5, 5))
    for a in range(5):
        for b in range(5):
            Cq[a, b] = float(np.real(np.vdot(psi, np.kron(pauli(MENU[a]), pauli(MENU[b])) @ psi)))
    L_c = mean_loss(Cq)
    block = T[np.ix_([1, 0, 4], [1, 0, 4])]
    sig = np.linalg.svd(block, compute_uv=False)
    sig2 = float(sig[-1] ** 2)
    lines = [
        f"sigma_min_sq {fmt(sig2)} svd_value unfinished_formula_not_used",
        f"C_loss {fmt(L_c)}",
    ]
    best_exact = math.inf
    best_opt = math.inf
    for digits in itertools.product((0, 1, 2), repeat=5):
        ex = pattern_loss_singlet(digits, np.real(rho_s))
        if ex < best_exact:
            best_exact = ex
        opt = powell(digits)
        if opt < best_opt:
            best_opt = opt
    Lr = min(best_exact, best_opt)
    lines.append(f"rebit_exact {fmt(best_exact)} rebit_opt {fmt(best_opt)} rebit_min {fmt(Lr)}")
    Cv = vertices()
    Lh, k_atoms, k_prod = classical_minimax(Cv)
    lines.append(f"classical_Linf {fmt(Lh)} K_atoms {k_atoms} K_prod {k_prod}")
    Lg, joint0, _ = g_model(0.0)
    _, joint1, _ = g_model(1.0)
    _, joint_m, _ = g_model(-1.0)
    Lw = odd_momentum_witness()
    Lgmin = gmin_loss()
    Lgmax = gmax_loss()
    Lr4 = r4c_loss(psi)
    lines.append(
        f"G_loss {fmt(Lg)} joint_eta0 {fmt(joint0)} joint_eta1 {fmt(joint1)} "
        f"joint_eta_m1 {fmt(joint_m)} G_minus_C {fmt(Lg - L_c)}"
    )
    lines.append(f"witness {fmt(Lw)} phase_space_two_point")
    lines.append(f"gmin {fmt(Lgmin)} gmax {fmt(Lgmax)} r4c {fmt(Lr4)}")
    # Lemma I0: the record is fixed before the settings, so this mutual
    # information is 0. The number is that lemma, not a computed mutual information.
    lines.append(f"I_A6 {fmt(0.0)} holevo_one_state {fmt(0.0)} Lemma_I0_value_not_computed")
    p_loss = Lr >= 1e-4
    floor = (3 - 2 * math.sqrt(2)) / 4
    p_bell = Lh + 1e-8 >= floor
    lines.append(f"P-loss {'PASS' if p_loss else 'FAIL'}")
    lines.append(f"P-bell {'PASS' if p_bell else 'FAIL'}")
    # cells at eps=0
    labels_pos = []
    p_tie_i = True
    for lam in LAMBDAS:
        jc = 0.0 if lam == 0 else lam * math.log(16)
        feas = {
            "C": L_c <= 1e-8,
            "R": Lr <= 1e-8,
            "H": Lh <= 1e-8,
            "G": Lg <= 1e-8,
            "R4a": Lh <= 1e-8,
            "R4c": Lr4 <= 1e-8,
            "Gmin": Lgmin <= 1e-8,
            "Gmax": Lgmax <= 1e-8,
        }
        K = {"C": 16, "R": 10, "H": k_prod, "G": 17, "R4a": k_prod, "R4c": 36, "Gmin": 16, "Gmax": 16}
        Lmap = {"C": L_c, "R": Lr, "H": Lh, "G": Lg, "R4a": Lh, "R4c": Lr4, "Gmin": Lgmin, "Gmax": Lgmax}
        labs = []
        lines.append(f"cell lam {fmt(lam)} eps 0 K-price")
        cell_at = len(lines) - 1
        for name in K:
            if not feas[name]:
                J = math.inf
            else:
                J = lam * math.log(K[name]) + Lmap[name]
            if name == "C":
                lab = "SELF"
            else:
                lab = pair(jc, feas["C"], J, feas[name])
                labs.append(lab)
            lines.append(f"  {name} feas {int(feas[name])} K {K[name]} L {fmt(Lmap[name])} J {fmt(J)} {lab}")
        lab_cell = cell(labs)
        lines[cell_at] = lines[cell_at] + " " + lab_cell
        # mutual-information price: price term 0, so ties among feasible loss-0
        labs_i = []
        for name in K:
            if name == "C":
                continue
            Ji = 0.0 if feas[name] else math.inf
            Jic = 0.0 if feas["C"] else math.inf
            labs_i.append(pair(Jic, feas["C"], Ji, feas[name]))
        i_lab = cell(labs_i)
        lines.append("  I-price " + i_lab + " Lemma_I0_value_not_computed")
        if i_lab != "TIE":
            p_tie_i = False
        if lam > 0:
            labels_pos.append(lab_cell)
    p_win = p_loss and all(z == "WIN" for z in labels_pos)
    lines.append(f"P-win {'PASS' if p_win else 'FAIL'}")
    lines.append(f"P-tie {'PASS' if p_tie_i else 'FAIL'} G {fmt(Lg)} R4c {fmt(Lr4)}")
    Lbit = shared_bit_loss()
    lines.append(f"shared_bit_loss {fmt(Lbit)}")
    lines.append(
        "shared_bit_count_used 40 reason both wings hold the bit, m_A times m_B = 4, times rebit 10"
    )
    sens = {"charged_K40": 40, "charged_K20": 20, "uncharged_K10": 10}
    sens_pos = {name: [] for name in sens}
    for lam in LAMBDAS:
        jc = 0.0 if lam == 0 else lam * math.log(16)
        fc = L_c <= 1e-8
        fb = Lbit <= 1e-8
        for name, Kb in sens.items():
            Jb = math.inf if not fb else lam * math.log(Kb) + Lbit
            lab = pair(jc, fc, Jb, fb)
            lines.append(
                f"sensitivity {name} lam {fmt(lam)} K {Kb} L {fmt(Lbit)} J {fmt(Jb)} {lab}"
            )
            if lam > 0:
                sens_pos[name].append(lab)
    for name, labs in sens_pos.items():
        lines.append(f"sensitivity_positive {name} {cell(labs)}")
    lines.append(
        "headline conditional_on Hardy_ln_K_AB "
        + ("WIN" if p_win else "FAIL")
        + " positive_lambda_under_the_lock"
    )
    text = "\n".join(lines) + "\n"
    (HERE / "decisions.out").write_text(text, encoding="utf-8", newline="\n")
    digest = hashlib.sha256((HERE / "decisions.out").read_bytes()).hexdigest()
    (HERE / "SHA256SUMS").write_text(digest + "  decisions.out\n", encoding="utf-8", newline="\n")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
