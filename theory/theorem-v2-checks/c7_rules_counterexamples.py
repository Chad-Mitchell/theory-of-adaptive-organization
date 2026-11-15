"""C7. Rule 3 (belief updating), vacuity of 'optimal for some cost', and the no-model persistence counterexample."""
import numpy as np
from scipy import integrate, stats
rng = np.random.default_rng(7)
print("== C7a: Gaussian: posterior mean moves by weight K = prec_signal/(prec_prior+prec_signal) (KNOWN); ex-ante spread rises with precision ==")
for r in [4.0, 1.0, 0.25]:
    K = (1/r)/(1+1/r); print(f"  signal noise var {r}: weight K={K:.3f}; Var(E[X|S]) = K = {K:.3f}")
print("== C7b: heavy-tailed (Cauchy) signal noise: the posterior mean is NOT monotone in the surprise (outlier rejection) ==")
def post_mean(sv):
    num = integrate.quad(lambda x: x*stats.norm.pdf(x)*stats.cauchy.pdf(sv-x, scale=0.5), -30, 30, limit=200)[0]
    den = integrate.quad(lambda x: stats.norm.pdf(x)*stats.cauchy.pdf(sv-x, scale=0.5), -30, 30, limit=200)[0]
    return num/den
print("  signal s:        ", [0.5, 1, 2, 3, 5, 10, 30])
print("  E[X|s] (prior N(0,1)):", [round(post_mean(v), 3) for v in [0.5, 1, 2, 3, 5, 10, 30]])
print("  => a very surprising report moves the belief LESS. Rule 3 'move further the more reliable the signal' holds in the Gaussian")
print("     case and ex ante (Blackwell: more informative experiments give a mean-preserving spread of posteriors), not realization-wise.")
print("== C7c: vacuity. Any deterministic policy pi is the unique optimum of loss l(a,x) = 1[a != pi(x)] ==")
nX, nA = 6, 4; pi = rng.integers(0, nA, nX); L = (np.arange(nA)[:, None] != pi[None, :]).astype(float)
print("  recovered argmin per state == pi:", bool(np.all(L.argmin(0) == pi)))
print("  => 'observed behaviour is optimal for some cost' has no content unless loss and costs are fixed independently of the behaviour.")
print("== C7d: persistence with ZERO predictive information (bet-hedging in an i.i.d. world) ==")
p, o = 0.5, 3.0   # two env states i.i.d., type i reproduces o-fold only in state i
G = p*np.log(p*o)+(1-p)*np.log((1-p)*o); print(f"  growth rate with allocation f=p and no cue: {G:.4f} nats/gen > 0; I_pred of any memory = 0 (i.i.d.)")
T = 2000; lw = np.cumsum(np.log(np.where(rng.random((2000, T)) < p, p*o, (1-p)*o)), 1)
print(f"  simulated lineages, fraction with log-size > 0 after {T} gens: {np.mean(lw[:, -1] > 0):.3f}")
print("  => a self-maintaining lineage persists with no model of the state; it carries a constant (the distribution), which needs no upkeep.")
print("== C7e: rule 1's myopic interrupt/acquire rule can fail: X = S1 xor S2 (each signal alone worthless, both together perfect) ==")
S = rng.integers(0, 2, (200_000, 2)); X = S[:, 0] ^ S[:, 1]
acc = lambda pred: np.mean(pred == X)
print(f"  best accuracy: no signal {max(acc(np.zeros_like(X)), acc(np.ones_like(X))):.3f}; S1 only {max(acc(S[:,0]), acc(1-S[:,0])):.3f};"
      f" S2 only {max(acc(S[:,1]), acc(1-S[:,1])):.3f}; both {acc(S[:,0]^S[:,1]):.3f}")
print("  => one-step VOI of each signal is 0, so a myopic 'stake x chance > cost' rule never acquires either; the optimal plan acquires both.")
print("     The rule is exact only if 'what the outcome would teach' is the full continuation value (then it is the Bellman equation).")
