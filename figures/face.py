"""The face figure: 'One map for every adaptive system'. nice -n 19 python3 figures/face.py
Phase diagram of the optimal design in ONE made-up model world (two OU modes tau=1 and 100, equal variance, noise N=0.05,
upkeep h per layer, federation overhead 20h, income 200h; same model as theory/meq_checks/phase.py), on dimensionless axes
R = w*Var/h (stakes over upkeep) and latency/tau_fast, with dotted contours of a measurable currency-free share (the share of
optimal cost spent on upkeep = d ln J*/d ln h, THEORY CT24) and HYPOTHESIZED placements of six systems.
The placements are order-of-magnitude guesses (see figures/face_placements.md); nothing here is a measurement."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'theory', 'layers_checks'))
from lead import E_opt, E_K_lead
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.colors import ListedColormap

a = np.array([1.0, 1/100]); v = np.array([0.5, 0.5]); N = 0.05; Var = v.sum(); h = 1.0; hf = 20.0; y = 200.0
lat = np.logspace(-2, np.log10(30), 60)
E1 = np.array([E_K_lead(a, v, N, 1, l, starts=6) for l in lat]); E2 = np.array([E_opt(a, v, N, l) for l in lat])
E1_0 = E_K_lead(a, v, N, 1, 0.0, starts=6); E2_0 = E_opt(a, v, N, 0.0)
R = np.logspace(-0.7, 3.6, 600); W = R*h/Var
lab = np.zeros((len(lat), len(R)), int); share = np.zeros_like(lab, float)
for i in range(len(lat)):
    Jn = W*Var; J1 = h + W*E1[i]; J2 = 2*h + W*E2[i]
    Jf1 = hf + h + W*E1_0; Jf2 = hf + 2*h + W*E2_0; Jf = np.minimum(Jf1, Jf2); Kf = np.where(Jf1 <= Jf2, 1, 2)
    C = np.vstack([Jn, J1, J2, Jf]); k = C.argmin(0); best = C.min(0); k[best > y] = 4; lab[i] = k
    up = np.vstack([0*R, h + 0*R, 2*h + 0*R, hf + Kf*h]); kk = np.minimum(k, 3)
    share[i] = up[kk, np.arange(len(R))]/C[kk, np.arange(len(R))]

BLUE1, BLUE2, GREY, ORANGE, RED = '#cfe3f3', '#8fbfe6', '#e6e6e6', '#fcd9a8', '#f1a9a0'
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
X, Y = np.meshgrid(R, lat)
ax.pcolormesh(X, Y, lab, cmap=ListedColormap([GREY, BLUE1, BLUE2, ORANGE, RED]), vmin=-0.5, vmax=4.5, shading='nearest')
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(R[0], R[-1]); ax.set_ylim(lat[0], lat[-1])
for kreg in (1, 2, 3):
    m = np.ma.masked_where(lab != kreg, share)
    try:
        cs = ax.contour(X, Y, m, levels=[0.1, 0.3, 0.5], colors='#333333', linewidths=1.6, linestyles=':')
        ax.clabel(cs, fmt=lambda val: f'{val:.0%}', fontsize=15, inline=True)
    except Exception: pass
out = [pe.withStroke(linewidth=5, foreground='white')]
for txt, xx, yy in [('no model', 0.55, 0.9), ('one layer', 7.0, 0.02), ('two layers', 330.0, 0.03), ('federate', 560.0, 4.5), ('not viable', 1900.0, 0.5)]:
    ax.text(xx, yy, txt, ha='center', va='center', fontsize=26, weight='bold', color='#222222', alpha=0.55)
# hypothesized placements: (name, log10 R, log10 latency, half-width in decades in x, in y, colour)
SYS = [
 ('E. coli chemotaxis', 0.95, -0.55, 0.38, 0.32),
 ('small team', 1.55, -1.45, 0.34, 0.26),
 ('immune system', 2.15, -0.95, 0.38, 0.4),
 ('ant colony', 1.65, 0.95, 0.4, 0.34),
 ('firm', 2.45, 0.2, 0.34, 0.34),
 ('city', 2.85, 1.15, 0.28, 0.26),
]
th = np.linspace(0, 2*np.pi, 200)
for name, lx, ly, wx, wy in SYS:
    ax.plot(10**(lx + wx*np.cos(th)), 10**(ly + wy*np.sin(th)), color='#111111', lw=3.2)
    ax.fill(10**(lx + wx*np.cos(th)), 10**(ly + wy*np.sin(th)), color='white', alpha=0.28)
    ax.plot([10**lx], [10**ly], 'o', color='#111111', ms=9)
    ax.text(10**lx, 10**(ly - 0.1), name, ha='center', va='top', fontsize=22, weight='bold', color='#111111', path_effects=out)
ax.set_xlabel('Stakes over upkeep   R = w·Var/h   (any currency)', fontsize=25, labelpad=8)
ax.set_ylabel('Latency over fast scale  ℓ/τ_fast', fontsize=25, labelpad=10)
ax.tick_params(labelsize=22, length=8, width=2)
ax.set_title('One map for every adaptive system', fontsize=42, weight='bold', pad=70)
fig.text(0.5, 0.885, 'Hypothesized positions, not measurements   ·   Illustrative model world', ha='center', fontsize=26, weight='bold', color='#b02a1a')
ax.plot([], [], ':', color='#333333', lw=2.2, label='dotted: share of cost spent on upkeep (a currency-free, measurable number)')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.17), fontsize=19, frameon=False)
fig.text(0.5, 0.045, 'Regions: the best design in one made-up model world (two time scales). Circles: order-of-magnitude guesses, wide uncertainty.', ha='center', fontsize=15, color='#444444')
fig.text(0.5, 0.015, 'Notes and sources: figures/face_placements.md   ·   A Theory of Adaptive Organization   ·   CC0', ha='center', fontsize=15, color='#444444')
fig.subplots_adjust(left=0.085, right=0.985, top=0.83, bottom=0.24)
fig.savefig(os.path.join(HERE, 'face.png'), dpi=100)
print('saved', os.path.join(HERE, 'face.png'))
