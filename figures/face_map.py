"""The map of adaptive design: what ONE component of the world calls for (theory core; no drawing here).

A system is n units (n = 1 allowed) facing a world that is a sum of independent components (time scales). For one component c:
  a LAYER IN EACH UNIT (local): every unit tracks c from its own reads, on time; upkeep n*h_l; gain per unit G_L.
  ONE SHARED LAYER (shared):    one tracker pools all n units' reads, which reach it a delay l late; upkeep h_c; gain per unit G_S.
  BOTH:                         local layers plus a shared one; gain per unit G_B (G_B >= max(G_L, G_S)).
  NONE.
Stakes w_u per unit on squared error.  Two numbers place the component on the map (each is "stakes it can win / its upkeep"):
  X_L = w_u*G_L / h_l          (is a layer in each unit worth its upkeep?)
  X_S = n*w_u*G_S / h_c        (is one shared layer worth its upkeep?)
Map theorem (exact, any world, any loss, any noise, delay, n, rho; proof in face_placements.md / THEORY B.11):
  value over NONE, in units of n*h_l:  local = X_L - 1;  shared = (X_S - 1)/nu;  both = X_L - 1 + (k_S*X_S - 1)/nu,
  with nu = n*h_l/h_c (how many local layers' upkeep one shared layer costs) and k_S = (G_B - G_L)/G_S, k_L = (G_B - G_S)/G_L
  (the share of each layer's gain the other does not already supply; 0 = redundant, 1 = independent).  Hence:
    NONE   iff X_L <= 1 and X_S <= 1                                  (no other number enters)
    LOCAL  if  X_L > 1 and X_S <= 1                                   (no other number enters)
    SHARED if  X_S > 1 and X_L <= 1                                   (no other number enters)
    X_L > 1 and X_S > 1: local vs shared by nu*(X_L - 1) vs X_S - 1; both iff k_L*X_L > 1 and k_S*X_S > 1.
For an Ornstein-Uhlenbeck component (rate a = 1/tau, variance v) read through white noise of density N per unit, with shared fraction rho
across units, the gains have closed forms (Kalman-Bucy; THEORY L1):
  G_L = v - P(v, a, N),  G_S = exp(-2 l/tau) * (v_m - P(v_m, a, N/n)),  v_m = v*(rho + (1 - rho)/n),
  P(v, a, N) = N*a*(sqrt(1 + 2v/(N a)) - 1).
So delay enters only through exp(-2 l/tau) and pooling through the factor pi = (v_m - P(v_m, a, N/n))/(v - P(v, a, N)):
  X_S = nu * pi * exp(-2 l/tau) * X_L.
G_B has no closed form; face_hybrid.py computes it (first-order stores, the theory's layer class).
"""
import numpy as np

def P_ou(v, a, N):
    """Steady-state Kalman error of one OU component (variance v, rate a) read through white noise of density N."""
    v = np.asarray(v, float); a = np.asarray(a, float); N = np.asarray(N, float)
    lam = 2 * v / (N * a)
    return N * a * lam / (np.sqrt(1 + lam) + 1)          # = N a (sqrt(1+lam) - 1), written stably

def gains_ou(v, a, N, n, rho, lead):
    """(G_L, G_S, pi) per unit for one OU component; lead = delay of the pooled reads (same time unit as 1/a)."""
    GL = v - P_ou(v, a, N)
    vm = v * (rho + (1 - rho) / n)
    GS0 = vm - P_ou(vm, a, N / n)
    return GL, np.exp(-2 * a * lead) * GS0, GS0 / GL

VALUE_NAMES = ('none', 'local', 'shared', 'both')

def values(XL, XS, nu, kL=None, kS=None):
    """Value of each design over NONE, in units of n*h_l (array of shape (4, ...)); both = -inf if kL/kS not given."""
    XL = np.asarray(XL, float); XS = np.asarray(XS, float); nu = np.asarray(nu, float)
    z = np.zeros(np.broadcast(XL, XS, nu).shape)
    loc = XL - 1 + z; sh = (XS - 1) / nu + z
    if kS is None: both = np.full_like(z, -np.inf)
    else: both = XL - 1 + (np.asarray(kS) * XS - 1) / nu + z
    return np.stack([z, loc, sh, both])

def decide(XL, XS, nu, kL=None, kS=None):
    """Index into VALUE_NAMES of the best design (ties to the simpler design)."""
    V = values(XL, XS, nu, kL, kS)
    return np.argmax(V + np.array([3, 2, 1, 0]).reshape((4,) + (1,) * (V.ndim - 1)) * 1e-12, axis=0)

def quadrant(XL, XS):
    """The part of the decision that no other number can change: 0 none, 1 local, 2 shared, 3 'both pay' (nu and k decide)."""
    XL = np.asarray(XL); XS = np.asarray(XS)
    return np.where(XL > 1, np.where(XS > 1, 3, 1), np.where(XS > 1, 2, 0))
