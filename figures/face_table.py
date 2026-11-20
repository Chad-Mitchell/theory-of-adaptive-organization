"""Write the placements table into face_placements.md (between the TABLE markers) from face_dots.json and face_systems.py.
nice -n 19 python3 figures/face_table.py"""
import os, json, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SEC, MIN, H, D, W, MO, Y = 1 / 3600, 1 / 60, 1.0, 24.0, 24.0 * 7, 24.0 * 30.4, 24.0 * 365.25
SRC = {('E. coli', 'gradient signal'): 'all inputs measured or proxy: PR #110 `theory/measured/measured.json` (Mattingly et al. 2021, 10.1038/s41567-021-01380-3; Ni et al. 2019, 10.1073/pnas.1910849117); X_L is a proxy (benefit / proteome share)',
       ('immune system', 'adaptive'): 'lead: dendritic-cell trafficking to lymph nodes, Randolph, Angeli & Swartz 2005 (10.1038/nri1670); rest guess',
       ('immune system', 'memory'): 'tau: antibody half-lives 11 to >200 y, Amanna, Carlson & Slifka 2007 (10.1056/NEJMoa066092); rest guess',
       ('immune system', 'innate'): 'lead as adaptive (Randolph et al. 2005); rest guess',
       ('ant colony', 'patch'): 'tau: trail lifetime ~47 min (Lasius niger), Beckers, Deneubourg & Goss 1993 (10.1007/bf01201674); rest guess',
       ('ant colony', 'food supply'): 'rho: foraging regulated by return rate with no spatial information, Prabhakar, Dektar & Gordon 2012 (10.1371/journal.pcbi.1002670); rest guess',
       ('nation-state', 'business cycle'): 'lead: data-release lags, Giannone, Reichlin & Small 2008 (10.1016/j.jmoneco.2008.05.010); rest guess'}

def fmt_t(h):
    for u, s in ((Y, 'y'), (MO, 'mo'), (W, 'wk'), (D, 'd'), (H, 'h'), (MIN, 'min'), (SEC, 's')):
        if h >= u * 0.999: x = h / u; return (f'{x:.3g}' if x < 10 else f'{x:.0f}') + ' ' + s
    return f'{h / SEC:.2g} s'

def rng(p, f=lambda x: f'{x:.3g}'):
    return f(p[0]) if np.isclose(p[0], p[1]) else f'{f(p[0])}–{f(p[1])}'

def table():
    dots = json.load(open(os.path.join(HERE, 'face_dots.json')))
    L = ['| System | Scale | τ | delay ℓ | units n | shared ρ | snr | stakes ÷ upkeep R | h_c ÷ h_l | X_L (centre) | X_S (centre) | map gives | share of draws | sources |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for d in dots:
        i, c = d['inputs'], d['centre']; nm = d['system'] + ('' if d['strong'] else '*')
        xs = '—' if not np.isfinite(c['XS']) else f"{c['XS']:.3g}"
        sh = ', '.join(f'{k} {v:.0%}' for k, v in sorted(d['design_share'].items(), key=lambda kv: -kv[1]) if v >= 0.01)
        R = rng(i['R']) if not d.get('measured') else f"proxy 10^{i['logXL'][0]:.2f}–10^{i['logXL'][1]:.2f}"
        lab = d['lab'] + (' (degree 2)' if d.get('degree', 1) == 2 else '')
        L.append(f"| {nm} | {d['lab']} | {rng(i['tau'], fmt_t)} | {rng(i['lead'], fmt_t)} | {rng(i['n'], lambda x: f'{x:.0f}')} | {rng(i['rho'], lambda x: f'{x:.2g}')} | "
                 f"{rng(i['snr'])} | {R} | {rng(i['hc'])} | {c['XL']:.3g} | {xs} | **{('local' if c['d'] == 1 else ['none', 'local', 'shared', 'both'][c['d']])}** | {sh} | {SRC.get((d['system'], d['lab']), 'guess')} |")
    return '\n'.join(L)

if __name__ == '__main__':
    p = os.path.join(HERE, 'face_placements.md'); s = open(p).read()
    s = re.sub(r'<!-- TABLE -->.*<!-- /TABLE -->', lambda m: '<!-- TABLE -->\n' + table() + '\n<!-- /TABLE -->', s, flags=re.S)
    open(p, 'w').write(s); print('table written')
