"""The face figure: 'Where adaptive systems should sit'.   nice -n 19 python3 figures/face.py     (about 1-2 minutes)
Needs figures/face_tables.json (from figures/face_model.py).  Regions are the argmin of J over designs in ONE illustrative model world
(14 real-pole time scales, n = 10 units reading the same world, see face_model.py and face_regions.py), with sensing optimized and the
master equation's ruin constraint imposed (assumed income, reserve and ruin probability, face_regions.py):
  colour / number = layers per unit in the best design (0..6+), hatching = federate (n semi-independent units that pay n times the
  upkeep and sensing, lose the pooling of their reads, and buy zero latency), dark grey = not viable (no design meets the ruin constraint).
Nothing is hand-drawn except the labels and the hypothesized circles.
Writes figures/face.png (1600x1000), figures/face_regions.json (the label grid that tools/test_face_regions.py rechecks) and
figures/face_dots.json (the model's design at each circle's centre)."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import face_regions as fr
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

R = np.logspace(-1, 9.8, 440); LAT = np.logspace(-6, 4, 61)
KK = np.zeros((len(LAT), len(R)), int); FF = np.zeros_like(KK); BB = np.zeros_like(KK)
for i, l in enumerate(LAT):
    K, F, _, _, bind = fr.best_design(R, l); KK[i] = K; FF[i] = F; BB[i] = bind
json.dump(dict(R=R.tolist(), lat=LAT.tolist(), K=KK.tolist(), fed=FF.tolist(), params=dict(n=fr.N_UNITS, eta=fr.ETA, beta=fr.BETA, eps=fr.EPS)),
          open(os.path.join(HERE, 'face_regions.json'), 'w'))

# hypothesized placements: name, log10 R, log10 (l/tau_fast), half-width in decades x, y, label (dx, dy decades), ha, selection ('strong' | 'weak')
SYS = [
 ('E. coli', 1.0, -0.5, 0.4, 0.55, (-0.55, 0.0), 'right', 'strong'),
 ('small team', 1.55, -1.4, 0.4, 0.5, (0.55, 0.0), 'left', 'strong'),
 ('immune system', 2.15, -0.9, 0.4, 0.5, (0.55, 0.0), 'left', 'strong'),
 ('ant colony', 2.2, 0.95, 0.4, 0.5, (-0.55, 0.0), 'right', 'strong'),
 ('firm', 2.45, 0.2, 0.4, 0.5, (0.55, 0.0), 'left', 'strong'),
 ('city', 2.9, 1.15, 0.4, 0.5, (0.55, 0.0), 'left', 'weak'),
 ('nation-state', 5.0, 1.3, 0.55, 0.55, (0.7, 0.0), 'left', 'weak'),
 ('global economy', 7.0, 1.8, 0.6, 0.55, (0.0, 1.0), 'center', 'weak'),
]
dots = {}
for name, lx, ly, *_ in SYS:
    K, F, J, S, bd = fr.best_design(np.array([10 ** lx]), 10 ** ly); dots[name] = dict(logR=lx, loglat=ly, K=int(K[0]), federated=bool(F[0]), ruin_binds=bool(bd[0]))
json.dump(dots, open(os.path.join(HERE, 'face_dots.json'), 'w'), indent=1)

COL = ['#e3e3e3', '#d6e8f5', '#b3d3ec', '#8dbbe0', '#6aa2d3', '#4a86c0', '#2f68a8']     # layers 0..6
NV = '#5a5a5a'                                                                              # not viable
fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
X, Y = np.meshgrid(R, LAT)
Z = np.where(KK < 0, -1, np.minimum(KK, 6))
ax.pcolormesh(X, Y, Z, cmap=ListedColormap([NV] + COL), vmin=-1.5, vmax=6.5, shading='nearest')
plt.rcParams['hatch.linewidth'] = 1.0
ax.contourf(X, Y, FF, levels=[0.5, 1.5], colors='none', hatches=['//'], edgecolors='#d98a2b')
ax.contour(X, Y, FF, levels=[0.5], colors='#c26a00', linewidths=3)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(R[0], R[-1]); ax.set_ylim(LAT[0], LAT[-1])
out = [pe.withStroke(linewidth=5, foreground='white')]
# layer-count digits above the map, centred on each band of the lowest-latency row (central design, computed from the labels)
row = KK[0]
for k in range(0, 7):
    idx = np.where((np.minimum(row, 6) == k) & (row >= 0))[0]
    if len(idx):
        ax.text(10 ** np.mean(np.log10(R[idx])), 1.045, str(k) + ('+' if k == 6 else ''), ha='center', va='center', fontsize=30, weight='bold', color='#111111', transform=ax.get_xaxis_transform(), clip_on=False)
ax.text(10 ** 6.4, 10 ** -5.0, 'CENTRAL: one pooled\ntracker, reads travel', ha='center', va='center', fontsize=20, weight='bold', color='#1f4f80', path_effects=out)
ax.text(10 ** 3.7, 10 ** 3.05, 'FEDERATE: semi-independent units,\neach with its own layers; pays n× upkeep and\nsensing, loses pooling, buys zero latency', ha='center', va='center', fontsize=17, weight='bold', color='#8a4a00', path_effects=out)
ax.text(10 ** -0.85, 10 ** 2.9, 'NOT\nVIABLE', ha='left', va='center', fontsize=22, weight='bold', color='white')
ax.text(10 ** 7.6, 10 ** -2.6, 'more layers need more\nseparated scales in the\nworld (14 here), not size', ha='center', va='center', fontsize=16, color='#333333', path_effects=out)

th = np.linspace(0, 2 * np.pi, 200)
for name, lx, ly, wx, wy, (dx, dy), ha, sel in SYS:
    ls = '-' if sel == 'strong' else (0, (4, 2))
    ax.plot(10 ** (lx + wx * np.cos(th)), 10 ** (ly + wy * np.sin(th)), color='#111111', lw=3.0, ls=ls)
    ax.fill(10 ** (lx + wx * np.cos(th)), 10 ** (ly + wy * np.sin(th)), color='white', alpha=0.35)
    ax.plot([10 ** lx], [10 ** ly], 'o', color='#111111', ms=8)
    if dx == 0: xy, xyt = (10 ** lx, 10 ** (ly + (wy if dy > 0 else -wy))), (10 ** lx, 10 ** (ly + dy))
    else: xy, xyt = (10 ** (lx + (wx if dx > 0 else -wx)), 10 ** ly), (10 ** (lx + dx + (wx if dx > 0 else -wx)), 10 ** (ly + dy))
    ax.annotate(name + ('' if sel == 'strong' else '*'), xy=xy, xytext=xyt,
                ha=ha, va='center', fontsize=20, weight='bold', color='#111111', path_effects=out,
                arrowprops=dict(arrowstyle='-', lw=1.8, color='#111111', shrinkA=0, shrinkB=0))
ax.set_xlabel('Stakes over upkeep   R = w·Var/h   (any currency; not size)', fontsize=23, labelpad=6)
ax.set_ylabel('Latency over fast scale  ℓ/τ_fast', fontsize=24, labelpad=10)
ax.tick_params(labelsize=21, length=8, width=2)
fig.text(0.5, 0.958, 'Where adaptive systems should sit', ha='center', va='center', fontsize=42, weight='bold')
fig.text(0.5, 0.908, 'Hypothesized positions, not measurements   ·   Illustrative model world', ha='center', va='center', fontsize=26, weight='bold', color='#cc0000')
fig.text(0.5, 0.088, 'Number: layers per unit.  Hatched: federate.  Grey: not viable (assumed income can\u2019t cover upkeep at the ruin limit).', ha='center', fontsize=17, color='#222222')
fig.text(0.5, 0.055, 'Size enters through R and latency, not directly.  Circles: guesses.   * selection weak or unknown: model position only.', ha='center', fontsize=18, color='#222222')
fig.text(0.5, 0.022, 'One 1/f world of 14 time scales, 10 units; colours belong to this world.  Details: figures/face_placements.md  ·  CC0', ha='center', fontsize=15, color='#444444')
fig.subplots_adjust(left=0.085, right=0.985, top=0.80, bottom=0.23)
fig.savefig(os.path.join(HERE, 'face.png'), dpi=100)
print('saved face.png; max layers in grid', KK.max(), '; viable fraction', float((KK >= 0).mean()), '; central multi-layer fraction of viable', float(((KK >= 2) & (FF == 0)).sum() / (KK >= 0).sum()),
      '; ruin binds somewhere', bool(BB.any()))
