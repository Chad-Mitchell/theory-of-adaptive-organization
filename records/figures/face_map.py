"""The map of adaptive design: what ONE component of the world calls for (theory core; no drawing here).

A system is n units (n = 1 allowed) facing a world that is a sum of independent components (time scales). For one component c:
  a LAYER IN EACH UNIT (local): every unit tracks c from its own reads, on time; upkeep n*h_l; gain per unit G_L.
  ONE SHARED LAYER (shared):    one tracker pools all n units' reads, which reach it a delay l late; upkeep h_c; gain per unit G_S.
  BOTH:                         local layers plus a shared one; gain per unit G_B (G_B >= max(G_L, G_S)).
  NONE.
Stakes w_u per unit on squared error.  Two numbers place the component on the map (each is "stakes it can win / its upkeep"):
  X_L = w_u*G_L / h_l          (is a layer in each unit worth its upkeep?)
  X_S = n*w_u*G_S / h_c        (is one shared layer worth its upkeep?)
Exact identities (any model, any loss: nothing but the definitions):
  value over NONE, in units of n*h_l:  local = X_L - 1;  shared = (X_S - 1)/nu;  both = X_L - 1 + (k_S*X_S - 1)/nu = (1 + 1/nu)(X_B - 1),
  with nu = n*h_l/h_c, k_S = (G_B - G_L)/G_S, k_L = (G_B - G_S)/G_L and X_B = n*w_u*G_B/(n*h_l + h_c) (the joint layers' stakes over
  their joint upkeep).  So the best design is the argmax of (0, X_L - 1, (X_S - 1)/nu, (1 + 1/nu)(X_B - 1)) -- always exact (decide()).
Map theorem (THEORY B.11, CT35; premises G_L, G_S > 0 and gains independent of stake and upkeep): for fixed gains, the quadrant edges
  X_L = 1 and X_S = 1 decide the design outside the upper-right quadrant for every stake and upkeep  IFF  the layers'
  value is SUBADDITIVE, G_B <= G_L + G_S (equivalently k_L, k_S <= 1, equivalently X_B <= 1 whenever X_L, X_S <= 1).  Then:
    NONE   iff X_L <= 1 and X_S <= 1;   LOCAL if X_L > 1 >= X_S;   SHARED if X_S > 1 >= X_L;
    X_L > 1 and X_S > 1: local vs shared by nu*(X_L - 1) vs X_S - 1; both iff k_L*X_L > 1 and k_S*X_S > 1.
  Where subadditivity fails (joint-only value: a shared store paying as a COMMON-MODE REFERENCE for local ones -- the suppressor-variable
  effect of regression, Horst 1941, Conger 1974; adaptive noise cancelling, Widrow et al. 1975; complementary signals, Borgers et al. 2013)
  BOTH can win in any quadrant, including NONE's.  Which classes are subadditive: face_subadd.py (sampled; review 26 counterexamples in
  tools/test_face_map.py).  Separate-channel OU class, independent unit noise, unpriced reading: subadditive in every world sampled
  (not proved).  Priced reading, read noise common to units, or common and idiosyncratic parts at different rates on one stream: not.
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

def XB(XL, XS, nu, kS):
    """Joint stakes over joint upkeep: X_B = n w_u G_B / (n h_l + h_c) = (nu*X_L + kS*X_S) / (nu + 1)  (from G_B = G_L + kS*G_S)."""
    return (np.asarray(nu) * np.asarray(XL) + np.asarray(kS) * np.asarray(XS)) / (np.asarray(nu) + 1)

def subadditive(kL, kS, tol=1e-9):
    return (np.asarray(kL) <= 1 + tol) & (np.asarray(kS) <= 1 + tol)

def excess_fixed(rL, rS, rLS):
    """Exact at fixed store rates: (G_B - G_L - G_S)/Var for two linear predictors with correlations rL, rS to the target and rLS to each
    other (G_B = the two-predictor R^2).  With signs chosen so rL, rS >= 0 (no loss of generality),
    positive (joint value) iff rLS < 0 or rLS > 2 rL rS / (rL^2 + rS^2): suppression.  At optimized rates a positive value at the joint optimum is
    necessary, not sufficient, for superadditivity (each single layer re-optimizes its own rate)."""
    return rLS * ((rL ** 2 + rS ** 2) * rLS - 2 * rL * rS) / (1 - rLS ** 2)

def quadrant(XL, XS):
    """Which single layers pay ALONE: 0 neither, 1 local only, 2 shared only, 3 each alone (nu and k then decide).  Exact by definition in
    every model.  It is the best design outside quadrant 3 only under subadditivity (see decide() for the design itself)."""
    XL = np.asarray(XL); XS = np.asarray(XS)
    return np.where(XL > 1, np.where(XS > 1, 3, 1), np.where(XS > 1, 2, 0))
