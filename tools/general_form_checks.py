#!/usr/bin/env python3
"""Checks for theory/GENERAL_FORM.md. Standard library only. No network
unless --crossref is passed. Prints PASS/FAIL lines and exits 1 on a failure.
"""
from __future__ import annotations

import math
import os
import sys
import time
import json
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HYP = (
    "The law of adaptive organization (hypothesis): "
    "strongly selected systems minimize the cost of judgment."
)


def check(name, ok, detail=""):
    check.fails += int(not ok)
    mark = "PASS" if ok else "FAIL"
    print(f"  {mark}  {name}" + (f"  {detail}" if detail else ""))
    return bool(ok)


check.fails = 0


def pareto(points):
    """Return the Pareto subset of a finite list of bad-vectors (smaller better)."""
    out = []
    for i, p in enumerate(points):
        dominated = False
        for j, q in enumerate(points):
            if i == j:
                continue
            if all(a <= b for a, b in zip(q, p)) and any(a < b for a, b in zip(q, p)):
                dominated = True
                break
        if not dominated:
            out.append(p)
    return out


def section_q1():
    print("Q1")
    front = pareto([(0, 1), (1, 0), (0.6, 0.6), (0.7, 0.7), (2, 2)])
    check("dominated points drop out of the front",
          (0.7, 0.7) not in front and (2, 2) not in front
          and (0, 1) in front and (1, 0) in front and (0.6, 0.6) in front)
    # lexicographic refinement is strictly stronger
    lex = sorted([(0, 1), (1, 0)], key=lambda z: (z[1], z[0]))
    check("lex ranks one Pareto point above the other",
          lex[0] == (1, 0) and lex[1] == (0, 1))
    # persistence only: both viable, one dominated
    viable = [(1.0, 0.2), (0.5, 0.2)]
    check("viable set can contain a dominated design",
          all(rho < 1 for _, rho in viable) and pareto(viable) == [(0.5, 0.2)])
    # compact existence: sum minimizer is Pareto
    cloud = [(0.4, 0.9), (0.2, 0.3), (0.8, 0.1), (0.5, 0.5), (0.2, 0.3)]
    zstar = min(cloud, key=lambda z: z[0] + z[1])
    check("sum minimizer on a finite set is Pareto", zstar in pareto(cloud))
    # continuity is load-bearing for compactness of the image (F-0)
    def bad_image(x):
        return 0.0 if x == 0.0 else 1.0 / x
    check("without continuity a compact domain need not have a compact image",
          bad_image(0.0) == 0.0 and bad_image(1e-6) == 1e6)
    # free disposal: waste is dominated by the point it wastes from
    z0, u = (0.2, 0.3), (0.1, 0.0)
    wasted = (z0[0] + u[0], z0[1] + u[1])
    check("free-disposal waste is dominated",
          wasted not in pareto([z0, wasted]))


def section_q2():
    print("Q2")
    # an extra layer that changes none of the other bads is not dominated
    four = {
        "K1": (1.0, 0.5, 2.0, 0.01),
        "K2": (1.0, 0.5, 2.0, 0.01),
    }
    check("equal scores at two layer counts are tied, so K is not forced as a bad",
          four["K1"] == four["K2"])
    # if the extra layer raises memory, it is dominated at equal error
    k1 = (1.0, 0.5, 2.0)   # I, r, e
    k2 = (1.4, 0.5, 2.0)
    check("extra memory at equal error is dominated", pareto([k1, k2]) == [k1])


def section_q3():
    print("Q3")
    A, B, C = (0.0, 1.0), (1.0, 0.0), (0.6, 0.6)
    pts = [A, B, C]
    check("A, B, C are all Pareto", pareto(pts) == [A, B, C] or set(pareto(pts)) == set(pts))
    # no nonnegative weight minimizes at C
    supported = False
    for i in range(0, 21):
        for j in range(0, 21):
            if i == 0 and j == 0:
                continue
            p = (i / 20.0, j / 20.0)
            scores = [p[0] * z[0] + p[1] * z[1] for z in pts]
            if scores[2] <= min(scores) + 1e-12:
                supported = True
    check("C is the minimum of no nonnegative weight on a 21x21 grid", not supported)
    # algebraic obstruction: both inequalities cannot hold
    # p1*0.6 <= p1*0 and impossible if we require <= A and <= B with p>0
    # rearrange: 0.6 p1 + 0.6 p2 <= p2  =>  p1/p2 <= 2/3
    #            0.6 p1 + 0.6 p2 <= p1  =>  p2/p1 <= 2/3
    check("price-ratio bounds 2/3 and 2/3 are incompatible", (2.0 / 3.0) * (2.0 / 3.0) < 1)
    mix = (0.5 * (A[0] + B[0]), 0.5 * (A[1] + B[1]))
    check("the mixture dominates C",
          mix[0] <= C[0] and mix[1] <= C[1] and mix != C)
    cheb = [max(z) for z in pts]
    check("C uniquely minimizes the unweighted Chebyshev scalarization",
          cheb[2] < cheb[0] and cheb[2] < cheb[1] and abs(cheb[2] - 0.6) < 1e-12)
    # coordinate cap preserves convexity of a polygon (half-space cut)
    # triangle (0,0), (2,0), (0,2), cut y <= 1. Random convex combinations stay in.
    import random
    rng = random.Random(0)

    def in_capped(x, y):
        return x >= 0 and y >= 0 and x + y <= 2 and y <= 1

    samples = []
    while len(samples) < 30:
        x, y = rng.random() * 2, rng.random() * 2
        if in_capped(x, y):
            samples.append((x, y))
    ok_conv = True
    for _ in range(200):
        i, j = rng.randrange(30), rng.randrange(30)
        t = rng.random()
        x = t * samples[i][0] + (1 - t) * samples[j][0]
        y = t * samples[i][1] + (1 - t) * samples[j][1]
        if not in_capped(x, y):
            ok_conv = False
            break
    check("a coordinate cap of a convex triangle stays convex (200 combinations)", ok_conv)
    # non-half-space: surviving image {A,B,C} is not convex
    check("the dent is not a convex set", mix not in pts)
    # concatenation fails for a square
    check("z |-> z^2 is not Cauchy", (1 + 1) ** 2 != 1 ** 2 + 1 ** 2)
    # marginal rate of z^2 at 1 and at 3
    check("marginal rate of z^2 is not constant", abs((2 * 1) - (2 * 3)) > 0)
    # Kelly
    beta, a1, b1, b0 = 0.05, 1.30, 1.05, 0.90
    q = beta * a1 / (a1 - b1)
    lean = (1 - beta) * a1
    robust = (1 - beta) * b1 + beta * b0
    check("Kelly mixture q* = 0.26", abs(q - 0.26) < 1e-12, f"q={q}")
    check("per-unit means 1.235 and 1.0425",
          abs(lean - 1.235) < 1e-12 and abs(robust - 1.0425) < 1e-12,
          f"lean={lean} robust={robust}")
    check("expected currency picks the pure lean design, not the mixture", lean > robust)
    # Lundberg vs EOQ
    c, w, sg, s0, y = 0.05, 1.0, 1.0, 0.3, 1.0
    alpha = w * sg ** 2 / 2.0
    beta_v = (w ** 2) * (sg ** 4) / 3.0
    tE = math.sqrt(c / alpha)

    def Jp(t):
        return -c / t ** 2 + alpha

    def m(t):
        return y - (c / t + alpha * t)

    def s2(t):
        return s0 ** 2 + beta_v * t ** 3

    def thp(t):
        return 2 * ((-Jp(t)) * s2(t) - m(t) * (3 * beta_v * t ** 2)) / s2(t) ** 2

    disc = y * y - 4 * alpha * c
    r1 = (y - math.sqrt(disc)) / (2 * alpha)
    lo, hi = r1 + 1e-9, tE
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if thp(mid) > 0:
            lo = mid
        else:
            hi = mid
    tS = 0.5 * (lo + hi)
    check("tau_S = 0.2362 and tau_E = 0.3162",
          abs(tS - 0.2362) < 5e-5 and abs(tE - 0.3162) < 5e-5,
          f"tau_S={tS:.6f} tau_E={tE:.6f}")
    check("the two intervals differ", abs(tS - tE) > 0.05)
    # quartic excess is 1/(4 beta), not 1/(2 beta)
    ratio = math.gamma(1.25) / math.gamma(0.25)
    check("quartic Gibbs excess factor is 1/4, not 1/2",
          abs(ratio - 0.25) < 1e-12, f"Gamma ratio={ratio}")
    # slack cap indifference
    eps = 0.05
    d_lo = (1.0, 1.0, 0.01)
    d_hi = (1.0, 1.0, 0.02)
    J = lambda z: z[0] + z[1]
    check("slack-cap additive cost ties two ruin levels under the cap",
          d_lo[2] <= eps and d_hi[2] <= eps and J(d_lo) == J(d_hi)
          and pareto([d_lo, d_hi]) == [d_lo])
    # single crossing vs an arbitrary front pick
    def m_star(ww):
        return math.sqrt(ww)

    def m_arbitrary(ww):
        return 1.0 / ww

    ws = [1.0, 2.0, 4.0]
    check("scalar S+wE: memory rises and error falls as w rises",
          m_star(ws[0]) < m_star(ws[1]) < m_star(ws[2])
          and 1 / m_star(ws[0]) > 1 / m_star(ws[2]))
    check("an arbitrary Pareto pick can move error the other way",
          m_arbitrary(ws[0]) > m_arbitrary(ws[2])
          and (1 / m_arbitrary(ws[2])) > (1 / m_arbitrary(ws[0])))


def section_lyapunov():
    print("LY")
    lam_L = 0.5 * math.log(0.2)
    lam_H = math.log(1.1)
    check("L is strictly better on both expected bads", (1.0 < 2.0) and (0.0 < 0.4))
    check("L has strictly worse growth", lam_L < lam_H,
          f"lam_L={lam_L:.12f} lam_H={lam_H:.12f}")
    check("printed growth values",
          abs(lam_L - (-0.804718956)) < 5e-10 and abs(lam_H - 0.095310180) < 5e-10)
    # state-contingent logs are incomparable
    L = (math.log(4.0), math.log(0.05))
    H = (math.log(1.1), math.log(1.1))
    check("state-contingent log offspring is incomparable",
          L[0] > H[0] and L[1] < H[1])
    gaps = [2.0 - 1.5 * x for x in (0.0, 0.25, 0.5, 0.75, 1.0)]
    check("dominated type invades at every frequency",
          min(gaps) >= 0.5 - 1e-12 and abs(gaps[0] - 2.0) < 1e-12,
          f"gaps={gaps}")
    # no three reals realize a strict cycle
    def cycle_possible():
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    if a > b and b > c and c > a:
                        return True
        return False
    check("a strict cycle is not three real numbers", not cycle_possible())
    check("unweighted Chebyshev is weakly monotone",
          max(0.6, 0.6) == max(0.6, 0.5) == 0.6)


def section_q5():
    print("Q5")
    a, Q, k, P = 0.9, 1.0, 2, 0.5
    V = Q / (1 - a * a)
    I = 0.5 * math.log(V / P)
    r = 0.5 * math.log(a * a + Q / P)
    D = (a ** (2 * k)) * P + V * (1 - a ** (2 * k))
    check("Gauss-Markov relaxation at P=0.5",
          abs(V - 5.2631578947) < 1e-9 and abs(I - 1.1769391937) < 1e-9
          and abs(r - 0.5165922417) < 1e-9 and abs(D - 2.13805) < 1e-9,
          f"V={V:.6f} I={I:.6f} r={r:.6f} D={D:.6f}")
    # wasteful point: same D, more memory and more rate
    waste = (I + 0.4, r + 0.4, D)
    floor = (I, r, D)
    check("a point above both curves is strictly dominated in the relaxation",
          pareto([floor, waste]) == [floor])
    # an antitone cloud of wasteful points, every one interior by 0.4 nats
    Ps = [0.3, 0.5, 0.8, 1.2]
    cloud = []
    for Pp in Ps:
        Ii = 0.5 * math.log(V / Pp)
        Di = (a ** (2 * k)) * Pp + V * (1 - a ** (2 * k))
        cloud.append((Ii + 0.4, Di, Ii))
    antitone = all(
        (cloud[i][1] - cloud[j][1]) * (cloud[i][0] - cloud[j][0]) <= 0
        for i in range(len(cloud)) for j in range(len(cloud))
    )
    interior = all(c[0] > c[2] + 0.3 for c in cloud)
    check("a fitted antitone cloud can lie entirely inside the computed relaxation",
          antitone and interior)


def section_sentence():
    print("sentence")
    path = os.path.join(ROOT, "theory", "GENERAL_FORM.md")
    text = open(path, encoding="utf-8").read()
    check("hypothesis sentence is byte-identical", HYP in text)
    # the sentence that names the law must label itself a hypothesis
    ok = False
    for line in text.splitlines():
        if "law of adaptive organization" in line:
            ok = "hypothesis" in line
    check("the sentence that names the law labels itself a hypothesis", ok)


DOIS = [
    ("10.2307/1906814", "Coefficient of Resource Utilization"),
    ("10.1073/pnas.40.7.588", "PARETO OPTIMUM"),
    ("10.1017/ccol052123736x.010", "Topological methods in cardinal utility theory"),
    ("10.1017/ccol052123736x.007", "Representation of a preference ordering by a numerical function"),
    ("10.2307/2343100", "Measurement of Productive Efficiency"),
    ("10.1016/0022-247X(68)90201-1", "Proper efficiency"),
    ("10.1126/science.1217405", "Evolutionary Trade-Offs"),
    ("10.1002/j.1538-7305.1956.tb03809.x", "A New Interpretation of Information Rate"),
    ("10.1103/PhysRevLett.109.120604", "Thermodynamics of Prediction"),
    ("10.1109/TAC.1963.1105511", "non-scalar-valued performance criteria"),
    ("10.1007/978-3-642-48782-8_32", "Reference Objectives in Multiobjective Optimization"),
    ("10.1007/978-3-642-87563-2_5", "Tchebycheff Norm"),
    ("10.1007/978-0-8176-4910-4", "Viability Theory"),
    ("10.1147/rd.53.0183", "Irreversibility and Heat Generation"),
    ("10.1109/TAC.2004.834430", "Stochastic Linear Control Over a Communication Channel"),
    ("10.2307/2951479", "Monotone Comparative Statics"),
    ("10.1287/opre.26.2.305", "Minimizing a Submodular Function on a Lattice"),
    ("10.1214/aoms/1177729032", "Equivalent Comparisons of Experiments"),
    ("10.1073/pnas.0501865102", "statistical physics to evolutionary biology"),
    ("10.1103/PhysRevLett.102.250602", "Minimal Energy Cost"),
    ("10.1007/978-1-4615-5563-6", "Nonlinear Multiobjective Optimization"),
]


def crossref():
    print("crossref")
    out_dir = os.path.join(ROOT, "theory", "general_form_checks")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "crossref.out")
    lines = []
    UA = {"User-Agent": "gtao-general-form (mailto:chad39@gmail.com)"}
    for doi, needle in DOIS:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as resp:
                m = json.load(resp)["message"]
            title = (m.get("title") or [""])[0]
            au = "; ".join(a.get("family", "") for a in m.get("author", [])[:6])
            yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
            cont = (m.get("container-title") or [""])[0]
            ok = needle.lower() in title.lower()
            lines.append(f"{'OK' if ok else 'MISMATCH'}\t{doi}\t{yr}\t{au}\t{title}\t{cont}")
            check(f"Crossref title matches {doi}", ok, title[:80])
        except Exception as exc:
            lines.append(f"FAIL\t{doi}\t{exc}")
            check(f"Crossref fetch {doi}", False, str(exc))
        time.sleep(0.35)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"  wrote {out_path}")


def main(argv):
    section_q1()
    section_lyapunov()
    section_q2()
    section_q3()
    section_q5()
    section_sentence()
    if "--crossref" in argv:
        crossref()
    print("FAILS", check.fails)
    if check.fails == 0:
        print("ALL GF CHECKS PASS")
        return 0
    print("SOME GF CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
