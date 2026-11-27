"""figures/master_curve.png: the cost of judgment on one curve (worked class), 16:9 for X.
Run: nice -n 19 python3 figures/master_curve.py   Checks: figures/master_curve_checks.py"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import master_curve_math as M  # noqa: E402
from master_curve_params import P  # noqa: E402

OUT = __file__.rsplit("/", 1)[0] + "/master_curve.png"
NAVY, BLUE, ORANGE, GREY, GREEN, PURPLE = "#14213d", "#1f5fa8", "#d1495b", "#8d99ae", "#2a7f4f", "#6a3d9a"

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig = plt.figure(figsize=(13.333, 7.5), dpi=180)
fig.patch.set_facecolor("white")
TEAL = "#0b7285"

def chip(x, y, text, color, size=9.5):
    fig.text(x, y, text, fontsize=size, fontweight="bold", color="white", va="center", ha="left",
             bbox=dict(boxstyle="round,pad=0.25", fc=color, ec=color))

# ---------------- title and cost band ----------------
fig.text(0.03, 0.952, "One cost of judgment: when to remember, and where", fontsize=25, fontweight="bold", color=NAVY, va="center")
fig.text(0.03, 0.905, P["hypothesis"], fontsize=13.5, color=NAVY, va="center", style="italic")

axc = fig.add_axes([0.03, 0.79, 0.94, 0.085]); axc.axis("off")
axc.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.15", transform=axc.transAxes,
                             facecolor="#f1f3f5", edgecolor="#adb5bd", lw=1))
axc.text(0.012, 0.5, "THE COST", fontsize=12, fontweight="bold", color=NAVY, va="center", transform=axc.transAxes)
axc.text(0.098, 0.5, "J = heat + w\u00b7E[loss],  cap: P(ruin) \u2264 \u03b5", fontsize=12.4, color=NAVY, va="center",
         transform=axc.transAxes, fontweight="bold")
axc.text(0.43, 0.5,
         "Heat \u2265 kT \u00d7 the rate the memory learns its world: KNOWN for bipartite jump processes, PROVED (in-model) for additive-noise diffusions.\n"
         "R1 (axioms A1\u2013A7, \u22653 essential coordinates) proves only that a continuous representing cost is an additive price sum.\n"
         "In a world it does not steer, memory pays only by cutting decision loss or keeping the system inside the ruin cap. w and the cap are assumed.",
         fontsize=7.5, color=NAVY, va="center", transform=axc.transAxes, linespacing=1.35)

# ---------------- TIME panel: the curve ----------------
ax = fig.add_axes([0.075, 0.205, 0.43, 0.50])
fig.text(0.03, 0.752, "TIME \u2022 one curve for every time scale", fontsize=13.5, fontweight="bold", color=BLUE, va="center")
chip(0.338, 0.752, "WORKED-CLASS-ONLY \u2022 IP11\u2013IP13", BLUE)
xs = np.logspace(-2, 4, 1200)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(1e-2, 1e4); ax.set_ylim(1e-2, 1e4)
ax.fill_between(xs, 1e-3, M.F(xs), color="#e9ecef", zorder=0, lw=0)
ax.text(250, 0.05, "below the curve:\nunreachable\n(second law, this class)", fontsize=10.5, color="#6c757d", ha="center", va="center")
xa = np.logspace(0, 4, 200)
ax.plot(xa, xa, ls=(0, (4, 3)), color=GREY, lw=1.8, zorder=2)
ax.text(1.6e3, 5.5e2, "remember nothing", fontsize=10, color="#5c677d", ha="center", va="center", rotation=33)
K = P["K"]
ax.plot(xs[xs >= 1], M.separate_copies(xs[xs >= 1], K), color=ORANGE, lw=2.4, ls=(0, (1.5, 1.5)), zorder=3)
ax.plot(xs, M.F(xs), color=BLUE, lw=5, zorder=4, solid_capstyle="round")
kT, a, v, w = M.random_worlds(P["n_worlds"], P["seed"])
xw = w * v / (kT * a)
Jw = np.array([M.brute_min(a[i], v[i], w[i], kT[i], n=4001)[0] for i in range(len(xw))]) / (kT * a)
ax.scatter(xw, Jw, s=8, color="white", edgecolor=NAVY, lw=0.5, zorder=5, alpha=0.9)
lx = np.array(M.ladder_xs(P["x_slowest"], P["rho"], P["rungs"]))
ly = M.F(lx)
on = lx > 1
ax.scatter(lx[on], ly[on], s=150, color=GREEN, edgecolor="white", lw=1.6, zorder=7)
ax.scatter(lx[~on], ly[~on], s=120, facecolor="white", edgecolor=GREEN, lw=2, zorder=7)
ax.axvline(1, color=NAVY, lw=1, ls=":", zorder=1)
ax.text(1.12, 1.6e-2, "x = 1", fontsize=10.5, color=NAVY, va="bottom")
ax.text(0.1, 2.5e3, "NO MEMORY\nPAYS", fontsize=13, fontweight="bold", color="#5c677d", ha="center", va="center")
ax.text(25, 2.5e3, "KEEP A MEMORY", fontsize=13, fontweight="bold", color=BLUE, ha="center", va="center")
ax.text(25, 1.0e3, "MSE = v/\u221ax", fontsize=10.5, color=BLUE, ha="center", va="center")
ax.annotate("LAYERS: one system's\ntime scales, each read alone,\nrates \u03c1 = %g apart.\n4 sit past x = 1 \u2192 4 stores.\nStakes \u00d7%g \u2192 one more."
            % (P["rho"], P["rho"]), xy=(lx[2], ly[2]), xytext=(0.10, 62), fontsize=8.6, color=GREEN, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color=GREEN, lw=1.2))
ax.annotate("%d separate copies\nof a %d-item sum" % (K, K), xy=(2e3, float(M.separate_copies(2e3, K))), xytext=(6.2e2, 5.2),
            fontsize=10, color=ORANGE, ha="center", va="center", arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.2))
ax.set_xlabel("x = stake \u00d7 signal variance \u00f7 (kT \u00d7 signal rate) = w\u00b7v / (kT\u00b7a)", fontsize=11, color=NAVY)
ax.set_ylabel("minimum cost \u00f7 (kT\u00b7a)", fontsize=11, color=NAVY)
ax.tick_params(labelsize=9.5, colors=NAVY)
for s in ax.spines.values():
    s.set_color(NAVY)
fig.text(0.075, 0.718, "\u25cb %d random model worlds, raw stakes over %d decades, minimized numerically (computed, not data)"
         % (len(xw), int(np.log10(w.max() / w.min()))), fontsize=8.8, color=NAVY, va="center")

# ---------------- SPACE panel: holographic memory, cut, boundary ----------------
X0 = 0.555
fig.text(X0, 0.752, "SPACE \u2022 what to hold, and where", fontsize=13.5, fontweight="bold", color=TEAL, va="center")

def tbox(y0, h, color, title, chiptext, lines, size=9.6):
    axb = fig.add_axes([X0, y0, 0.415, h]); axb.axis("off")
    axb.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.05", transform=axb.transAxes,
                                 facecolor=color + "12", edgecolor=color, lw=1.4))
    axb.text(0.025, 0.88, title, fontsize=12, fontweight="bold", color=color, va="center", transform=axb.transAxes)
    axb.text(0.975, 0.88, chiptext, fontsize=8.5, fontweight="bold", color="white", va="center", ha="right",
             transform=axb.transAxes, bbox=dict(boxstyle="round,pad=0.25", fc=color, ec=color))
    axb.text(0.025, 0.73, lines, fontsize=size, color=NAVY, va="top", transform=axb.transAxes, linespacing=1.35)
    return axb

tbox(0.60, 0.13, ORANGE, "HOLOGRAPHIC MEMORY", "T42 \u2022 WORKED-CLASS-ONLY",
     "A decision that combines %d items: one shared memory sits on the curve and\n"
     "pays from x = 1; %d separate copies wait until x = %d and cost \u2192 2\u00d7 (\u221a%d).\n"
     "Ties or loses when each item is read alone." % (K, K, K, K), size=9.0)

tbox(0.455, 0.13, "#b35c00", "THE SWARM RULE", "SYNTHESIS \u2022 IN-CLASS CLAUSES",
     "A part stays iff \u03bb\u00b7s\u00b7c < w\u00b7\u03a6: signal change rate \u00d7 its share of the price\n"
     "of following, against its stake \u00d7 the signal's worth. Its choice is the whole's\n"
     "iff shares match stakes, s = w/W (each clause in its THEORY Appendix B class).", size=9.0)

ab = tbox(0.205, 0.235, TEAL, "FIELD, CUT, BOUNDARY", "T41, T44, T62 \u2022 WORKED-CLASS-ONLY", "", size=9.6)
rows = M.cut_vs_bulk()
axs = fig.add_axes([X0 + 0.035, 0.235, 0.15, 0.145])
nn = np.array([r[0] for r in rows], float)
axs.loglog(nn, [r[1] for r in rows], "o-", color=GREY, lw=2, ms=4)
axs.loglog(nn, [r[3] for r in rows], "o-", color=TEAL, lw=2.4, ms=4)
axs.set_xticks([6, 8, 10, 16]); axs.set_xticklabels(["6", "8", "10", "16"])
axs.minorticks_off()
axs.tick_params(labelsize=8, colors=NAVY)
axs.set_xlabel("lattice side n (2-D)", fontsize=8.5, color=NAVY, labelpad=1)
axs.set_ylabel("min heat (kT)", fontsize=8.5, color=NAVY, labelpad=1)
axs.text(6.1, 2300, "every site:\n13\u00b7n\u00b2", fontsize=8.5, color="#5c677d", va="top")
axs.text(6.1, 300, "a named cut:\n\u224813.61\u00b7n", fontsize=8.5, color=TEAL, va="top")
axs.set_ylim(60, 5000)
fig.text(X0 + 0.205, 0.395,
         "Per-site error everywhere: heat scales\n"
         "with the volume; with a cut only when\n"
         "the decision names it (\u224813.61 per cut\n"
         "site, bound 13). For decisions outside a\n"
         "region the blanket suffices (T44). Through\n"
         "finite-capacity channels the tracked rate\n"
         "scales with area (T62, class AL);\n"
         "not the holographic bound.", fontsize=8.8, color=NAVY, va="top", linespacing=1.28)

# ---------------- status strip ----------------
def sbox(x0, wdt, color, tag, text):
    axb = fig.add_axes([x0, 0.04, wdt, 0.10]); axb.axis("off")
    axb.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.12", transform=axb.transAxes,
                                 facecolor=color + "14", edgecolor=color, lw=1.4))
    axb.text(0.03, 0.80, tag, fontsize=10.5, fontweight="bold", color=color, va="center", transform=axb.transAxes)
    axb.text(0.03, 0.36, text, fontsize=8.6, color=NAVY, va="center", transform=axb.transAxes, linespacing=1.3)

sbox(0.03, 0.335, GREEN, "GENERAL (scope: ledger header)",
     "R1: additive price sum (A1\u2013A7). Heat \u2265 kT \u00d7 information flow\n"
     "(KNOWN for jump processes; PROVED in-model for diffusions).\n"
     "Stakes up \u2192 judgment not down (ruin cap slack). A cut screens.")
sbox(0.375, 0.305, BLUE, "WORKED-CLASS-ONLY (curve, panels)",
     "Equilibrium OU signals or a Gaussian field;\n"
     "mean-square error; memory does not move the\n"
     "signal. T62: class AL. Swarm rule: SYNTHESIS.")
sbox(0.69, 0.28, PURPLE, "HYPOTHESIS (not yet measured)",
     "Where this class applies, strongly selected\n"
     "systems sit near the curve. No real system\n"
     "has been placed on it or shown to qualify.")
fig.text(0.03, 0.012,
         "Sources (theory/): GENERAL_FORM_PHYSICS, HOLOGRAPHIC_MEMORY, HOLOGRAPHIC, BOUNDARY_SUFFICIENCY, GENERALITY (22 Nov 2026); "
         "SWARM_RULE, AREA_LAW_PROBE (23 Nov 2026). Checks: figures/master_curve_checks.py. "
         "github.com/Chad-Mitchell/theory-of-adaptive-organization \u00b7 CC0",
         fontsize=6.0, color="#5c677d", va="bottom")

fig.savefig(OUT, dpi=180, facecolor="white")
print("wrote", OUT)
