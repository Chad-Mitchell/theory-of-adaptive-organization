"""T67 library: bipartite Gaussian (Ornstein-Uhlenbeck) lattices with Kac-normalised r^-p couplings.
Fixed by PREREG_T67.md (sha256 in PREREG_T67.sha256). kT units."""
import numpy as np
import scipy.linalg as sl

ALPHA = 0.5


def geometry(d, n):
    """Minimum-image Euclidean distance from the origin for every site (flattened, row-major)."""
    z = np.arange(n)
    r1 = np.minimum(z, n - z).astype(float)
    if d == 1:
        return r1
    return np.sqrt(r1[:, None] ** 2 + r1[None, :] ** 2).ravel()


def coupling_vector(d, n, p):
    r = geometry(d, n)
    J = np.zeros_like(r)
    m = r > 0
    J[m] = r[m] ** (-p)
    J /= J.sum()  # Kac normalisation Z(n,p): row sum 1
    return J


def spectrum(d, n, p):
    J = coupling_vector(d, n, p)
    if d == 1:
        Jh = np.fft.fft(J)
    else:
        Jh = np.fft.fft2(J.reshape(n, n)).ravel()
    return (ALPHA + 1.0) - Jh.real


def dense_K(d, n, p):
    J = coupling_vector(d, n, p)
    if d == 1:
        idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
        Jm = J[idx]
    else:
        i = np.repeat(np.arange(n), n)
        j = np.tile(np.arange(n), n)
        di = (i[None, :] - i[:, None]) % n
        dj = (j[None, :] - j[:, None]) % n
        Jm = J.reshape(n, n)[di, dj]
    return (ALPHA + 1.0) * np.eye(n ** d) - Jm


def lyap_fourier(d, n, lam, Tvec):
    """Solve K S + S K = 2 diag(T) for circulant symmetric K with eigenvalues lam (FFT order)."""
    N = n ** d
    if d == 1:
        vh = np.fft.fft(Tvec)
        k = np.arange(N)
        G = vh[(k[:, None] - k[None, :]) % N] / N
        G *= 2.0 / (lam[:, None] + lam[None, :])
        S = np.fft.fft(np.fft.ifft(G, axis=0), axis=1)
    else:
        vh = np.fft.fft2(Tvec.reshape(n, n))
        k1 = np.repeat(np.arange(n), n)
        k2 = np.tile(np.arange(n), n)
        G = vh[(k1[:, None] - k1[None, :]) % n, (k2[:, None] - k2[None, :]) % n] / N
        G *= 2.0 / (lam[:, None] + lam[None, :])
        G = G.reshape(n, n, n, n)
        G = np.fft.ifft2(G, axes=(0, 1))
        G = np.fft.fft2(G, axes=(2, 3))
        S = G.reshape(N, N)
    S = S.real.copy()
    return 0.5 * (S + S.T)


def region(d, n, L):
    if d == 1:
        return np.arange(L)
    return np.array([i * n + j for i in range(L) for j in range(L)])


def boundary(d, L):
    return 2.0 if d == 1 else 4.0 * L


def temps(N, A, drive):
    if drive == "EQ":
        return np.ones(N)
    if drive == "HOT":
        T = np.ones(N); T[A] = 2.0; return T
    if drive == "COLD":
        T = np.full(N, 2.0); T[A] = 1.0; return T
    raise ValueError(drive)


def residual(K, S, Tvec, ncols=8):
    N = len(K)
    cols = np.linspace(0, N - 1, ncols).astype(int)
    R = K @ S[:, cols] + S @ K[:, cols]
    R[cols, np.arange(ncols)] -= 2 * Tvec[cols]
    return float(np.abs(R).max())


def quantities(K, S, Tvec, A, chol=None):
    """I(A;B), Idot_A = t1 + t2 (reviewed boundary-layer identity)."""
    N = len(K)
    mask = np.ones(N, bool); mask[A] = False
    B = np.where(mask)[0]
    if chol is None:
        chol = sl.cho_factor(S, lower=True)
    E = np.zeros((N, len(A))); E[A, np.arange(len(A))] = 1.0
    PA = sl.cho_solve(chol, E)
    PAA = PA[A]
    SAA = S[np.ix_(A, A)]
    ldS = np.linalg.slogdet(SAA)
    ldP = np.linalg.slogdet(PAA)
    assert ldS[0] > 0 and ldP[0] > 0
    I = 0.5 * (ldS[1] + ldP[1])
    SAAinv = np.linalg.inv(SAA)
    M = PAA - SAAinv
    t1 = -np.trace(SAAinv @ (K[np.ix_(A, B)] @ S[np.ix_(B, A)]))
    t2 = -float(np.sum(Tvec[A] * np.diag(M)))
    return float(I), float(t1 + t2), float(t1), float(t2)


def mi_direct(S, A):
    N = len(S)
    mask = np.ones(N, bool); mask[A] = False
    B = np.where(mask)[0]
    ld = lambda X: np.linalg.slogdet(X)[1]
    return 0.5 * (ld(S[np.ix_(A, A)]) + ld(S[np.ix_(B, B)]) - ld(S))


def idot_fd(K, S, Tvec, A, h=1e-5):
    N = len(K)
    Pi = np.zeros(N); Pi[A] = 1.0
    PK = Pi[:, None] * K
    dS = -(PK @ S + S @ PK.T) + 2 * np.diag(Pi * Tvec * Pi)
    return (mi_direct(S + h * dS, A) - mi_direct(S - h * dS, A)) / (2 * h)


def approach_exponent(y):
    """s = log2[(y3-y2)/(y2-y1)] on a doubling ladder; None if non-monotone."""
    r = (y[2] - y[1]) / (y[1] - y[0])
    if not np.isfinite(r) or r <= 0:
        return None
    return float(np.log2(r))


def p_crossing(ps, ss):
    """Largest zero crossing of s(p) (s>=0 then s<0), linear interpolation; undefined points bridged."""
    pts = [(p, s) for p, s in zip(ps, ss) if s is not None]
    if not pts:
        return {"p_c": None, "status": "undefined", "all": []}
    if all(s < 0 for _, s in pts):
        return {"p_c": pts[0][0], "status": "censored_below", "all": []}
    if pts[-1][1] >= 0:
        return {"p_c": pts[-1][0], "status": "censored_above", "all": []}
    cr = []
    for (p0, s0), (p1, s1) in zip(pts[:-1], pts[1:]):
        if s0 >= 0 > s1:
            cr.append(p0 + (p1 - p0) * s0 / (s0 - s1))
    return {"p_c": float(cr[-1]), "status": "ok", "all": [float(c) for c in cr]}
