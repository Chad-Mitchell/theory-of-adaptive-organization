"""The face figure: 'One map for every adaptive system'.   nice -n 19 python3 figures/face.py     (about 1-2 minutes)
Needs figures/face_tables.json (from figures/face_model.py).  Regions are the argmin of J over designs in ONE illustrative model world
(14 real-pole time scales, see face_model.py), with sensing optimized: colour = number of layers per unit (0..6), hatching = federate
(split into semi-independent units, each with its own layers).  Nothing is hand-drawn except the labels and the hypothesized circles.
Writes figures/face.png (1600x1000) and figures/face_regions.json (the label grid that tools/test_face_regions.py rechecks)."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import face_regions as fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

R = np.logspace(-1, 9.5, 420); LAT = np.logspace(-2, 4, 49)
KK = np.zeros((len(LAT), len(R)), int); FF = np.zeros_like(KK)
for i, l in enumerate(LAT):
    K, F, _, _ = fr.best_with_spend(R, l); KK[i] = K; FF[i] = F
json.dump(dict(R=R.tolist(), lat=LAT.tolist(), K=KK.tolist(), fed=FF.tolist()), open(os.path.join(HERE, 'face_regions.json'), 'w'))

COL = ['#e3e3e3', '#d6e8f5', '#b3d3ec', '#8dbbe0', '#6aa2d3', '#4a86c0', '#2f68a8']     # layers 0..6
KS = min(KK.max(), 6)
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
X, Y = np.meshgrid(R, LAT)
ax.pcolormesh(X, Y, np.minimum(KK, 6), cmap=ListedColormap(COL), vmin=-0.5, vmax=6.5, shading='nearest')
plt.rcParams['hatch.linewidth'] = 1.0
ax.contourf(X, Y, FF, levels=[0.5, 1.5], colors='none', hatches=['//'], edgecolors='#d98a2b')
ax.contour(X, Y, FF, levels=[0.5], colors='#c26a00', linewidths=3)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(R[0], R[-1]); ax.set_ylim(LAT[0], LAT[-1])
out = [pe.withStroke(linewidth=5, foreground='white')]
# layer-count digits in a strip above the map, centred on each band of the lowest-latency row (computed from the labels)
row = KK[0]
for k in range(0, 7):
    idx = np.where(np.minimum(row, 6) == k)[0]
    if len(idx):
        xc = 10 ** np.mean(np.log10(R[idx]))
        ax.text(xc, 1.045, str(k) + ('+' if k == 6 else ''), ha='center', va='center', fontsize=34, weight='bold', color='#111111', transform=ax.get_xaxis_transform(), clip_on=False)
ax.text(10 ** 2.35, 10 ** 3.1, 'FEDERATE: split into semi-independent units,\neach with its own layers (not a dead end)', ha='center', va='center', fontsize=21, weight='bold', color='#8a4a00', path_effects=out)
ax.annotate('', xy=(3e8, 1.5e3), xytext=(1.2e8, 1.5e3), arrowprops=dict(arrowstyle='->', lw=3, color='#555555'))
ax.text(7.5e8, 4.5e3, 'no size ceiling:\nit goes on', ha='right', va='center', fontsize=18, color='#444444', path_effects=out)

# hypothesized placements: name, log10 R, log10 (l/tau_fast), half-width in decades x, y, label offset (dx, dy decades), ha
th = np.linspace(0, 2 * np.pi, 200)
SYS = [
 ('E. coli', 0.95, -0.55, 0.45, 0.4, (-0.55, 0.0), 'right'),
 ('small team', 1.55, -1.45, 0.45, 0.3, (0.55, -0.1), 'left'),
 ('immune system', 2.15, -0.9, 0.5, 0.45, (0.62, 0.12), 'left'),
 ('ant colony', 1.65, 0.95, 0.5, 0.45, (-0.3, 0.7), 'center'),
 ('firm', 2.45, 0.2, 0.45, 0.4, (0.95, -0.1), 'left'),
 ('city', 2.85, 1.15, 0.45, 0.4, (0.0, 0.62), 'center'),
 ('nation-state', 5.0, 1.3, 0.7, 0.45, (0.0, 0.75), 'center'),
 ('global economy', 7.0, 1.8, 0.8, 0.5, (0.0, 0.8), 'center'),
 ('biosphere', 8.5, 0.0, 0.8, 0.5, (0.0, -0.75), 'center'),
]
for name, lx, ly, wx, wy, (dx, dy), ha in SYS:
    ax.plot(10 ** (lx + wx * np.cos(th)), 10 ** (ly + wy * np.sin(th)), color='#111111', lw=3.2)
    ax.fill(10 ** (lx + wx * np.cos(th)), 10 ** (ly + wy * np.sin(th)), color='white', alpha=0.3)
    ax.plot([10 ** lx], [10 ** ly], 'o', color='#111111', ms=9)
    ax.text(10 ** (lx + dx), 10 ** (ly + dy), name, ha=ha, va='center', fontsize=22, weight='bold', color='#111111', path_effects=out)
ax.set_xlabel('Stakes over upkeep   R = w·Var/h   (any currency; not size)', fontsize=24, labelpad=6)
ax.set_ylabel('Latency over fast scale  ℓ/τ_fast', fontsize=25, labelpad=10)
ax.tick_params(labelsize=22, length=8, width=2)
fig.text(0.5, 0.955, 'One map for every adaptive system', ha='center', va='center', fontsize=42, weight='bold')
fig.text(0.5, 0.905, 'Hypothesized positions, not measurements   ·   Illustrative model world', ha='center', va='center', fontsize=26, weight='bold', color='#cc0000')
fig.text(0.5, 0.098, 'Number above the map and colour: layers per unit in the best design (read effort also optimized). Hatched: federate.', ha='center', fontsize=17, color='#222222')
fig.text(0.5, 0.065, 'Size enters through R and latency, not directly. Circles: order-of-magnitude guesses with wide uncertainty.', ha='center', fontsize=17, color='#222222')
fig.text(0.5, 0.036, 'Model world: 14 non-oscillating time scales, 1 to 3×10⁶ fast units, about 1/f. Layers = first-order stores; a rhythm would count two.', ha='center', fontsize=14, color='#444444')
fig.text(0.5, 0.012, 'Notes and sources: figures/face_placements.md   ·   A Theory of Adaptive Organization   ·   CC0', ha='center', fontsize=14, color='#444444')
fig.subplots_adjust(left=0.085, right=0.985, top=0.80, bottom=0.215)
fig.savefig(os.path.join(HERE, 'face.png'), dpi=100)
print('saved face.png; max layers in grid', KK.max())
