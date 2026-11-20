"""Data-collapse figure for the face map.   nice -n 19 python3 figures/face_collapse.py   (seconds; reads the face_collapse_v*.json files)
(a) 3000 random one-component worlds (face_collapse_v1.py) in raw inputs: stakes/upkeep against number of units, coloured by the design a
    brute-force numerical search found best.  The designs overlap.  (b) the same worlds in the map's coordinates (X_L, X_S): closed forms plus
    the decision rule agree with brute force, and kappa <= 1 in all of them, so the quadrant edges at 1 separate NONE, LOCAL and SHARED.  (c) the worlds in the upper-right quadrant on (kappa_L*X_L, kappa_S*X_S): BOTH
    iff both exceed 1; the rest split on nu*(X_L-1) vs X_S-1.  (d) 1500 worlds with the reading price optimized per design (face_collapse_v1b.py):
    net coordinates; kappa > 1 worlds circled (value not subadditive: the edges need not decide there, review 26 counterexample A).  Writes figures/face_collapse.png."""
import os, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import face_map as fm
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
ax.set_title(f'(b) closed forms + decision rule agree with brute force\n({V1["summary"]["agree"]:.0%} of {V1["summary"]["M"]}; \u03ba \u2264 1 in all of them)', weight='bold')
ur = (XL > 1) & (XS > 1); kL = np.array([r['kL'] for r in w]); kS = np.array([r['kS'] for r in w])
ax = axs[1, 0]; scatter(ax, L((kL * XL)[ur]), L((kS * XS)[ur]), b[ur], s=9); quad(ax)
ax.set_xlabel('log10 $\\kappa_L X_L$ (local layer\u2019s worth on what the shared one misses)'); ax.set_ylabel('log10 $\\kappa_S X_S$ (shared layer\u2019s worth on what local misses)')
ax.set_title('(c) top-right quadrant: both iff \u03ba$_L$X$_L$ > 1 and \u03ba$_S$X$_S$ > 1', weight='bold'); ax.legend(loc='lower right', markerscale=2.5, fontsize=10)
w2 = V1B['worlds']; b2 = np.array([r['brute'] for r in w2])
ax = axs[1, 1]; scatter(ax, L([r['XL'] for r in w2]), L([r['XS'] for r in w2]), b2); quad(ax)
ax.set_xlabel('log10 $X_L$ net of reading cost'); ax.set_ylabel('log10 $X_S$ net of reading cost')
sup = np.array([r['kL'] > 1 + 1e-6 or r['kS'] > 1 + 1e-6 for r in w2]); q2 = np.array([int(fm.quadrant(r['XL'], r['XS'])) for r in w2])
wrong = (q2 < 3) & (q2 != b2)
ax.scatter(L([r['XL'] for r in np.array(w2)[sup]]), L([r['XS'] for r in np.array(w2)[sup]]), s=26, facecolors='none', edgecolors='k', lw=0.7, label=f'\u03ba > 1 ({sup.sum()})')
ax.legend(loc='lower right', markerscale=1.5, fontsize=10)
ax.set_title(f'(d) reading priced: value not always subadditive\n\u03ba > 1 in {sup.sum()} of {len(w2)} worlds; quadrant rule \u2260 best design in {wrong.sum()}', weight='bold')
fig.suptitle('Data collapse: random worlds by their best design, in raw inputs and in the map\u2019s coordinates', fontsize=18, weight='bold')
S3 = V23['v3_all']
fig.text(0.5, 0.012, f'One read stream, two time scales, \u2264 2 local + 2 shared stores ({S3["worlds"]} worlds; \u03c1 per component in half): adding layers one at a time finds the best design in {S3["greedy_same"]:.1%}\n'
         f'(worst regret {S3["greedy_regret_max"]:.1e} of total cost); with a pairwise look-ahead {S3["pair_same"]:.1%}.  Tested scope only: counterexample B stops greedy at NONE, and a 3-scale world defeats the look-ahead.', ha='center', fontsize=11.5)
fig.text(0.5, 0.068, 'Values \u2264 $10^{-6}$ (including 0 and below) are drawn at $10^{-6}$.', ha='center', fontsize=11, color='#444444')
fig.tight_layout(rect=(0, 0.09, 1, 0.96)); fig.savefig(os.path.join(HERE, 'face_collapse.png')); print('saved face_collapse.png')
