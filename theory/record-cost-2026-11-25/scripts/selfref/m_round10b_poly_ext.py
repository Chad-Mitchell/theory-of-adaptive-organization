# Review extension of M3h (m_round10b_poly.py), added at the independent review of PR #295, 26 November 2026.
# Same cost and same polygon distance as M3h; extends the horizons and tests the (2T+1)-gon at each T.
# Question: does some odd polygon beat the disk's optimum T*sin^2(pi/2T) at every tested horizon T?
import math
from m_round10b_poly import poly_dist, v
def best_cost(n, T):
    d = [poly_dist(n, v(n, 0), v(n, j)) for j in range(n)]
    targets = [j for j in range(n) if d[j] > 1 - 1e-9]
    INF = 1e9; best = [INF] * n; best[0] = 0
    for t in range(T):
        nb = best[:]
        for i in range(n):
            if best[i] < INF:
                for j in range(n): nb[j] = min(nb[j], best[i] + d[(j - i) % n] ** 2)
        best = nb
    return min(best[j] for j in targets)
if __name__ == "__main__":
    for T in list(range(1, 13)) + [16, 20]:
        disk = T * math.sin(math.pi / (2 * T)) ** 2
        res = {n: best_cost(n, T) for n in range(3, 2 * T + 8, 2)}
        nb = min(res, key=res.get)
        print(f"M3h-ext T={T} disk={disk:.4f} | best odd n-gon (n=3..{2*T+7}) n={nb} cost={res[nb]:.4f}; (2T+1)-gon={res[2*T+1]:.4f}; odd polygon strictly below disk: {res[nb] < disk - 1e-9}")
