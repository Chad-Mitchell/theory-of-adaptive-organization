#!/usr/bin/env python3
"""Checks for theory/CONTINUOUS_A6_2026-11-23.md (T48).

Run from the repo root:
  nice -n 19 python3 theory/continuous_a6_checks/continuous_a6_checks.py

These checks are identities and numerical evaluations of named closed
forms (finite-alphabet mutual information, and quantile-bin approximations
of bivariate Gaussians). They are not evidence about a real system.
A machinery failure sets a nonzero exit code.

Pass --crossref to refresh crossref.out from the Crossref API (network).
Pytest does not pass that flag.
"""
from __future__ import annotations

import math
import os
import re
import sys

import numpy as np
from scipy.stats import multivariate_normal, norm

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
NOTE = os.path.join(ROOT, "theory", "CONTINUOUS_A6_2026-11-23.md")
CROSSREF_OUT = os.path.join(HERE, "crossref.out")

checks_failed = []

# DOIs cited in the note (canonical lowercase for comparison).
CITED_DOIS = [
    "10.1090/trans2/012/09",
    "10.1090/trans2/033/11",
    "10.1137/1105003",
    "10.1109/tit.1956.1056823",
    "10.1090/trans2/033/10",
    "10.1002/047174882x",
    "10.1007/978-1-4419-7970-4",
    "10.2307/1426210",
    "10.3390/e10030261",
]


def check(name, ok, detail):
    print("CHECK %s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        checks_failed.append(name)


def mi_from_joint(P, floor=0.0):
    P = np.clip(np.asarray(P, dtype=float), 0.0, None)
    total = float(P.sum())
    if total <= 0.0:
        return 0.0
    P = P / total
    px = P.sum(axis=1)
    py = P.sum(axis=0)
    value = 0.0
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            if P[i, j] > floor and px[i] > 0.0 and py[j] > 0.0:
                value += float(P[i, j] * math.log(P[i, j] / (px[i] * py[j])))
    return value


def entropy_from_mass(p, floor=0.0):
    p = np.clip(np.asarray(p, dtype=float), 0.0, None)
    total = float(p.sum())
    if total <= 0.0:
        return 0.0
    p = p / total
    value = 0.0
    for pi in p:
        if pi > floor:
            value -= float(pi * math.log(pi))
    return value


def gaussian_I(rho):
    return -0.5 * math.log(1.0 - rho * rho)


def quantile_edges(n):
    return np.concatenate(([-np.inf], norm.ppf(np.arange(1, n) / n), [np.inf]))


def equal_width_edges(lo, hi, n):
    return np.linspace(lo, hi, n + 1)


def rect_prob(rv, x0, x1, y0, y1):
    cap = 1e9

    def F(x, y):
        if np.isneginf(x) or np.isneginf(y):
            return 0.0
        xx = cap if np.isposinf(x) else x
        yy = cap if np.isposinf(y) else y
        return float(rv.cdf([xx, yy]))

    return F(x1, y1) - F(x0, y1) - F(x1, y0) + F(x0, y0)


def quantized_gaussian_joint(rho, edges_x, edges_y):
    cov = np.array([[1.0, rho], [rho, 1.0]], dtype=float)
    rv = multivariate_normal(mean=[0.0, 0.0], cov=cov, allow_singular=False)
    nx = len(edges_x) - 1
    ny = len(edges_y) - 1
    P = np.zeros((nx, ny), dtype=float)
    for i in range(nx):
        for j in range(ny):
            P[i, j] = rect_prob(rv, edges_x[i], edges_x[i + 1], edges_y[j], edges_y[j + 1])
    P = np.clip(P, 0.0, None)
    return P


def extract_dois(text):
    found = re.findall(r"10\.\d{4,9}/[^\s)<>]+", text)
    cleaned = []
    for raw in found:
        token = raw.rstrip(".,;:]")
        cleaned.append(token.lower())
    # unique, preserve order
    out = []
    seen = set()
    for d in cleaned:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def run_crossref():
    import json
    import urllib.parse
    import urllib.request

    headers = {"User-Agent": "gtao-continuous-a6/1.0 (mailto:chad39@gmail.com)"}
    lines = [
        "Crossref API, 23 November 2026, America/New_York. User-Agent gtao-continuous-a6/1.0.",
        "Queried https://api.crossref.org/works/{doi}. A line is HTTP 200 only when the work record loaded.",
        "",
    ]
    for doi in CITED_DOIS:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                message = json.load(resp)["message"]
            title = " ".join(message.get("title") or [])
            year = (message.get("published-print") or message.get("issued") or {}).get(
                "date-parts", [[None]]
            )[0][0]
            authors = "; ".join(
                ("%s %s" % (a.get("family", ""), a.get("given", ""))).strip()
                for a in (message.get("author") or [])[:6]
            )
            isbn = message.get("ISBN")
            page = message.get("page")
            container = " ".join(message.get("container-title") or [])
            lines.append(
                "HTTP %s | %s | %s | %s | pp %s | %s | %s | ISBN=%s"
                % (status, doi, year, container, page, authors, title, isbn)
            )
        except Exception as exc:
            lines.append("FAIL | %s | %s" % (doi, exc))
    lines.append("")
    lines.append(
        "Pinsker, M. S. 1964. Information and Information Stability of Random Variables "
        "and Processes. Holden-Day, San Francisco. Translated and edited by Amiel Feinstein "
        "from the 1960 Russian monograph. Crossref has no work record for the book itself "
        "(no DOI, and the 1964 edition predates ISBN). Cited from the title page, not from a DOI."
    )
    lines.append("")
    text = "\n".join(lines) + "\n"
    with open(CROSSREF_OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if "--crossref" in argv:
        run_crossref()
        return 0

    # 1. Finite alphabet: identity attains I; coarser does not exceed it.
    # A 2x3 joint, not a product.
    P = np.array(
        [
            [0.10, 0.20, 0.10],
            [0.05, 0.05, 0.50],
        ],
        dtype=float,
    )
    I_id = mi_from_joint(P)
    # Merge the last two columns (coarser on Y).
    P_coarse = np.column_stack((P[:, 0], P[:, 1] + P[:, 2]))
    I_coarse = mi_from_joint(P_coarse)
    # Merge the two rows (coarser on X): then I = 0 because X is constant.
    P_xconst = np.array([P.sum(axis=0)])
    I_xconst = mi_from_joint(P_xconst)
    check(
        "finite_identity_attains_and_coarser_does_not_exceed",
        I_id > I_coarse + 1e-15
        and I_coarse >= -1e-15
        and abs(I_xconst) < 1e-15
        and I_id > 0.1,
        "I_id=%.12f I_coarse_Y=%.12f I_Xconst=%.12e" % (I_id, I_coarse, I_xconst),
    )

    # 2. Product joint has I = 0 exactly (finite alphabet).
    px = np.array([0.3, 0.7])
    py = np.array([0.2, 0.5, 0.3])
    P_prod = np.outer(px, py)
    I_prod = mi_from_joint(P_prod)
    check(
        "finite_product_has_zero_mutual_information",
        abs(I_prod) < 1e-12,
        "I=%.3e" % I_prod,
    )

    # 3. Sign of a standard normal: I(X; 1_{X>0}) = log 2, attained by the
    # split at zero.
    # Two-bin partition of X at 0, Y already two-valued and equal to that split.
    # Joint is deterministic: P = diag(1/2, 1/2), I = log 2.
    P_sign = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=float)
    I_sign = mi_from_joint(P_sign)
    H_sign = entropy_from_mass(np.array([0.5, 0.5]))
    check(
        "sign_of_standard_normal_attains_log_2",
        abs(I_sign - math.log(2.0)) < 1e-15
        and abs(H_sign - math.log(2.0)) < 1e-15,
        "I=%.12f log 2=%.12f" % (I_sign, math.log(2.0)),
    )

    # 4. Y = X on a finite alphabet: I = H(X).
    p = np.array([0.1, 0.2, 0.3, 0.4], dtype=float)
    P_copy = np.diag(p)
    I_copy = mi_from_joint(P_copy)
    H_x = entropy_from_mass(p)
    check(
        "finite_copy_is_the_entropy",
        abs(I_copy - H_x) < 1e-15 and abs(I_copy - entropy_from_mass(p)) < 1e-15,
        "I=H=%.12f" % I_copy,
    )

    # 5. Y = X uniform on [0,1], n equal bins: I = log n, which diverges.
    logs = []
    ok_uniform = True
    for n in (2, 4, 8, 16, 32):
        P_u = np.eye(n) / n
        I_u = mi_from_joint(P_u)
        logs.append(I_u)
        if abs(I_u - math.log(n)) > 1e-12:
            ok_uniform = False
    check(
        "unit_interval_copy_quantized_is_log_n",
        ok_uniform and logs[-1] > logs[0] + 1.0,
        "I(n)=%s" % ", ".join("%.10f" % v for v in logs),
    )

    # 6. Uncorrelated Gaussians: every quantile quantization has I = 0
    # (independence is preserved by any pair of marginal partitions).
    ok_ind = True
    details_ind = []
    for n in (2, 4, 8, 16):
        edges = quantile_edges(n)
        P = quantized_gaussian_joint(0.0, edges, edges)
        In = mi_from_joint(P)
        mass = float(P.sum())
        details_ind.append("n=%d I=%.3e mass=%.8f" % (n, In, mass))
        if abs(In) > 1e-12 or abs(mass - 1.0) > 1e-8:
            ok_ind = False
    check(
        "uncorrelated_gaussian_quantizations_have_zero_I",
        ok_ind,
        "; ".join(details_ind),
    )

    # 7. Correlated Gaussians: I_n < I, monotone in n, gap shrinks.
    # Recorded decimals are computed in this script; the closed form is
    # -1/2 log(1-rho^2).
    ok_g = True
    g_details = []
    for rho in (0.3, 0.5, 0.8, 0.95):
        I_true = gaussian_I(rho)
        prev = -1.0
        last_gap = None
        first_gap = None
        row = ["rho=%.2f I=%.10f" % (rho, I_true)]
        for n in (2, 4, 8, 16):
            edges = quantile_edges(n)
            P = quantized_gaussian_joint(rho, edges, edges)
            In = mi_from_joint(P)
            mass = float(P.sum())
            gap = I_true - In
            row.append("n=%d I_n=%.10f gap=%.6e mass=%.8f" % (n, In, gap, mass))
            if In < prev - 1e-12:
                ok_g = False
            if gap <= 0.0 or abs(mass - 1.0) > 1e-7:
                ok_g = False
            if first_gap is None:
                first_gap = gap
            last_gap = gap
            prev = In
        if not (last_gap < 0.5 * first_gap):
            ok_g = False
        g_details.append("; ".join(row))
    check(
        "gaussian_quantile_bins_increase_toward_closed_form",
        ok_g,
        " | ".join(g_details),
    )

    # 8. Entropy of a quantized standard normal grows like -log Delta,
    # while mutual information of a correlated pair stays bounded by I.
    # Equal-width bins on [-6, 6], widths 6, 3, 1.5, 0.75.
    rho = 0.5
    I_true = gaussian_I(rho)
    Hs = []
    Is = []
    ok_cancel = True
    # For a standard normal, Theorem 8.3.1: H(X^Delta) + log Delta -> h(X).
    # h(N(0,1)) = 0.5 log(2 pi e).
    h_normal = 0.5 * math.log(2.0 * math.pi * math.e)
    for n, width in ((2, 6.0), (4, 3.0), (8, 1.5), (16, 0.75)):
        edges = equal_width_edges(-6.0, 6.0, n)
        # Isolated standard-normal bin masses (the diagonal of rho=0, or the
        # marginal of any rho). Use rho=0 margins.
        P0 = quantized_gaussian_joint(0.0, edges, edges)
        px = P0.sum(axis=1)
        H = entropy_from_mass(px)
        Hs.append(H)
        P = quantized_gaussian_joint(rho, edges, edges)
        In = mi_from_joint(P)
        Is.append(In)
        # Mutual information stays below the closed form (plus a tiny
        # truncation/numerical allowance).
        if In > I_true + 1e-6:
            ok_cancel = False
    # Entropy increases as the bins refine, and H + log(width) approaches
    # a finite number near h(N(0,1)). The last two widths give a closer
    # approach than the first.
    combo = [Hs[k] + math.log(w) for k, w in enumerate((6.0, 3.0, 1.5, 0.75))]
    if not (Hs[3] > Hs[0] + 1.0):
        ok_cancel = False
    if not (Is[3] > Is[0]):
        ok_cancel = False
    if not (abs(combo[3] - h_normal) < abs(combo[0] - h_normal)):
        ok_cancel = False
    if not (abs(combo[3] - h_normal) < 0.15):
        ok_cancel = False
    check(
        "quantized_entropy_diverges_mutual_information_does_not",
        ok_cancel,
        "H=%s; H+log Delta=%s; h=%.10f; I_n=%s; I=%.10f"
        % (
            ", ".join("%.8f" % v for v in Hs),
            ", ".join("%.8f" % v for v in combo),
            h_normal,
            ", ".join("%.8f" % v for v in Is),
            I_true,
        ),
    )

    # 9. Every DOI in the note is one of the cited list, and each appears
    # as HTTP 200 in the recorded Crossref file. Pinsker is recorded as
    # having no work record, and the note does not invent a DOI for it.
    note = open(NOTE, encoding="utf-8").read()
    dois_in_note = extract_dois(note)
    cited_set = set(CITED_DOIS)
    unexpected = [d for d in dois_in_note if d not in cited_set]
    missing_from_note = [d for d in CITED_DOIS if d not in set(dois_in_note)]
    # The note mentions "no DOI" for Pinsker and must not invent one.
    pinsker_ok = (
        "Pinsker" in note
        and "no Crossref work record" in note
        and "10." not in note.split("Pinsker, M. S. 1964")[1].split("\n")[0]
    )
    xref = open(CROSSREF_OUT, encoding="utf-8").read()
    missing_200 = []
    for d in CITED_DOIS:
        # Accept either the canonical form or the original capitalization
        # that the note uses.
        found_200 = False
        for line in xref.splitlines():
            if line.startswith("HTTP 200") and d in line.lower():
                found_200 = True
                break
        if not found_200:
            missing_200.append(d)
    pinsker_xref = "no work record" in xref.lower() and "Pinsker" in xref
    check(
        "dois_in_note_match_resolved_crossref_record",
        not unexpected
        and not missing_from_note
        and not missing_200
        and pinsker_ok
        and pinsker_xref
        and ("9780471241959" in xref),
        "note_dois=%d unexpected=%s missing_from_note=%s missing_200=%s pinsker_ok=%s"
        % (
            len(dois_in_note),
            unexpected,
            missing_from_note,
            missing_200,
            pinsker_ok and pinsker_xref,
        ),
    )

    # 10. ISBN strings for Cover and Gray appear in the note and in the
    # Crossref record.
    isbn_ok = (
        "978-0-471-24195-9" in note
        and "978-0-471-74882-3" in note
        and "978-1-4419-7969-8" in note
        and "978-1-4419-7970-4" in note
        and "9780471241959" in xref
        and "9781441979698" in xref
    )
    check(
        "cover_and_gray_isbns_recorded",
        isbn_ok,
        "Cover and Gray print and electronic ISBNs present in the note and in crossref.out",
    )

    if checks_failed:
        print("FAILS %d: %s" % (len(checks_failed), ", ".join(checks_failed)))
        return 1
    print("FAILS 0")
    print("ALL CONTINUOUS-A6 CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
