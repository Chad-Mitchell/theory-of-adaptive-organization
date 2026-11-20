"""The face figure: where layers belong.   nice -n 19 python3 figures/face.py        (seconds; needs figures/face_dots.json from face_place.py)
Regions are the map theorem (face_map.py, THEORY B.11): exact for any world, noise, delay and number of units.  Dots are hypothesized
placements (inputs face_systems.py, coordinates face_place.py).  Writes figures/face.png (1600x1000), figures/face_square.png (1200x1200)
and figures/face_all.png (every system's chain with 2-sigma ellipses from the input ranges; a detail figure, not for phones)."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import face_map as fm
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.lines import Line2D

DOTS = json.load(open(os.path.join(HERE, 'face_dots.json')))
SYSTEMS = list(dict.fromkeys(d['system'] for d in DOTS))
C_NONE, C_LOC, C_SH, C_BOTH = '#ebebeb', '#fbe2bb', '#cfe5f6', '#d2eee0'
K_LOC, K_SH, K_BOTH, K_NONE = '#c25100', '#0b5fa0', '#00785a', '#7a7a7a'
MK = {0: ('o', K_NONE), 1: ('o', K_LOC), 2: ('s', K_SH), 3: ('D', K_BOTH)}
OUT = [pe.withStroke(linewidth=4, foreground='white')]

def comps(name):
    out = []
    for d in DOTS:
        if d['system'] != name: continue
        c = d['centre']; ly = np.log10(c['XS']) if np.isfinite(c['XS']) and c['XS'] > 0 else -999.0
        out.append((np.log10(c['XL']), ly, d))
    return out

def reading(name, short=False):
    ds = [d['centre']['d'] for _, _, d in comps(name)]; n1 = all(not np.isfinite(d['centre']['XS']) for _, _, d in comps(name))
    dg = [d.get('degree', 1) for _, _, d in comps(name)]
    kl = sum(g for x, g in zip(ds, dg) if x in (1, 3)); ks = sum(g for x, g in zip(ds, dg) if x in (2, 3))
    nb = sum(max(d['design_share'].values()) < 0.65 for _, _, d in comps(name))
    tail = '' if not nb else (f' ({nb} near edge)' if short else (' (1 borderline)' if nb == 1 else f' ({nb} borderline)'))
    if n1: return (f'{kl} layer' + ('s' if kl != 1 else '')) + (' (by degree; measured proxy)' if name == 'E. coli' else '') + tail
    parts = []
    if kl: parts.append(f'{kl} local' if short else f'{kl} in each unit')
    if ks: parts.append(f'{ks} shared')
    return (' + '.join(parts) if parts else 'no layer') + tail

def tick_lab(t):
    return {0: '1', 1: '10'}.get(t, f'$10^{{{t}}}$')

def draw_map(ax, st, lim, fs, show, lab, ell_sigma=1.0, ell_alpha=0.10, strip_rows=None):
    X0, X1, Y0, Y1 = lim
    ax.set_xlim(X0, X1); st.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); st.set_ylim(0, 1)
    for a, (y0, y1) in ((ax, (Y0, Y1)), (st, (0, 1))):
        a.add_patch(Rectangle((X0, y0), -X0, (0 if a is ax else 1) - y0, color=C_NONE, zorder=0))
        a.add_patch(Rectangle((0, y0), X1, (0 if a is ax else 1) - y0, color=C_LOC, zorder=0))
        a.axvline(0, color='#1a1a1a', lw=2.6, zorder=1)
    ax.add_patch(Rectangle((X0, 0), -X0, Y1, color=C_SH, zorder=0)); ax.add_patch(Rectangle((0, 0), X1, Y1, color=C_BOTH, zorder=0))
    ax.axhline(0, color='#1a1a1a', lw=2.6, zorder=1)
    kw = dict(fontsize=fs * 1.3, weight='bold', zorder=2, path_effects=OUT)
    ax.text(X0 + 0.1, Y0 + 0.12, 'NO LAYER', color='#555555', ha='left', va='bottom', **kw)
    ax.text(0.08, Y0 + 0.12, 'A LAYER IN\nEACH UNIT', color=K_LOC, ha='left', va='bottom', **kw)
    ax.text(X0 + 0.1, 0.1, 'ONE SHARED\nLAYER', color=K_SH, ha='left', va='bottom', **kw)
    ax.text(X1 - 0.08, 0.1, 'BOTH PAY', color=K_BOTH, ha='right', va='bottom', **kw)
    st.text(X0 + 0.06, 0.78, 'shared layer worth ≈ 0', color='#555555', ha='left', va='center', fontsize=fs * 0.74, zorder=2, path_effects=OUT)
    for k, name in enumerate(show):
        pts = comps(name); strong = pts[0][2]['strong']; ls = '-' if strong else (0, (3, 2))
        row = (strip_rows or {}).get(name, 0.5)
        P = [(x, y if y >= Y0 else None) for x, y, _ in pts]
        for (x1, y1), (x2, y2) in zip(P[:-1], P[1:]):
            if y1 is not None and y2 is not None: ax.plot([x1, x2], [y1, y2], color='#2a2a2a', lw=1.7, ls=ls, zorder=3)
            elif y1 is None and y2 is not None:
                ax.plot([x1, x2], [Y0, y2], color='#2a2a2a', lw=1.7, ls=ls, zorder=3)
                st.plot([x1, x1], [row, 1], color='#2a2a2a', lw=1.7, ls=ls, zorder=3)
            elif y1 is None and y2 is None: st.plot([x1, x2], [row, row], color='#2a2a2a', lw=1.7, ls=ls, zorder=3)
        for (x, y, d), (_, yy) in zip(pts, P):
            m, col = MK[d['centre']['d']]; a, yv = (ax, y) if yy is not None else (st, row)
            if ell_sigma and a is ax and 'cov' in d:
                C = np.array(d['cov']); w, V = np.linalg.eigh(C); ang = np.degrees(np.arctan2(V[1, 1], V[0, 1]))
                a.add_patch(Ellipse((x, y), 2 * ell_sigma * np.sqrt(w[1]), 2 * ell_sigma * np.sqrt(max(w[0], 1e-8)), angle=ang, facecolor=col, edgecolor='none', alpha=ell_alpha, zorder=2.2))
            if d.get('measured') and a is st:
                q = d['inputs']['logXL']; a.plot(q, [yv, yv], color=col, lw=3, alpha=0.55, zorder=3.5, solid_capstyle='butt')
                a.plot(q, [yv, yv], ls='none', marker='|', ms=fs * 0.9, mew=2.4, color=col, zorder=3.5)
            a.plot([x], [yv], marker=m, ms=fs * 0.85, mfc=col if strong else 'white', mec=col, mew=2.4, zorder=4, clip_on=False)
            if (name, d['lab']) in lab:
                dx, dy = lab[(name, d['lab'])]
                a.annotate(d['lab'], (x, yv), xytext=(dx, dy), textcoords='offset points', fontsize=fs * 0.74, color='#222222', zorder=5, path_effects=OUT,
                           ha='center' if dx == 0 else ('left' if dx > 0 else 'right'), va='center',
                           arrowprops=dict(arrowstyle='-', lw=0.8, color='#555555', shrinkA=0, shrinkB=4) if abs(dx) + abs(dy) > 25 else None)
        if (name, None) in lab:
            i, dx, dy = lab[(name, None)]; x, y, d = pts[i]; yy = P[i][1]; a, yv = (ax, y) if yy is not None else (st, row)
            a.annotate(name + ('' if strong else '*'), (x, yv), xytext=(dx, dy), textcoords='offset points', fontsize=fs * 0.98, weight='bold', color='#111111',
                       zorder=6, path_effects=OUT, ha='center' if dx == 0 else ('left' if dx > 0 else 'right'), va='center',
                       arrowprops=dict(arrowstyle='-', lw=1.0, color='#333333', shrinkA=0, shrinkB=5) if abs(dx) + abs(dy) > 30 else None)
    tk = range(int(np.ceil(X0)), int(np.floor(X1)) + 1)
    st.set_xticks(list(tk)); st.set_xticklabels([tick_lab(t) for t in tk], fontsize=fs * 0.88); ax.set_xticks(list(tk)); ax.set_xticklabels([])
    ty = range(int(np.ceil(Y0)), int(np.floor(Y1)) + 1)
    ax.set_yticks(list(ty)); ax.set_yticklabels([tick_lab(t) for t in ty], fontsize=fs * 0.88)
    st.set_yticks([0.5]); st.set_yticklabels(['≈0'], fontsize=fs * 0.88)
    for a in (ax, st): a.tick_params(length=5, width=1.4)
    st.set_xlabel('A layer in each unit:  stakes it can win, net of reading cost, ÷ its upkeep', fontsize=fs * 1.0, labelpad=3)
    ax.set_ylabel('One shared layer:  net stakes ÷ upkeep', fontsize=fs * 1.0, labelpad=5)

def side_panel(fig, x, y_top, dy, fs, names):
    fig.text(x, y_top, 'What the map gives each system', fontsize=fs * 1.0, weight='bold', va='center')
    fig.text(x, y_top - 0.033, 'its time scales, fast \u2192 slow:', fontsize=fs * 0.78, color='#444444', va='center')
    legend_row(fig, x + 0.006, y_top - 0.068, fs, 0.105)
    fig.text(x, y_top - 0.1, 'both: when each still pays on what the other\ndoes not know; else the one that nets more', fontsize=fs * 0.66, color=K_BOTH, va='center', linespacing=1.1)
    for i, name in enumerate(names):
        yy = y_top - 0.17 - i * dy; pts = comps(name); strong = pts[0][2]['strong']
        fig.text(x, yy, name + ('' if strong else '*'), fontsize=fs * 0.88, weight='bold', va='center')
        for j, (_, _, d) in enumerate(pts):
            m, col = MK[d['centre']['d']]
            fig.lines.append(Line2D([x + 0.006 + j * 0.019], [yy - 0.029], marker=m, ms=fs * 0.58, mfc=col if strong else 'white', mec=col, mew=2, transform=fig.transFigure))
        fig.text(x + 0.008 + len(pts) * 0.019, yy - 0.029, reading(name), fontsize=fs * 0.76, va='center', color='#222222')

def legend_row(fig, x, y, fs, gap):
    items = [('o', K_LOC, 'in each unit'), ('s', K_SH, 'shared'), ('D', K_BOTH, 'both')]
    for i, (m, c, t) in enumerate(items):
        fig.lines.append(Line2D([x + i * gap], [y], marker=m, ms=fs * 0.6, mfc=c, mec=c, transform=fig.transFigure))
        fig.text(x + i * gap + 0.012, y, t, fontsize=fs * 0.78, va='center')

LIM = (-1.3, 3.0, -3.0, 3.2)
SHOW = ['E. coli', 'immune system', 'ant colony', 'firm', 'nation-state']
LAB = {('E. coli', None): (0, 0, 15),
       ('immune system', 'innate'): (10, 0), ('immune system', 'adaptive'): (11, 0), ('immune system', 'memory'): (-11, 0), ('immune system', None): (1, 70, 14),
       ('ant colony', 'patch'): (-9, 13), ('ant colony', 'food supply'): (0, 15), ('ant colony', None): (1, 0, 34),
       ('firm', 'operations'): (11, -3), ('firm', 'management'): (12, 0), ('firm', 'strategy'): (-4, -18), ('firm', None): (0, 12, 18),
       ('nation-state', 'local'): (10, 0), ('nation-state', 'business cycle'): (12, -3), ('nation-state', 'institutions'): (-9, -15), ('nation-state', None): (1, 110, -28)}
ROWS = {'E. coli': 0.3, 'nation-state': 0.7, 'immune system': 0.7}

T = 'Where the cost of judgment puts layers'
RED = 'Hypothesized positions, not measurements'
SUB = 'For each time scale of its world, the cost picks no layer, a layer in each unit, one shared layer, or both.'
SUB2 = 'Layer = tracking store, not org-chart level.  Edges hold for any world.  Inputs are guesses (E. coli: measured proxy).'
F1 = 'A shared layer\u2019s worth = upkeep shared \u00d7 pooling gain \u00d7 e^(\u22122 \u00d7 delay \u00f7 time scale) \u00d7 a local layer\u2019s worth, so fast scales go local and slow ones shared.'
F2 = 'Survival is a separate gate.   * hollow, dashed: selection weak or unknown.   Shading: input ranges; bar: measured range.   figures/face_placements.md  \u00b7  CC0'

def face():
    fig = plt.figure(figsize=(16, 10), dpi=100); fs = 19
    st = fig.add_axes([0.075, 0.125, 0.56, 0.07]); ax = fig.add_axes([0.075, 0.201, 0.56, 0.59])
    draw_map(ax, st, LIM, fs, SHOW, LAB, strip_rows=ROWS)
    fig.text(0.5, 0.958, T, ha='center', va='center', fontsize=40, weight='bold')
    fig.text(0.5, 0.908, RED, ha='center', va='center', fontsize=25, weight='bold', color='#cc0000')
    fig.text(0.5, 0.866, SUB, ha='center', va='center', fontsize=17, color='#222222')
    fig.text(0.5, 0.834, SUB2, ha='center', va='center', fontsize=17, color='#222222')
    side_panel(fig, 0.668, 0.77, 0.068, 19, SYSTEMS)
    fig.text(0.5, 0.045, F1, ha='center', va='center', fontsize=13.5, color='#222222')
    fig.text(0.5, 0.016, F2, ha='center', va='center', fontsize=12, color='#444444')
    fig.savefig(os.path.join(HERE, 'face.png'), dpi=100); plt.close(fig)

def square():
    fig = plt.figure(figsize=(12, 12), dpi=100); fs = 17
    st = fig.add_axes([0.1, 0.315, 0.87, 0.055]); ax = fig.add_axes([0.1, 0.375, 0.87, 0.47])
    draw_map(ax, st, LIM, fs, SHOW, LAB, strip_rows=ROWS)
    fig.text(0.5, 0.967, T, ha='center', va='center', fontsize=38, weight='bold')
    fig.text(0.5, 0.927, RED, ha='center', va='center', fontsize=23, weight='bold', color='#cc0000')
    fig.text(0.5, 0.884, 'For each time scale of its world, the cost picks no layer, a layer in each unit, one shared layer,\nor both.  Layer = tracking store, not org-chart level.  Edges exact; inputs guessed (E. coli: proxy).',
             ha='center', va='center', fontsize=15, color='#222222', linespacing=1.25)
    legend_row(fig, 0.07, 0.222, 17, 0.17)
    fig.text(0.56, 0.222, 'both: if each still pays on what the other does not know', fontsize=12.5, color=K_BOTH, va='center')
    for k, name in enumerate(SYSTEMS):
        col, row = divmod(k, 4); x = 0.04 + col * 0.495; off = 0.183 if col == 0 else 0.166; yy = 0.18 - row * 0.034; pts = comps(name); strong = pts[0][2]['strong']
        fig.text(x, yy, name + ('' if strong else '*'), fontsize=14.5, weight='bold', va='center')
        for j, (_, _, d) in enumerate(pts):
            m, c = MK[d['centre']['d']]
            fig.lines.append(Line2D([x + off + j * 0.022], [yy], marker=m, ms=10, mfc=c if strong else 'white', mec=c, mew=2, transform=fig.transFigure))
        fig.text(x + off + 0.003 + len(pts) * 0.022, yy, reading(name, short=True), fontsize=11.8, va='center')
    fig.text(0.5, 0.034, 'Fast scales go local, slow ones shared: a shared layer\u2019s worth falls as e^(\u22122 \u00d7 delay \u00f7 time scale).', ha='center', fontsize=13, color='#222222')
    fig.text(0.5, 0.01, 'Survival is a separate gate.  * hollow, dashed: selection weak or unknown.  Shading: input ranges.  figures/face_placements.md \u00b7 CC0', ha='center', fontsize=11, color='#444444')
    fig.savefig(os.path.join(HERE, 'face_square.png'), dpi=100); plt.close(fig)

def all_systems():
    fig, axs = plt.subplots(2, 4, figsize=(24, 13), dpi=80); fs = 15
    for k, name in enumerate(SYSTEMS):
        ax = axs.flat[k]; pos = ax.get_position(); ax.set_position([pos.x0, pos.y0 + 0.06, pos.width, pos.height - 0.06])
        st = fig.add_axes([pos.x0, pos.y0, pos.width, 0.05])
        lab = {(name, d['lab']): (8, 8) for _, _, d in comps(name)}
        draw_map(ax, st, (-1.5, 3.5, -3.0, 3.5), fs * 0.8, [name], lab, ell_sigma=2.0, ell_alpha=0.12)
        ax.set_title(name + ': ' + reading(name), fontsize=fs, weight='bold')
    fig.suptitle('Every placement with 2\u03c3 ellipses from its input ranges (hypothesized positions, not measurements)', fontsize=22, weight='bold', color='#cc0000')
    fig.savefig(os.path.join(HERE, 'face_all.png'), dpi=80); plt.close(fig)

if __name__ == '__main__':
    face(); square(); all_systems(); print('saved face.png, face_square.png, face_all.png')
