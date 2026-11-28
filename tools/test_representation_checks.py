"""CT22 binding multiplier and the affine-scale arithmetic in theory/REPRESENTATION.md."""
import math
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "theory", "representation_checks", "binding_multiplier.py")


def test_binding_multiplier_script_passes():
    r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RESULT: PASS" in r.stdout
    assert "0 FAIL" in r.stdout


def test_multiplier_identity_independent_of_the_script():
    """Recompute mu = J'/theta' at B=0.5 from the diffusion formulas, not from the script's report."""
    y, c, w, sg, s0, eps = 1.0, 0.05, 1.0, 1.0, 0.3, 1e-3
    alpha = w * sg * sg / 2.0
    beta = (w * w) * (sg ** 4) / 3.0

    def J(t):
        return c / t + alpha * t

    def Jp(t):
        return -c / t**2 + alpha

    def m(t):
        return y - J(t)

    def s2(t):
        return s0 * s0 + beta * t**3

    def th(t):
        return 2.0 * m(t) / s2(t)

    def thp(t):
        mp = -Jp(t)
        s2p = 3.0 * beta * t * t
        return 2.0 * (mp * s2(t) - m(t) * s2p) / s2(t)**2

    tE = math.sqrt(c / alpha)
    # bisection for the unique root of theta' on (0.05, tE), then for theta = ln(1/eps)/B
    def bisect(f, a, b):
        fa = f(a)
        for _ in range(80):
            mid = 0.5 * (a + b)
            if fa * f(mid) <= 0:
                b = mid
            else:
                a, fa = mid, f(mid)
        return 0.5 * (a + b)

    tS = bisect(thp, 0.06, tE)
    B = 0.5
    treq = math.log(1.0 / eps) / B
    tau = bisect(lambda t: th(t) - treq, tS, tE)
    mu = Jp(tau) / thp(tau)
    assert tS < tau < tE
    assert abs(tau - 0.29905) < 1e-4
    assert abs(mu - 0.005231) < 1e-4
    assert mu > 0
    assert abs(Jp(tau) - mu * thp(tau)) < 1e-9
    # phi' = m'' s^2 - m (s^2)'' is negative at the binding point
    phip = (-2.0 * c / tau**3) * s2(tau) - m(tau) * (6.0 * beta * tau)
    assert phip < 0
    assert thp(tau) != 0


def test_dent_is_pareto_and_unsupported():
    A, B, C = (0.0, 1.0), (1.0, 0.0), (0.6, 0.6)

    def dominates(p, q):
        return all(x <= y for x, y in zip(p, q)) and any(x < y for x, y in zip(p, q))

    assert not any(dominates(p, q) for p in (A, B, C) for q in (A, B, C) if p is not q)
    for i in range(0, 21):
        w1 = i / 20.0
        w = (w1, 1.0 - w1)
        scores = [w[0] * p[0] + w[1] * p[1] for p in (A, B, C)]
        assert scores[2] > min(scores[0], scores[1])
    assert dominates((0.5, 0.5), C)
