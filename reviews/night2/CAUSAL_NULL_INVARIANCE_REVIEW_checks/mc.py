"""Own Monte Carlo (numba) of the same sampled world, for cross-checking the grid engine. Independent of the author's code."""
import numpy as np, numba as nb, math
@nb.njit(cache=True)
def sim(lam, mu, N, D, a, bayes_p, g, nsamp, seed, linear):
    np.random.seed(seed)
    p = (1 - math.exp(-2 * lam * D)) / 2; s = math.sqrt(N / D)
    x = 1.0; z = 0.0
    burn = 200000
    nerr = 0; tot = 0.0; tot2 = 0.0; nsw = 0; waiting = False; cnt = 0
    for k in range(burn + nsamp):
        if np.random.random() < p:
            x = -x
            if k >= burn:
                waiting = True; cnt = 0
        y = x * mu + s * np.random.standard_normal()
        if linear:
            z = a * z + y
        else:
            zc = min(max(z, -50.0), 50.0); e = math.exp(zc)
            z = math.log(((1 - bayes_p) * e + bayes_p) / (bayes_p * e + 1 - bayes_p)) + g * y
        if k >= burn:
            if z * x <= 0: nerr += 1
            if waiting:
                cnt += 1
                if z * x > 0:
                    tot += cnt; tot2 += cnt * cnt; nsw += 1; waiting = False
    return nerr / nsamp, tot, tot2, nsw
