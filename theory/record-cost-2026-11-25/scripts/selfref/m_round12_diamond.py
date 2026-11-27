"""Round 12-M: condition (diamond) on every extreme point of max(A,B):
   Phi = mA*mB*(||C||^2-1) - mA*(1-|a|^2) - mB*(1-|b|^2) <= 0  (products give 0).
Pairs from the command line, default: the 17 pairs of the round 12 run. Prints only."""
import sys
import numpy as np
from m_round12_parts import max_vertices
DEFAULT = "P3xP3 sqxsq P5xP5 P6xP6 P7xP7 P8xP8 P5xP6 sqxP6 P3xP6 sqxP5 P9xP9 P10xP10 cube3xcube3 oct3xoct3 cube3xoct3 sqxcube3 P6xoct3".split()
def run(na, nb):
    X = max_vertices(na, nb); dA, dB = X.shape[1:]; mA, mB = dA-1, dB-1
    a = X[:, 1:, 0]; b = X[:, 0, 1:]; C = X[:, 1:, 1:]
    A2 = (a**2).sum(1); B2 = (b**2).sum(1); C2 = (C**2).sum((1, 2))
    phi = mA*mB*(C2-1)-mA*(1-A2)-mB*(1-B2)
    prod = np.array([abs(A2[i]-1) < 1e-9 and abs(B2[i]-1) < 1e-9 and np.allclose(C[i], np.outer(a[i], b[i]), atol=1e-9) for i in range(len(X))])
    ent = ~prod
    mx = phi[ent].max() if ent.any() else float('nan')
    print(f"max({na},{nb}): {len(X)} extreme pts ({prod.sum()} product); entangled: max ||C||^2={C2[ent].max() if ent.any() else float('nan'):.6f}, "
          f"max Phi={mx:+.6f}  -> diamond {'HOLDS' if (not ent.any() or mx <= 1e-9) else 'FAILS'}")
    sys.stdout.flush()
if __name__ == "__main__":
    for s in (sys.argv[1:] or DEFAULT):
        run(*s.split('x'))
