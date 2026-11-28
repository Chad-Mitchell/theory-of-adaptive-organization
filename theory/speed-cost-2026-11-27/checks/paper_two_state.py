"""PAPER values: the symmetric two-state copy with the toward-rate at the cap (closed form, no search).
Heat/kT = r (1-2e) ln( G (1-e) / (e G - r (1-2e)) ), feasible iff e > r/(G+2r).  Excess E2 = heat / (r L(e)) - 1.
Prints the thirteen grid points of the scored arm A and the ratios E2(G=100)/E2(G=1000) used by bar B3."""
import numpy as np
from sc_lib import two_state_closed, floor_heat, eps_min_two_state

GRID_G = (5, 20, 100, 1000)
GRID_EPS = (0.05, 0.1, 0.2, 0.3)
FEAS = 1.25     # a grid point is scored only if eps >= FEAS * r/(G+2r)

TOY_GRID = [(7, 0.35), (50, 0.15), (12, 0.25), (30, 0.12)]     # off the scored grid, used only by --toy

def grid(toy=False):
    if toy:
        return list(TOY_GRID)
    return [(G, e) for G in GRID_G for e in GRID_EPS if e >= FEAS * eps_min_two_state(G)]

if __name__ == '__main__':
    pts = grid()
    print('points', len(pts))
    E2 = {}
    for G, e in pts:
        h, am, ap = two_state_closed(G, e)
        E2[(G, e)] = h / floor_heat(e) - 1
        print(f'G={G:<5} eps={e:<5} heat={h:.9f} floor={floor_heat(e):.9f} E2={E2[(G,e)]:.9f} a_minus={am:.6f}')
    for e in GRID_EPS:
        print(f'E2(100)/E2(1000) at eps={e}: {E2[(100, e)] / E2[(1000, e)]:.6f}')
