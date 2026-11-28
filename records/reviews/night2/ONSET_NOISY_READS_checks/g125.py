"""ONSET-NOISY-READS check 5: asymptote f(z)/(g z^b) at alpha = 1.25 and 2.75 (not covered by fz.py), M = 1000, 2000, 3000."""
from fz import f, g
for H in (0.125, 0.875):
    a = 1+2*H; b = 1-1/a
    for M in (1000, 2000, 3000):
        print(f"alpha={a} M={M}:", [round(f(H, z, M)/(g(a)*z**b), 4) for z in (10, 100, 1e3, 1e4)], flush=True)
