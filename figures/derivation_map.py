#!/usr/bin/env python3
"""One cost, five yields: the front-page map.

    nice -n 19 python3 figures/derivation_map.py

Writes figures/derivation_map.png beside this file. Portrait, one card wide.
Colors are a second channel. Every card also prints its status word.

  PROVED      proved inside the class named on the card
  SYNTHESIS   the five yields on one cost; not one theorem
  IN REVIEW   pull request 203; not merged
  OPEN        not derived, or not measured

A card states the claim. It does not re-prove it.
Sources: theory/GENERAL_FORM_PHYSICS_2026-11-22.md,
theory/ACTING_LOOP_2026-11-22.md §8, and the notes named on the cards.
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derivation_map.png")

PALETTE = {
    "PROVED": ("#0E5C34", "#E4F6EC"),
    "SYNTHESIS": ("#7A4308", "#FFF1DC"),
    "IN REVIEW": ("#4C3478", "#F3EEF8"),
    "OPEN": ("#3A414B", "#EEEFF2"),
    "COST": ("#143E66", "#E5F0FA"),
}

# Pre-wrapped for a phone column.
YIELDS = [
    ("LAYERS", "Per mode: one store for a paid scale, or none."),
    ("SPREAD", "One shared memory when the decision is a sum."),
    ("BOUNDARY", "Gaussian field: the blanket suffices outside."),
    ("REBUILD", "Identical units can cost less under the cap."),
    ("ACTING", "Priced channel: only if the stake covers the probe."),
]


def rounded(ax, x, y, w, h, edge, face, radius=0.08, lw=1.5):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=%s" % radius,
            linewidth=lw,
            edgecolor=edge,
            facecolor=face,
            mutation_aspect=None,
        )
    )


def main():
    width = 4.70
    left = 0.34
    right = 0.16
    inner = width - left - right
    rail = 0.08
    spine_x = 0.16

    # Vertical rhythm, top to bottom, in inches.
    top = 0.20
    title_h = 0.95
    legend_row = 0.34
    legend_gap = 0.06
    cost_h = 2.05
    stem = 0.28
    yield_h = 0.78
    yield_gap = 0.08
    synth_h = 0.95
    open_h = 2.58
    foot = 0.38
    n_yield = len(YIELDS)
    legend_h = 2 * legend_row + legend_gap

    height = (
        top
        + title_h
        + legend_h
        + 0.12
        + cost_h
        + stem
        + n_yield * yield_h
        + (n_yield - 1) * yield_gap
        + 0.16
        + synth_h
        + 0.10
        + open_h
        + foot
    )

    fig = plt.figure(figsize=(width, height), dpi=200, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")

    y = height - top
    ax.text(
        width / 2,
        y,
        "One cost, five yields",
        ha="center",
        va="top",
        fontsize=18,
        fontname="DejaVu Sans",
        color="#1A1A1A",
        fontweight="bold",
    )
    y -= 0.38
    ax.text(
        width / 2,
        y,
        "The law of adaptive organization (hypothesis):",
        ha="center",
        va="top",
        fontsize=9.5,
        fontname="DejaVu Sans",
        color="#3A414B",
    )
    y -= 0.22
    ax.text(
        width / 2,
        y,
        "strongly selected systems minimize the cost of judgment.",
        ha="center",
        va="top",
        fontsize=9.5,
        fontname="DejaVu Sans",
        color="#3A414B",
    )
    y -= 0.32

    legend = [
        ("PROVED", "inside the named class"),
        ("SYNTHESIS", "the five on one cost"),
        ("IN REVIEW", "open pull request"),
        ("OPEN", "still to derive or measure"),
    ]
    for i, (name, gloss) in enumerate(legend):
        col = i % 2
        if col == 0 and i > 0:
            y -= legend_row + legend_gap
        ink, _fill = PALETTE[name]
        x = left + col * (inner / 2 + 0.04)
        w = inner / 2 - 0.04
        ax.add_patch(
            FancyBboxPatch(
                (x, y - legend_row),
                w,
                legend_row,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                linewidth=0,
                facecolor=ink,
            )
        )
        ax.text(
            x + 0.08,
            y - legend_row / 2 + 0.07,
            name,
            ha="left",
            va="center",
            fontsize=8,
            fontname="DejaVu Sans",
            color="white",
            fontweight="bold",
        )
        ax.text(
            x + 0.08,
            y - legend_row / 2 - 0.09,
            gloss,
            ha="left",
            va="center",
            fontsize=7.5,
            fontname="DejaVu Sans",
            color="white",
        )
    y -= legend_row + 0.16

    ink, fill = PALETTE["COST"]
    y -= cost_h
    rounded(ax, left, y, inner, cost_h, ink, fill, radius=0.10, lw=1.8)
    ax.add_patch(
        FancyBboxPatch(
            (left, y),
            rail,
            cost_h,
            boxstyle="round,pad=0.0,rounding_size=0.04",
            linewidth=0,
            facecolor=ink,
        )
    )
    ax.text(
        left + 0.22,
        y + cost_h - 0.16,
        "THE COST",
        ha="left",
        va="top",
        fontsize=9,
        fontname="DejaVu Sans",
        color=ink,
        fontweight="bold",
    )
    ax.text(
        left + 0.22,
        y + cost_h - 0.40,
        "OU, independent OU, telegraph",
        ha="left",
        va="top",
        fontsize=12,
        fontname="DejaVu Sans",
        color=ink,
    )
    ax.text(
        left + inner / 2 - 0.04,
        y + cost_h - 0.78,
        r"$J=\mathrm{heat}+w\cdot\mathbb{E}[\mathrm{loss}]$",
        ha="center",
        va="top",
        fontsize=12,
        color="#1C1C1C",
    )
    ax.text(
        left + inner / 2 - 0.04,
        y + cost_h - 1.12,
        r"subject to  $P(\mathrm{ruin})\leq\varepsilon$",
        ha="center",
        va="top",
        fontsize=11,
        color="#1C1C1C",
    )
    ax.text(
        left + 0.22,
        y + 0.52,
        r"$\kappa I_{\mathrm{mem}}+hK+w\cdot\mathbb{E}[\ell]+A+L$",
        ha="left",
        va="center",
        fontsize=11,
        color="#1C1C1C",
    )
    ax.text(
        left + 0.22,
        y + 0.24,
        "THEORY still prints five terms. A different object.",
        ha="left",
        va="center",
        fontsize=10,
        fontname="DejaVu Sans",
        color="#1C1C1C",
    )

    # Spine in the left margin, from the cost down through the five yields.
    y_cost_bottom = y
    y -= stem
    first_mid = y - yield_h * 0.45
    ax.plot(
        [width / 2, width / 2, spine_x, spine_x],
        [y_cost_bottom - 0.02, y_cost_bottom - 0.10, y_cost_bottom - 0.10, first_mid],
        color="#143E66",
        lw=1.6,
        solid_capstyle="round",
    )

    ink, fill = PALETTE["PROVED"]
    for index, (name, line) in enumerate(YIELDS):
        y -= yield_h
        mid = y + yield_h * 0.55
        rounded(ax, left, y, inner, yield_h, ink, fill, radius=0.08, lw=1.3)
        ax.add_patch(
            FancyBboxPatch(
                (left, y),
                rail,
                yield_h,
                boxstyle="round,pad=0.0,rounding_size=0.03",
                linewidth=0,
                facecolor=ink,
            )
        )
        ax.plot(
            [spine_x, left - 0.02],
            [mid, mid],
            color="#143E66",
            lw=1.4,
            solid_capstyle="round",
        )
        ax.text(
            left + 0.24,
            y + yield_h - 0.16,
            name,
            ha="left",
            va="top",
            fontsize=12,
            fontname="DejaVu Sans",
            color=ink,
            fontweight="bold",
        )
        ax.text(
            left + inner - 0.12,
            y + yield_h - 0.16,
            "PROVED",
            ha="right",
            va="top",
            fontsize=8,
            fontname="DejaVu Sans",
            color=ink,
            fontweight="bold",
        )
        ax.text(
            left + 0.24,
            y + 0.22,
            line,
            ha="left",
            va="center",
            fontsize=10.5,
            fontname="DejaVu Sans",
            color="#1C1C1C",
        )
        if index < n_yield - 1:
            next_mid = y - yield_gap - yield_h * 0.45
            ax.plot(
                [spine_x, spine_x],
                [mid, next_mid],
                color="#143E66",
                lw=1.6,
                solid_capstyle="round",
            )
            y -= yield_gap

    y -= 0.16
    ink, fill = PALETTE["SYNTHESIS"]
    y -= synth_h
    rounded(ax, left, y, inner, synth_h, ink, fill, radius=0.08, lw=1.4)
    ax.text(
        left + 0.16,
        y + synth_h - 0.14,
        "SYNTHESIS",
        ha="left",
        va="top",
        fontsize=9,
        fontname="DejaVu Sans",
        color=ink,
        fontweight="bold",
    )
    ax.text(
        left + 0.16,
        y + synth_h - 0.40,
        "The five sit on one cost.",
        ha="left",
        va="top",
        fontsize=12,
        fontname="DejaVu Sans",
        color="#1C1C1C",
    )
    ax.text(
        left + 0.16,
        y + synth_h - 0.66,
        "No theorem joins the learning heat and an option.",
        ha="left",
        va="top",
        fontsize=11,
        fontname="DejaVu Sans",
        color="#1C1C1C",
    )

    y -= 0.10
    ink, fill = PALETTE["OPEN"]
    y -= open_h
    rounded(ax, left, y, inner, open_h, ink, fill, radius=0.08, lw=1.3)
    ax.text(
        left + 0.16,
        y + open_h - 0.14,
        "STILL OPEN",
        ha="left",
        va="top",
        fontsize=9,
        fontname="DejaVu Sans",
        color=ink,
        fontweight="bold",
    )
    open_lines = [
        "Non-Gaussian case. A real-data test.",
        "Fractal draft, pull request 192.",
        "Adopt the derivation after review.",
        "Puzzle: the 5% radius bins at 2 and 2.",
        "Puzzle: J*(8) sits just under 5.",
    ]
    cursor = y + open_h - 0.44
    for line in open_lines:
        ax.text(
            left + 0.16,
            cursor,
            line,
            ha="left",
            va="top",
            fontsize=11,
            fontname="DejaVu Sans",
            color="#1C1C1C",
        )
        cursor -= 0.30

    # In-review chip, below the open lines, own color.
    ink_r, fill_r = PALETTE["IN REVIEW"]
    chip_h = 0.38
    chip_y = y + 0.14
    ax.add_patch(
        FancyBboxPatch(
            (left + 0.14, chip_y),
            inner - 0.28,
            chip_h,
            boxstyle="round,pad=0.01,rounding_size=0.06",
            linewidth=1.0,
            edgecolor=ink_r,
            facecolor=fill_r,
        )
    )
    ax.text(
        left + 0.26,
        chip_y + chip_h / 2,
        "IN REVIEW   ·   acting derivation, #203",
        ha="left",
        va="center",
        fontsize=9,
        fontname="DejaVu Sans",
        color=ink_r,
        fontweight="bold",
    )

    ax.text(
        width / 2,
        0.18,
        "22 Nov 2026   ·   sources in the README caption",
        ha="center",
        va="center",
        fontsize=8,
        fontname="DejaVu Sans",
        color="#6A717A",
    )

    fig.savefig(OUT, dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
