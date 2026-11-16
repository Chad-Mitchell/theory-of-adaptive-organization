"""Payoff-selected learner (in-model). A learner sees an experience record of E_SW expected switches and picks, from a
fixed candidate grid of the family F(pp, g) (nonlinear members and the linear subfamily), the candidate with the lowest
realized error rate on that record (common random numbers within a learner). Its adaptation time is then measured on a
fresh test record of TEST_SW expected switches. Nothing here uses the outcome arms' learner results before the lock."""
import numpy as np, math, sys
sys.path.insert(0, '.'); from core import run, bayes_params, kalman_pole
N = 1.0; D = 0.01
PPX = np.exp(np.linspace(math.log(1/8), math.log(8), 13))      # pp = p * PPX
GX = np.exp(np.linspace(math.log(1/16), math.log(4), 13))       # g = gBayes * GX (nonlinear members)
POLE_TX = np.exp(np.linspace(math.log(1/8), math.log(8), 25))   # linear members: 1-pole = (1-kalman pole) * POLE_TX

def candidates(lam, mu):
    p, gB = bayes_params(lam, mu, N, D); pole, _ = kalman_pole(lam, mu, N, D)
    c = [(p * a, gB * b, False) for a in PPX for b in GX]
    c += [((1 - pole) * t / 2, 1.0, True) for t in POLE_TX]
    return c

def learner(lam, mu, E_SW, TEST_SW, seed):
    c = candidates(lam, mu)
    nexp = int(E_SW / (lam * D)); ntest = int(TEST_SW / (lam * D))
    errs = [run(lam, mu, N, D, pp, g, nexp, seed, lin)[3] for pp, g, lin in c]
    j = int(np.argmin(errs)); pp, g, lin = c[j]
    t = run(lam, mu, N, D, pp, g, ntest, 10_000_000 + seed, lin)
    return dict(j=j, lin=lin, pp_over_p=pp / bayes_params(lam, mu, N, D)[0], g_over_gB=(g / bayes_params(lam, mu, N, D)[1]) if not lin else 0.0,
                exp_err=errs[j], tA=t[0] / t[2], nsw_test=t[2])

from core import run2
def mse_of(r, mu):
    shx, shh, n = r[4], r[5], r[6]
    return (n * mu * mu - shx * shx / shh) / n if shh > 0 else mu * mu

def learner_mse(lam, mu, E_SW, TEST_SW, seed):
    """Same as learner() but the payoff is squared error of the best-scaled estimate (scale fitted on the experience)."""
    c = candidates(lam, mu)
    nexp = int(E_SW / (lam * D)); ntest = int(TEST_SW / (lam * D))
    m = [mse_of(run2(lam, mu, N, D, pp, g, nexp, seed, lin), mu) for pp, g, lin in c]
    j = int(np.argmin(m)); pp, g, lin = c[j]
    t = run(lam, mu, N, D, pp, g, ntest, 10_000_000 + seed, lin)
    pB, gB = bayes_params(lam, mu, N, D)
    return dict(j=j, lin=lin, pp_over_p=pp / pB, g_over_gB=(g / gB) if not lin else 0.0, exp_mse=m[j], tA=t[0] / t[2], nsw_test=t[2])
