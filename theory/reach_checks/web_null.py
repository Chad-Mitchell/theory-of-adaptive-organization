#!/usr/bin/env python3
"""REACH check 1: what do proximity graphs give for free? (null models for the cosmic-web network metrics)
Run: nice -n 19 python3 web_null.py > web_null.out
Question: Vazza & Feletti 2020 and Coutinho et al. 2016 compare cosmic-web proximity networks with Erdos-Renyi graphs.
What does a pure proximity rule give on (a) Poisson points and (b) clustered points, with no gravity and no model?
Periodic unit cube; numpy/scipy/networkx; fixed seeds."""
import numpy as np, networkx as nx
from scipy.spatial import cKDTree
rng = np.random.default_rng(20261118)

def poisson(n): return rng.random((n, 3))
def neyman_scott(n, nparent, sigma):
    par = rng.random((nparent, 3)); idx = rng.integers(0, nparent, n)
    return (par[idx] + rng.normal(0, sigma, (n, 3))) % 1.0

def radius_graph(P, k_target):
    n = len(P); V = 1.0
    r = (3 * k_target / (4 * np.pi * n)) ** (1 / 3)          # mean degree k for Poisson
    t = cKDTree(P, boxsize=1.0)
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(t.query_pairs(r))
    return G, r

def stats(G):
    d = np.array([x for _, x in G.degree()])
    cc = nx.average_clustering(G)
    try: ass = nx.degree_assortativity_coefficient(G)
    except Exception: ass = float('nan')
    return dict(mean_k=d.mean(), var_over_mean=d.var()/d.mean(), max_k=int(d.max()), clustering=cc, assort=ass)

def knn_indegree(P, k):
    t = cKDTree(P, boxsize=1.0); _, nb = t.query(P, k + 1)
    indeg = np.bincount(nb[:, 1:].ravel(), minlength=len(P))
    return indeg

n = 4000
print("N =", n, "points per box; periodic unit cube; seed 20261118")
print("\n(1) Radius-graph (proximity) rule, mean degree ~4 for Poisson")
print("%-34s %7s %9s %6s %11s %8s" % ("point set", "mean_k", "var/mean", "max_k", "clustering", "assort"))
for name, P in [("Poisson (no structure)", poisson(n)),
                ("Neyman-Scott, 200 parents, s=0.03", neyman_scott(n, 200, 0.03)),
                ("Neyman-Scott, 60 parents, s=0.02", neyman_scott(n, 60, 0.02))]:
    G, r = radius_graph(P, 4.0); s = stats(G)
    print("%-34s %7.2f %9.2f %6d %11.3f %8.3f" % (name, s['mean_k'], s['var_over_mean'], s['max_k'], s['clustering'], s['assort']))
G = nx.gnp_random_graph(n, 4.0 / (n - 1), seed=1); s = stats(G)
print("%-34s %7.2f %9.2f %6d %11.4f %8.3f" % ("Erdos-Renyi, same N and mean_k", s['mean_k'], s['var_over_mean'], s['max_k'], s['clustering'], s['assort']))
print("\n(2) Directed nearest-neighbour rule (as in Coutinho et al. 2016 model M3: link to the closest galaxy)")
print("%-34s %6s %7s %9s %6s" % ("point set", "k_out", "mean_in", "var/mean", "max_in"))
for name, P in [("Poisson", poisson(n)), ("Neyman-Scott, 60 parents, s=0.02", neyman_scott(n, 60, 0.02))]:
    for k in (1, 4):
        d = knn_indegree(P, k)
        print("%-34s %6d %7.2f %9.2f %6d" % (name, k, d.mean(), d.var()/d.mean(), d.max()))
print("\nReading: a proximity rule alone gives clustering far above Erdos-Renyi, and (for a nearest-neighbour link rule)"
      " an in-degree capped by geometry, so 'no hubs' is partly built into the construction.")

print("\n(3) Hub-and-spoke references (arithmetic, not data): a star with 30 leaves and a Barabasi-Albert graph (m=2, N=4000)")
G = nx.star_graph(30); print("star: degree assortativity r = %.3f" % nx.degree_assortativity_coefficient(G))
G = nx.barabasi_albert_graph(4000, 2, seed=1); d = [x for _, x in G.degree()]
print("BA:   r = %.3f  clustering = %.4f  max degree = %d  mean degree = %.2f" % (nx.degree_assortativity_coefficient(G), nx.average_clustering(G), max(d), np.mean(d)))
print("Reading: hub-and-spoke growth gives r <= 0 and almost no clustering; proximity gives r > 0 and high clustering. They are different signatures.")
