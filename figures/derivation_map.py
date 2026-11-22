#!/usr/bin/env python3
"""The derivation map on the front page.

    nice -n 19 python3 figures/derivation_map.py

Writes figures/derivation_map.png beside this file. Portrait, one card wide,
so a phone can read each line. Colors are a second channel: every card also
prints its status word.

  KNOWN        published and credited (Horowitz and Esposito 2014)
  PROVED       proved inside the class named on the card
  CONJECTURE   the hypothesis about nature, not a theorem
  OPEN         not derived, or not measured

The chain is the one in theory/GENERAL_FORM_PHYSICS_2026-11-22.md,
theory/GENERAL_FORM.md, and theory/HOLOGRAPHIC_2026-11-22.md.
A card states the claim. It does not re-prove it.
"""
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "derivation_map.png")

# Ink, pale fill, pill. Text is always the dark ink, on the pale fill.
PALETTE = {
    "KNOWN": ("#143E66", "#E5F0FA", "#143E66"),
    "PROVED": ("#0E5C34", "#E4F6EC", "#0E5C34"),
    "CONJECTURE": ("#7A4308", "#FFF1DC", "#7A4308"),
    "OPEN": ("#3A414B", "#EEEFF2", "#3A414B"),
}

# Pre-wrapped. Line length is chosen for a phone column, not for a desktop page.
CARDS = [
    {
        "status": "KNOWN",
        "title": "Physics floor",
        "body": [
            "Heat  ≥  kT × learning rate.",
            "The bath that holds a memory",
            "pays at least temperature times",
            "the rate at which the memory",
            "learns the world it acts on.",
            "Horowitz and Esposito, 2014.",
        ],
    },
    {
        "status": "PROVED",
        "title": "Cost of judgment, in class",
        "body": [
            "J  =  heat  +  w × expected loss,",
            "with  P(ruin) ≤ ε  beside the sum.",
            "OU floor:  kT a (v − ε) / ε,",
            "approached as the rate diverges.",
            "Telegraph: heat approaches",
            "kT times that flow.",
            "The stake w and the ruin cap",
            "are assumed, not derived.",
        ],
    },
    {
        "status": "PROVED",
        "title": "Frontier from selection",
        "body": [
            "A growth maximizer is Pareto",
            "in a chosen vector of bads",
            "(Lemma LY), if offspring falls",
            "in each coordinate.",
            "The priced sum is the special",
            "case when prices are linear:",
            "extra assumptions, a linear",
            "formula. Not a claim that",
            "judgment is a gas.",
            "The vector is not derived.",
            "Occupation of the front is open.",
        ],
    },
    {
        "status": "CONJECTURE",
        "title": "Hypothesis",
        "body": [
            "Strongly selected systems",
            "minimize the cost of judgment.",
            "The limits above need no",
            "experiment. This sentence does.",
            "No system has yet qualified.",
        ],
    },
    {
        "status": "PROVED",
        "title": "Theorems, in the same class",
        "body": [
            "Frontier",
            "    2√(kT a v w) − kT a",
            "Layers, no free constant",
            "    floor(log(wv / kTa) / log ρ)",
            "    plus 1",
            "Sharing",
            "    one rank-one memory for a sum",
            "Cut",
            "    cost scales with the sites",
            "    the decision names",
            "    (with the volume, if every site).",
            "A holographic encoding of a bulk",
            "is a metaphor for that cut.",
        ],
    },
    {
        "status": "OPEN",
        "title": "Applications and tests",
        "body": [
            "Other signals, other losses.",
            "A memory that changes its world.",
            "Stake, attention, linking, ruin:",
            "not derived.",
            "Do qualifying systems sit",
            "near the floor? Unmeasured.",
            "Holographic memory: draft,",
            "under fixes. No result claimed.",
            "THEORY §3 still states the",
            "five-term sum. Adoption is T40.",
        ],
    },
]


def main():
    # A narrow column. Relative to this width, 15 pt body is about 16 px
    # when the image is shown at a phone's width.
    width_in = 4.35
    left = 0.22
    right = 0.22
    inner = width_in - left - right
    top = 0.28
    title_block = 0.82
    legend_h = 1.84
    arrow_h = 0.30
    pad_y = 0.14
    header_h = 0.56
    line_h = 0.25

    heights = []
    for card in CARDS:
        heights.append(pad_y + header_h + line_h * len(card["body"]) + pad_y)

    body_h = sum(heights) + arrow_h * (len(CARDS) - 1) + 0.10
    height_in = top + title_block + legend_h + body_h + 0.42

    fig = plt.figure(figsize=(width_in, height_in), dpi=200, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width_in)
    ax.set_ylim(0, height_in)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    y = height_in - top
    ax.text(
        width_in / 2,
        y,
        "How the derivation sits",
        ha="center",
        va="top",
        fontsize=20,
        fontname="DejaVu Sans",
        color="#1A1A1A",
    )
    y -= 0.42
    ax.text(
        width_in / 2,
        y,
        "Limits, then the hypothesis, then what is open.",
        ha="center",
        va="top",
        fontsize=12.5,
        fontname="DejaVu Sans",
        color="#3A414B",
    )
    y -= 0.38

    # One full-width row per status, so the gloss cannot run into the name.
    legend = [
        ("KNOWN", "published, credited"),
        ("PROVED", "inside the named class"),
        ("CONJECTURE", "the hypothesis"),
        ("OPEN", "not derived or measured"),
    ]
    bar_h = 0.36
    bar_gap = 0.08
    for name, gloss in legend:
        y -= bar_h
        ink, _fill, _pill = PALETTE[name]
        ax.add_patch(
            FancyBboxPatch(
                (left, y),
                inner,
                bar_h,
                boxstyle="round,pad=0.01,rounding_size=0.08",
                linewidth=0,
                facecolor=ink,
            )
        )
        ax.text(
            left + 0.14,
            y + bar_h / 2,
            name + "   ·   " + gloss,
            ha="left",
            va="center",
            fontsize=11,
            fontname="DejaVu Sans",
            color="white",
            fontweight="bold",
        )
        y -= bar_gap
    y -= 0.06

    for index, card in enumerate(CARDS):
        ink, fill, _pill = PALETTE[card["status"]]
        h = heights[index]
        y -= h
        ax.add_patch(
            FancyBboxPatch(
                (left, y),
                inner,
                h,
                boxstyle="round,pad=0.012,rounding_size=0.10",
                linewidth=1.4,
                edgecolor=ink,
                facecolor=fill,
            )
        )
        # Status rail, so the color survives if the fill is washed out.
        ax.add_patch(
            FancyBboxPatch(
                (left, y),
                0.08,
                h,
                boxstyle="round,pad=0.0,rounding_size=0.04",
                linewidth=0,
                facecolor=ink,
            )
        )
        # Status on its own line, then the title, so the two cannot collide.
        ax.text(
            left + 0.22,
            y + h - pad_y,
            card["status"],
            ha="left",
            va="top",
            fontsize=10,
            fontname="DejaVu Sans",
            color=ink,
            fontweight="bold",
        )
        ax.text(
            left + 0.22,
            y + h - pad_y - 0.24,
            card["title"],
            ha="left",
            va="top",
            fontsize=15,
            fontname="DejaVu Sans",
            color=ink,
        )
        cursor = y + h - pad_y - header_h
        for line in card["body"]:
            ax.text(
                left + 0.22,
                cursor,
                line,
                ha="left",
                va="top",
                fontsize=13.5,
                fontname="DejaVu Sans",
                color="#1C1C1C",
            )
            cursor -= line_h
        if index < len(CARDS) - 1:
            y -= arrow_h
            ax.text(
                width_in / 2,
                y + arrow_h * 0.55,
                "↓",
                ha="center",
                va="center",
                fontsize=16,
                fontname="DejaVu Sans",
                color="#5C6570",
            )

    ax.text(
        width_in / 2,
        0.22,
        "22 Nov 2026  ·  sources in the figure caption of README.md",
        ha="center",
        va="center",
        fontsize=8.5,
        fontname="DejaVu Sans",
        color="#6A717A",
    )

    fig.savefig(OUT, dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
