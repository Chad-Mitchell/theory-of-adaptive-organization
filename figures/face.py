"""The face figure: where the cost of judgment puts layers.   nice -n 19 python3 figures/face.py   (seconds; needs figures/face_dots.json)
What is drawn (v2.5.1, after review 26):
  SHADING = which single layer would pay ON ITS OWN (X_L > 1: a layer in each unit; X_S > 1: one shared layer).  Exact by definition, any model.
  SHAPE   = the cheapest design for that dot, from all four costs (face_map.decide, with the dot's own nu and kappa: exact in its model).
  The two agree outside the top-right quadrant exactly when the layers' value is subadditive (THEORY B.11).  A ringed dot would mark joint
  value (a shared layer paying as a common-mode reference); none of the placements has it in its model.
Dots are hypothesized placements (inputs face_systems.py, coordinates face_place.py); E. coli (one cell, no shared option, a plausibility
proxy) is drawn apart from the map.  Writes face.png (1600x1000), face_square.png (1200x1200), face_all.png (every system, 2-sigma ellipses)."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.lines import Line2D

DOTS = json.load(open(os.path.join(HERE, 'face_dots.json')))
SYSTEMS = list(dict.fromkeys(d['system'] for d in DOTS))
MAPPED = [s for s in SYSTEMS if s != 'E. coli']
NUM = {s: i + 1 for i, s in enumerate(MAPPED)}
C_NONE, C_LOC, C_SH, C_EACH = '#ececec', '#fbe3c2', '#d4e7f6', '#f3f1e4'
K_LOC, K_SH, K_BOTH, K_NONE = '#c25100', '#0b5fa0', '#00785a', '#6e6e6e'
MK = {0: ('o', K_NONE), 1: ('o', K_LOC), 2: ('s', K_SH), 3: ('D', K_BOTH)}
OUT = [pe.withStroke(linewidth=3.5, foreground='white')]
NEAR = 0.65
LIM = (-1.3, 3.0, -3.0, 3.0)

def comps(name):
    return [d for d in DOTS if d['system'] == name]

def code(d):
    i = [x['lab'] for x in comps(d['system'])].index(d['lab'])
    return f"{NUM[d['system']]}{'abc'[i]}"

def near(d): return max(d['design_share'].values()) < NEAR

def reading(name, short=False):
    ds = comps(name); dg = [d.get('degree', 1) for d in ds]; dd = [d['centre']['d'] for d in ds]
    kl = sum(g for x, g in zip(dd, dg) if x in (1, 3)); ks = sum(g for x, g in zip(dd, dg) if x in (2, 3))
    if name == 'E. coli': return f'{kl} stores (degree 2), local'
    parts = ([f'{kl} local' if short else f'{kl} in each unit'] if kl else []) + ([f'{ks} shared'] if ks else [])
    nb = sum(near(d) for d in ds)
    return (' + '.join(parts) + ' layers' if parts else 'no layer') + (f'  ({nb} hollow)' if nb else '')

def tick_lab(t): return {0: '1', 1: '10'}.get(t, f'$10^{{{t}}}$')

def place_labels(ax, pts, fs, fixed):
    """Deterministic labels: each label takes the nearest free spot (rings of 16 directions at growing radius) that overlaps no placed label,
    no dot and stays inside the axes; the most crowded dots choose first.  Far labels get a leader line."""
    fig = ax.figure; fig.canvas.draw(); T = ax.transData; k = 72.0 / fig.dpi; fs = fs / k
    bb = ax.get_window_extent(); P = np.array([T.transform(p[:2]) for p in pts]); n = len(pts)
    W = np.array([len(p[2]) * fs * 0.62 + 6 for p in pts]); H = fs * 1.25; rdot = fs * 0.75
    D = np.hypot(*(P[:, None, :] - P[None, :, :]).transpose(2, 0, 1)) + np.eye(n) * 1e9
    order = np.argsort(np.sort(D, 1)[:, :3].sum(1)); boxes = []; off = np.zeros((n, 2))
    dirs = [np.deg2rad(t) for t in (45, 0, 90, 135, 315, 180, 270, 225, 22, 68, 112, 158, 202, 248, 292, 338)]
    R = fig.canvas.get_renderer(); obst = [t.get_window_extent(R) for t in ax.texts]
    def free(cx, cy, w):
        for o in obst:
            if cx + w / 2 > o.x0 - 3 and cx - w / 2 < o.x1 + 3 and cy + H / 2 > o.y0 - 3 and cy - H / 2 < o.y1 + 3: return False
        if cx - w / 2 < bb.x0 + 4 or cx + w / 2 > bb.x1 - 4 or cy - H / 2 < bb.y0 + 4 or cy + H / 2 > bb.y1 - 4: return False
        for (bx, by, bw) in boxes:
            if abs(cx - bx) < (w + bw) / 2 + 2 and abs(cy - by) < H + 2: return False
        for q in P:
            if abs(cx - q[0]) < w / 2 + rdot and abs(cy - q[1]) < H / 2 + rdot: return False
        return True
    for i in order:
        if pts[i][3] in fixed:
            o = np.array(fixed[pts[i][3]]) * fs; off[i] = o; boxes.append((P[i][0] + o[0], P[i][1] + o[1], W[i])); continue
        done = False
        r0 = 2.3 if np.sort(D[i])[0] < fs * 3.0 else 1.25
        for r in np.arange(r0, 12.0, 0.45) * fs:
            for t in dirs:
                cx, cy = P[i][0] + (r + W[i] / 2 * abs(np.cos(t)) * 0.6) * np.cos(t), P[i][1] + r * np.sin(t)
                if free(cx, cy, W[i]): off[i] = (cx - P[i][0], cy - P[i][1]); boxes.append((cx, cy, W[i])); done = True; break
            if done: break
        if not done: off[i] = (fs, fs)
    return off * k

def draw_map(ax, st, fs, show, with_labels=True, ell_sigma=0.0, names=False, fixed=None):
    X0, X1, Y0, Y1 = LIM
    ax.set_xlim(X0, X1); st.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); st.set_ylim(0, 1)
    ax.add_patch(Rectangle((X0, Y0), -X0, -Y0, color=C_NONE, zorder=0)); ax.add_patch(Rectangle((0, Y0), X1, -Y0, color=C_LOC, zorder=0))
    ax.add_patch(Rectangle((X0, 0), -X0, Y1, color=C_SH, zorder=0)); ax.add_patch(Rectangle((0, 0), X1, Y1, color=C_EACH, zorder=0))
    st.add_patch(Rectangle((X0, 0), -X0, 1, color=C_NONE, zorder=0)); st.add_patch(Rectangle((0, 0), X1, 1, color=C_LOC, zorder=0))
    for a in (ax, st): a.axvline(0, color='#1a1a1a', lw=2.4, zorder=1)
    ax.axhline(0, color='#1a1a1a', lw=2.4, zorder=1)
    kw = dict(fontsize=fs * 1.05, weight='bold', zorder=2, path_effects=OUT)
    ax.text(X0 + 0.08, Y0 + 0.1, 'NEITHER PAYS\nON ITS OWN', color='#555555', ha='left', va='bottom', **kw)
    ax.text(0.08, -0.25, 'ONLY A LAYER IN EACH\nUNIT PAYS ON ITS OWN', color=K_LOC, ha='left', va='top', **kw)
    ax.text(X0 + 0.08, 0.12, 'ONLY ONE SHARED\nLAYER PAYS\nON ITS OWN', color=K_SH, ha='left', va='bottom', **kw)
    ax.text(X1 - 0.08, 0.12, 'EACH PAYS ON ITS OWN:\nthe shape shows the pick', color='#4a4a3a', ha='right', va='bottom', **kw)
    st.text(X0 + 0.06, 0.5, 'shared layer:\nstakes / upkeep < $10^{-3}$', color='#555555', ha='left', va='center', fontsize=fs * 0.62, zorder=2, linespacing=1.0)
    pts = []; seen = {}
    for name in show:
        for d in comps(name):
            c = d['centre']; x = np.log10(c['XL']); y = np.log10(c['XS']) if c['XS'] > 0 else -99
            inmap = y >= Y0; a = ax if inmap else st
            if not inmap: y = 0.45
            m, col = MK[c['d']]; hollow = near(d)
            if ell_sigma and inmap and 'cov' in d:
                C = np.array(d['cov']); w_, V = np.linalg.eigh(C); ang = np.degrees(np.arctan2(V[1, 1], V[0, 1]))
                ax.add_patch(Ellipse((x, y), 2 * ell_sigma * np.sqrt(w_[1]), 2 * ell_sigma * np.sqrt(max(w_[0], 1e-8)), angle=ang, facecolor=col, edgecolor='none', alpha=0.12, zorder=2.2))
            a.plot([x], [y], marker=m, ms=fs * 0.85, mfc='white' if hollow else col, mec=col, mew=2.4, zorder=4, clip_on=False)
            if c.get('joint'): a.plot([x], [y], marker='o', ms=fs * 1.5, mfc='none', mec='#111111', mew=1.6, zorder=4)
            key = (round(x, 2), round(y, 2) if inmap else 'strip'); t = d['lab'] if names else code(d)
            if key in seen: seen[key][2] += (', ' if names else ' ') + t; continue
            seen[key] = [x, y, t, code(d), inmap]
    for x, y, t, cd, inmap in seen.values():
        if inmap: pts.append((x, y, t, cd))
        elif with_labels: st.annotate(t, (x, y), xytext=(0, fs * 0.55), textcoords='offset points', ha='center', va='bottom',
                                      fontsize=fs * 0.68, weight='bold', zorder=5, path_effects=OUT)
    if with_labels and pts:
        off = place_labels(ax, pts, fs * 0.72, fixed or {})
        for (x, y, t, _), o in zip(pts, off):
            far = np.hypot(*o) > fs * 1.3
            ax.annotate(t, (x, y), xytext=tuple(o), textcoords='offset points', ha='center', va='center', fontsize=fs * 0.72, weight='bold', zorder=5,
                        path_effects=OUT, arrowprops=dict(arrowstyle='-', lw=0.9, color='#444444', shrinkA=0, shrinkB=4) if far else None)
    tk = range(int(np.ceil(X0)), int(np.floor(X1)) + 1)
    st.set_xticks(list(tk)); st.set_xticklabels([tick_lab(t) for t in tk], fontsize=fs * 0.82); ax.set_xticks(list(tk)); ax.set_xticklabels([])
    ty = range(int(np.ceil(Y0)), int(np.floor(Y1)) + 1)
    ax.set_yticks(list(ty)); ax.set_yticklabels([tick_lab(t) for t in ty], fontsize=fs * 0.82); st.set_yticks([])
    for a in (ax, st): a.tick_params(length=5, width=1.3)
    st.set_xlabel('A layer in each unit:  stakes it can win / its upkeep  (at the stated read quality)', fontsize=fs * 0.9, labelpad=3)
    ax.set_ylabel('One shared layer:  stakes it can win / its upkeep', fontsize=fs * 0.9, labelpad=4)

def legend_rows(fig, x, y, fs, dy):
    items = [('o', K_LOC, False, 'cheapest: a layer in each unit'), ('s', K_SH, False, 'cheapest: one shared layer'),
             ('D', K_BOTH, False, 'cheapest: both'), ('o', '#777777', True, 'hollow: no design wins \u2265 65% of its input draws')]
    for i, (m, c, hol, t) in enumerate(items):
        fig.lines.append(Line2D([x + 0.007], [y - i * dy], marker=m, ms=fs * 0.62, mfc='white' if hol else c, mec=c, mew=2, transform=fig.transFigure))
        fig.text(x + 0.02, y - i * dy, t, fontsize=fs * 0.74, va='center')

def key_rows(fig, x, y, fs, dy, names):
    for i, name in enumerate(names):
        ds = comps(name); yy = y - i * dy; star = '' if ds[0]['strong'] else '*'
        fig.text(x, yy, f'{NUM[name]}  {name}{star}', fontsize=fs * 0.8, weight='bold', va='center')
        fig.text(x + 0.012, yy - dy * 0.45, '  '.join(f"{'abc'[j]} {d['lab']}" for j, d in enumerate(ds)) + '   \u2192 ' + reading(name, short=True).split('  (')[0],
                 fontsize=fs * 0.56, va='center', color='#222222')

def ecoli_axis(fig, rect, fs):
    d = comps('E. coli')[0]; ax = fig.add_axes(rect); q = d['inputs']['logXL']; c = np.log10(d['centre']['XL'])
    ax.set_xlim(-1.3, 3.0); ax.set_ylim(0, 1); ax.set_facecolor('white')
    ax.plot(q, [0.45, 0.45], color=K_LOC, lw=3, alpha=0.6); ax.plot(q, [0.45, 0.45], ls='none', marker='|', ms=fs * 0.8, mew=2.2, color=K_LOC)
    ax.plot([c], [0.45], marker='o', ms=fs * 0.7, mfc='white', mec=K_LOC, mew=2.2)
    ax.set_yticks([]); tk = range(-1, 4); ax.set_xticks(list(tk)); ax.set_xticklabels([tick_lab(t) for t in tk], fontsize=fs * 0.62)
    ax.set_title('E. coli: one cell, no shared option (off the map)\nproxy: motility benefit / signalling proteome share\n(not X_L; the map\u2019s edges do not apply)', fontsize=fs * 0.64, loc='left')
    return ax

T = 'Where the cost of judgment puts layers'
RED = 'Hypothesized positions, not measurements'
SUB = 'Each dot: one time scale of a system, at the centre of its input ranges.  Shading: which layer would pay on its own.  Shape: the cheapest design.'
SUB2 = 'Outside the top-right, shading = cheapest design when two layers are worth no more together than apart (B.11).  Layer = tracking store.'
F1 = r'Shared layer' + '\u2019' + r's stakes / upkeep = ν × pooling gain × $e^{-2\,\mathrm{delay}/\mathrm{time\ scale}}$ × local layer' + '\u2019' + r's stakes / upkeep   (OU model, same read quality;'
F1b = '\u03bd = all local layers\u2019 upkeep / the shared layer\u2019s upkeep).  So, other things equal, fast scales go local and slow ones shared.'
F2 = ('If two layers are worth more together than apart (e.g. a shared layer as a reference for the local ones\u2019 common noise), both can win outside the top-right;'
      ' no dot here has that in its model.')
F3 = 'Survival is a separate gate.   * selection weak or unknown.   Inputs, sources, ellipses: figures/face_placements.md, face_all.png  \u00b7  CC0'
FIX_MAIN = {}

def face():
    fig = plt.figure(figsize=(16, 10), dpi=100); fs = 19
    st = fig.add_axes([0.07, 0.17, 0.56, 0.05]); ax = fig.add_axes([0.07, 0.227, 0.56, 0.585])
    draw_map(ax, st, fs, MAPPED, fixed=FIX_MAIN)
    fig.text(0.5, 0.962, T, ha='center', va='center', fontsize=38, weight='bold')
    fig.text(0.5, 0.915, RED, ha='center', va='center', fontsize=24, weight='bold', color='#cc0000')
    fig.text(0.5, 0.875, SUB, ha='center', va='center', fontsize=15.5, color='#222222')
    fig.text(0.5, 0.846, SUB2, ha='center', va='center', fontsize=15.5, color='#222222')
    legend_rows(fig, 0.655, 0.79, 19, 0.03)
    key_rows(fig, 0.655, 0.66, 19, 0.058, MAPPED)
    ecoli_axis(fig, [0.672, 0.17, 0.30, 0.028], 19)
    fig.text(0.5, 0.080, F1, ha='center', va='center', fontsize=11.2, color='#222222')
    fig.text(0.5, 0.059, F1b, ha='center', va='center', fontsize=11.2, color='#222222')
    fig.text(0.5, 0.036, F2, ha='center', va='center', fontsize=11.2, color='#222222')
    fig.text(0.5, 0.013, F3, ha='center', va='center', fontsize=11, color='#444444')
    fig.savefig(os.path.join(HERE, 'face.png'), dpi=100); plt.close(fig)

def square():
    fig = plt.figure(figsize=(12, 12), dpi=100); fs = 17
    st = fig.add_axes([0.09, 0.39, 0.88, 0.045]); ax = fig.add_axes([0.09, 0.44, 0.88, 0.415])
    draw_map(ax, st, fs, MAPPED, fixed=FIX_MAIN)
    fig.text(0.5, 0.969, T, ha='center', va='center', fontsize=34, weight='bold')
    fig.text(0.5, 0.932, RED, ha='center', va='center', fontsize=22, weight='bold', color='#cc0000')
    fig.text(0.5, 0.888, 'Each dot: one time scale of a system, at the centre of its input ranges.  Shading: which layer would pay on its own.\nShape: the cheapest design.  '
             'Outside the top-right, shading = cheapest design if together \u2264 apart (B.11).', ha='center', va='center', fontsize=13.5, color='#222222', linespacing=1.3)
    legend_rows(fig, 0.05, 0.31, 15, 0.024)
    ecoli_axis(fig, [0.55, 0.255, 0.42, 0.022], 16)
    key_rows(fig, 0.05, 0.205, 17, 0.042, MAPPED[:4]); key_rows(fig, 0.55, 0.205, 17, 0.042, MAPPED[4:])
    fig.text(0.5, 0.03, 'OU model, other things equal: fast scales go local, slow ones shared.  If two layers are worth more together than apart, both can win outside the top-right.',
             ha='center', fontsize=11.5, color='#222222')
    fig.text(0.5, 0.01, 'Layer = tracking store, not org-chart level.  Survival is a separate gate.  * selection weak or unknown.  figures/face_placements.md \u00b7 CC0', ha='center', fontsize=10.5, color='#444444')
    fig.savefig(os.path.join(HERE, 'face_square.png'), dpi=100); plt.close(fig)

def all_systems():
    fig = plt.figure(figsize=(20, 12), dpi=120); fs = 13
    for k, name in enumerate(MAPPED):
        r, c = divmod(k, 4); x0 = 0.05 + c * 0.245; y0 = 0.53 - r * 0.47
        st = fig.add_axes([x0, y0, 0.2, 0.035]); ax = fig.add_axes([x0, y0 + 0.04, 0.2, 0.3])
        draw_map(ax, st, fs, [name], ell_sigma=2.0, names=True)
        for t in ax.texts: t.set_fontsize(10) if t.get_text().isupper() or '\n' in t.get_text() else None
        st.set_xlabel('local layer: stakes / upkeep', fontsize=11); ax.set_ylabel('shared layer: stakes / upkeep' if c == 0 else '', fontsize=11)
        ax.set_title(f"{NUM[name]}  {name}{'' if comps(name)[0]['strong'] else '*'}\n{reading(name, short=True)}", fontsize=14, weight='bold')
    ax = fig.add_axes([0.785, 0.07, 0.19, 0.03]); fig.delaxes(ax)
    ecoli_axis(fig, [0.785, 0.12, 0.19, 0.025], 14)
    legend_rows(fig, 0.785, 0.40, 15, 0.03)
    fig.text(0.785, 0.25, 'Shading: which layer would pay on its own.\nShape: cheapest design (centre of ranges).\nOutside the top-right, shading = cheapest\ndesign if together \u2264 apart (B.11).', fontsize=11, va='center', linespacing=1.3)
    fig.suptitle('Every placement with 2\u03c3 ellipses from its input ranges (hypothesized positions, not measurements)', fontsize=20, weight='bold', color='#cc0000', y=0.985)
    fig.savefig(os.path.join(HERE, 'face_all.png'), dpi=120); plt.close(fig)

if __name__ == '__main__':
    face(); square(); all_systems(); print('saved face.png, face_square.png, face_all.png')
