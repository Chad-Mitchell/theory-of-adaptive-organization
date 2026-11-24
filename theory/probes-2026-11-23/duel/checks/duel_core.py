"""GTAO tracking duel: core error models. Units: time in revolutions, omega = 2*pi.
Error e = wrap(theta - theta_hat). All trackers' error laws on a circle grid or via Fourier coefficients."""
import numpy as np
from scipy.special import ive

M = 2**15                      # circle grid cells
EDGES = -np.pi + 2*np.pi*np.arange(M+1)/M
CENT = 0.5*(EDGES[:-1]+EDGES[1:])
TAILMASK = np.abs(CENT) > np.pi/2   # cells are edge-aligned at +-pi/2 since M % 4 == 0
DGRID = np.fft.fftfreq(M, d=1.0/M)  # integer frequencies

def wrap(x):
    return (x + np.pi) % (2*np.pi) - np.pi

def noise_char(d, v_diff=0.0, kappa_obs=None):
    """Characteristic function E exp(-i d Z) of the common noise: wrapped normal variance v_diff
    (sigma^2 * elapsed revolutions) times von Mises observation noise kappa_obs."""
    d = np.asarray(d, float)
    g = np.exp(-0.5*v_diff*d**2)
    if kappa_obs is not None:
        g = g * ive(np.abs(d), kappa_obs)/ive(0, kappa_obs)
    return g

# ---------- (b) quantum / (c1) restricted rotor / (o) orbitope: phase density from c ----------
def beta(d):
    d = np.asarray(d, float)
    out = np.where(d == 0, 0.5, 0.0)
    nz = d != 0
    out[nz] = -np.sin(d[nz]*np.pi/2)/(np.pi*d[nz])
    return out

def tail_matrix(N, v_diff=0.0, kappa_obs=None):
    j = np.arange(N)
    D = j[None, :]-j[:, None]
    return beta(D)*noise_char(D, v_diff, kappa_obs)

def stake_matrix(N):
    A = np.zeros((N, N))
    i = np.arange(N-1)
    A[i, i+1] = A[i+1, i] = 0.5
    return A

def best_state(N, eps, v_diff=0.0, kappa_obs=None):
    """Maximize R = c^T A c over unit c s.t. c^T B c <= eps (B includes the worst-case common noise).
    Returns (R, tail, c) or (None, tailmin, None) if infeasible. Lagrange path mu >= 0 on top eigvec of A - mu B.
    Exact by convexity of the phase-density set (Fejer-Riesz) + one linear constraint."""
    A = stake_matrix(N); B = tail_matrix(N, v_diff, kappa_obs)
    def top(mu):
        w, V = np.linalg.eigh(A - mu*B); c = V[:, -1]; c = c*np.sign(c.sum() or 1)
        return c, c@A@c, c@B@c
    c, R, tl = top(0.0)
    if tl <= eps:
        return R, tl, c
    wB, VB = np.linalg.eigh(B)
    if wB[0] > eps:
        return None, wB[0], None
    lo, hi = 0.0, 1.0
    while top(hi)[2] > eps:
        hi *= 2
        if hi > 1e12:
            return None, wB[0], None
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if top(mid)[2] > eps: lo = mid
        else: hi = mid
    c, R, tl = top(hi)
    return R, tl, c

def phase_coeffs(c):
    """P_d = sum_k c_k c_{k+d}, d=0..N-1 (density p = (1/2pi) sum_d P_d e^{i d phi})."""
    N = len(c)
    return np.array([np.dot(c[:N-d], c[d:]) for d in range(N)])

def b_tail(c, v_diff=0.0, kappa_obs=None):
    P = phase_coeffs(c); d = np.arange(len(c))
    g = noise_char(d, v_diff, kappa_obs); bt = beta(d)
    return P[0]*bt[0]*g[0] + 2*np.sum(P[1:]*g[1:]*bt[1:])

# ---------- (a) classical N-state record: frozen (r=0), Markov unicyclic clock (rate r), free ticks ----------
def a_jump_dist(N, r, t):
    """q_m = P(K_t = m mod N), K_t ~ Poisson(r t)."""
    j = np.arange(N)
    phi = np.exp(r*t*(np.exp(-2j*np.pi*j/N)-1.0))
    q = np.real(np.fft.ifft(phi))  # q_m = (1/N) sum_j phi_j e^{+2 pi i j m/N} = P(K = m mod N)
    q = np.clip(q, 0, None); return q/q.sum()

def a_char1(N, r, t, shift=None):
    """E cos e for the N-state record at time t (no common noise). Error = u + 2pi t - 2pi K/N (+ tick sawtooth)."""
    s = np.sinc(1.0/N)  # np.sinc(x)=sin(pi x)/(pi x) -> sin(pi/N)/(pi/N)
    if shift is not None:  # free ticks: deterministic residual shift
        return s*np.cos(shift)
    z = np.exp(r*t*(np.exp(-2j*np.pi/N)-1.0))*np.exp(2j*np.pi*t)
    return s*np.real(z)

def uniform_mix_density(centers, weights, width):
    """Cell masses of a mixture of uniforms of given width (exact cell integration, wrapped)."""
    mass = np.zeros(M)
    for cpos, w in zip(centers, weights):
        if w < 1e-15: continue
        a = cpos - width/2; b = cpos + width/2
        # integrate uniform on [a,b] over cells, wrapping
        for sh in (-2*np.pi, 0.0, 2*np.pi):
            lo = np.clip(EDGES[:-1], a+sh, b+sh); hi = np.clip(EDGES[1:], a+sh, b+sh)
            mass += w*np.clip(hi-lo, 0, None)/width
    return mass

def convolve_noise(mass, v_diff=0.0, kappa_obs=None):
    if v_diff == 0.0 and kappa_obs is None:
        return mass
    F = np.fft.fft(mass)
    F *= noise_char(DGRID, v_diff, kappa_obs)
    out = np.real(np.fft.ifft(F)); return np.clip(out, 0, None)

def a_tail(N, r, t, v_diff=0.0, kappa_obs=None, shift=None):
    width = 2*np.pi/N
    if shift is not None:
        mass = uniform_mix_density([shift], [1.0], width)
    else:
        q = a_jump_dist(N, r, t)
        centers = wrap(2*np.pi*t - 2*np.pi*np.arange(N)/N)
        mass = uniform_mix_density(centers, q, width)
    mass = convolve_noise(mass, v_diff, kappa_obs)
    return mass[TAILMASK].sum()

def tick_shift(N, t):
    """Free external ticks every 1/N rev, aligned so the residual sawtooth is in [-pi/N, pi/N)."""
    x = (t*N + 0.5) % 1.0 - 0.5
    return 2*np.pi*x/N

# ---------- (c-RD) noiseless point read through a covariant channel (P-info) ----------
def gibbs_density(beta_, nu):
    w = np.exp(beta_*(np.cos(CENT) - 1.0) - nu*TAILMASK)
    return w/w.sum()

def info_of_density(mass):
    p = mass/(2*np.pi/M)  # density
    m = mass > 0
    h = -np.sum(mass[m]*np.log(p[m]))
    return np.log(2*np.pi) - h

# ---------- fast Fourier-series tail for the N-state record (used in the grid) ----------
DMAX = 2**16
DD = np.arange(1, DMAX+1, dtype=float)
BETA_D = beta(DD)

def a_tail_fourier(N, r, t, v_diff=0.0, kappa_obs=None, shift=None):
    if shift is not None:
        C = np.sinc(DD/N)*np.exp(-1j*DD*shift)
    else:
        C = np.sinc(DD/N)*np.exp(-2j*np.pi*DD*t)*np.exp(r*t*(np.exp(2j*np.pi*DD/N)-1.0))
    C = C*noise_char(DD, v_diff, kappa_obs)
    return 0.5 + 2*np.sum(np.real(C)*BETA_D)
