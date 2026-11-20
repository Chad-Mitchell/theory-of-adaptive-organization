"""Data-collapse figure for the face map.   nice -n 19 python3 figures/face_collapse.py   (seconds; reads the face_collapse_v*.json files)
(a) 3000 random one-component worlds (face_collapse_v1.py) in raw inputs: stakes/upkeep against number of units, coloured by the design a
    brute-force numerical search found best.  The designs overlap.  (b) the same worlds in the map's coordinates (X_L, X_S): the quadrant
    edges at 1 separate NONE, LOCAL and SHARED exactly.  (c) the worlds in the upper-right quadrant on (kappa_L*X_L, kappa_S*X_S): BOTH
    iff both exceed 1; the rest split on nu*(X_L-1) vs X_S-1.  (d) 1500 worlds with the reading price optimized per design (face_collapse_v1b.py):
    net coordinates, same edges.  Writes figures/face_collapse.png."""
import os, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
COL = ['#7a7a7a', '#c25100', '#0b5fa0', '#00785a']; NAME = ['no layer', 'local', 'shared', 'both']
V1 = json.load(open(os.path.join(HERE, 'face_collapse_v1.json'))); V1B = json.load(open(os.path.join(HERE, 'face_collapse_v1b.json')))
V23 = json.load(open(os.path.join(HERE, 'face_collapse_v23.json')))['summary']
L = lambda x: np.log10(np.clip(np.asarray(x, float), 1e-6, None))

def scatter(ax, x, y, b, s=7):
    for k in range(4):
        m = b == k; ax.scatter(x[m], y[m], s=s, c=COL[k], label=f'{NAME[k]} ({m.sum()})', alpha=0.6, lw=0)

def quad(ax):
    ax.axvline(0, color='k', lw=1.6); ax.axhline(0, color='k', lw=1.6)

w = V1['worlds']; b = np.array([r['brute'] for r in w])
fig, axs = plt.subplots(2, 2, figsize=(14, 12), dpi=90)
ax = axs[0, 0]; scatter(ax, L([r['wu'] / r['hl'] for r in w]), L([r['n'] for r in w]) + np.random.default_rng(0).uniform(-0.04, 0.04, len(w)), b)
ax.set_xlabel('log10 stakes per unit \u00f7 local upkeep (raw input)'); ax.set_ylabel('log10 number of units (raw input)')
ax.set_title('(a) raw inputs: the best designs overlap', weight='bold'); ax.legend(loc='lower right', markerscale=2.5, fontsize=10)
XL = np.array([r['XL'] for r in w]); XS = np.array([r['XS'] for r in w])
ax = axs[0, 1]; scatter(ax, L(XL), L(XS), b); quad(ax)
ax.set_xlabel('log10 $X_L$ (local layer: stakes won \u00f7 upkeep)'); ax.set_ylabel('log10 $X_S$ (shared layer: stakes won \u00f7 upkeep)')
ax.set_title(f'(b) map coordinates: edges at 1 are exact  (agreement {V1["summary"]["agree"]:.0%} of {V1["summary"]["M"]})', weight='bold')
ur = (XL > 1) & (XS > 1); kL = np.array([r['kL'] for r in w]); kS = np.array([r['kS'] for r in w])
ax = axs[1, 0]; scatter(ax, L((kL * XL)[ur]), L((kS * XS)[ur]), b[ur], s=9); quad(ax)
ax.set_xlabel('log10 $\\kappa_L X_L$ (local layer\u2019s worth on what the shared one misses)'); ax.set_ylabel('log10 $\\kappa_S X_S$ (shared layer\u2019s worth on what local misses)')
ax.set_title('(c) upper-right quadrant: both iff both > 1', weight='bold'); ax.legend(loc='lower right', markerscale=2.5, fontsize=10)
w2 = V1B['worlds']; b2 = np.array([r['brute'] for r in w2])
ax = axs[1, 1]; scatter(ax, L([r['XL'] for r in w2]), L([r['XS'] for r in w2]), b2); quad(ax)
ax.set_xlabel('log10 $X_L$ net of reading cost'); ax.set_ylabel('log10 $X_S$ net of reading cost')
ax.set_title(f'(d) reading priced: agreement {V1B["summary"]["agree"]:.0%} of {V1B["summary"]["M"]}', weight='bold')
fig.suptitle('Data collapse: the map\u2019s coordinates sort random worlds by their best design', fontsize=18, weight='bold')
fig.text(0.5, 0.012, f'One read stream, two time scales (600 worlds): placing layers one at a time by marginal worth matches the exact best design in '
         f'{V23["v3_greedy_same"]:.0%};\n reading each scale as if it had its own channel matches in {V23["v3_same"]:.0%}.', ha='center', fontsize=12)
fig.text(0.99, 0.5, 'points at $10^{-6}$: worth ≤ 0 (clipped)', rotation=90, va='center', fontsize=9, color='#555555')
fig.tight_layout(rect=(0, 0.05, 0.98, 0.96)); fig.savefig(os.path.join(HERE, 'face_collapse.png')); print('saved face_collapse.png')
