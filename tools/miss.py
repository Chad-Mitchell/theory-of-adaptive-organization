#!/usr/bin/env python3
"""Log a miss at the moment it happens, in the one place it belongs, in the one format (process/PROCESS.md section 2).

A process miss is one row in process/FAILURES.md (the ten columns of its ledger). A model or measurement/code miss of a
test is one row in that test's DEVIATIONS.md (the eight fields of process/MISS_LOG_TEMPLATE.md). Every row names its
root cause, R1 to R7 (process/FAILURES.md, "Root-cause codes").

  python3 tools/miss.py --id ID --prediction TEXT --outcome TEXT --miss TEXT --cause "R3: ..." \\
        [--location process|model|measurement/code] [--stake low|medium|high] [--update TEXT] [--date YYYY-MM-DD] \\
        [--deviations PATH]          (required for a model or measurement/code miss)
  python3 tools/miss.py --batch rows.json      (a list of objects with the same keys; a medium or high entry
                                                also carries "block": its three items, which go below the ledger)
                                                a process row may carry "covers": [ids of DEVIATIONS rows it logs]
  python3 tools/miss.py --check-corrections [BASE]
        every commit since BASE (default: the merge base with origin/main) whose subject corrects something names a
        row: a FAILURES or DEVIATIONS id that exists, or the trailer `Miss: none (<reason>)`.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILURES = "process/FAILURES.md"
ROOT_CAUSE = re.compile(r"\bR[1-7]\b")
ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
STAKES = ("low", "medium", "high")
LOCATIONS = ("process", "model", "measurement/code")
CORRECTION = re.compile(r"^(?:\S+: )?(?:correct|fix|revert|restore|withdraw|retract|errat)", re.I)
BLOCK_HEADS = ("Locked prediction and risk.", "Miss and location.", "Update.")


class MissError(ValueError):
    pass


def _cell(s):
    s = " ".join(str(s).split())
    if not s:
        raise MissError("empty cell")
    return s.replace("|", "\\|")


def existing_ids(root):
    """Every row id in FAILURES and in every DEVIATIONS*.md, so an id is never used twice."""
    ids = set()
    text = open(os.path.join(root, FAILURES), encoding="utf-8").read()
    ids |= set(re.findall(r"^\| 20\d\d-\d\d-\d\d \| `([^`]+)`", text, re.M))
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", ".lake")]
        for f in fn:
            if f.startswith("DEVIATIONS") and f.endswith(".md"):
                t = open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
                ids |= set(re.findall(r"^\| `([^`]+)`", t, re.M))
    return ids


def validate(row, ids):
    r = dict(row)
    r.setdefault("location", "process")
    r.setdefault("stake", "low")
    r.setdefault("update", "none yet")
    r.setdefault("breach", "none")
    r.setdefault("date", datetime.date.today().isoformat())
    for k in ("id", "prediction", "outcome", "miss", "cause"):
        if not str(r.get(k, "")).strip():
            raise MissError("%s: missing %s" % (r.get("id", "?"), k))
    if not ID_RE.match(r["id"]):
        raise MissError("%s: an id is upper case letters, digits and hyphens" % r["id"])
    if r["id"] in ids:
        raise MissError("%s: id already used" % r["id"])
    if not ROOT_CAUSE.search(r["cause"]):
        raise MissError("%s: the cause names no root cause R1 to R7" % r["id"])
    if r["stake"] not in STAKES:
        raise MissError("%s: stake must be one of %s" % (r["id"], STAKES))
    if r["location"] not in LOCATIONS:
        raise MissError("%s: location must be one of %s" % (r["id"], LOCATIONS))
    if not re.fullmatch(r"20\d\d-\d\d-\d\d", r["date"]):
        raise MissError("%s: date must be YYYY-MM-DD" % r["id"])
    if r["stake"] != "low" and (not isinstance(r.get("block"), list) or len(r["block"]) != 3
                                or not all(str(x).strip() for x in r["block"])):
        raise MissError("%s: a %s entry adds its three-item block (prediction and risk, miss and location, update)"
                        % (r["id"], r["stake"]))
    if r["location"] != "process" and not r.get("deviations"):
        raise MissError("%s: a %s miss goes in its test's DEVIATIONS.md (--deviations)" % (r["id"], r["location"]))
    return r


def _check_target(root, r):
    if r["location"] != "process":
        d = os.path.dirname(os.path.join(root, r["deviations"]))
        if not os.path.basename(r["deviations"]).startswith("DEVIATIONS") or not os.path.isdir(d):
            raise MissError("%s: %s is not a DEVIATIONS file in an existing test folder" % (r["id"], r["deviations"]))


def failures_line(r):
    idcell = "`%s`" % r["id"]
    if r.get("covers"):
        idcell += " (DEVIATIONS %s)" % ", ".join(r["covers"])
    cells = [r["date"], idcell, r["prediction"], r["outcome"], r["miss"], r["cause"], r["location"],
             r["stake"], r["update"], r["breach"]]
    return "| " + " | ".join(_cell(c) if i != 1 else c for i, c in enumerate(cells)) + " |"


def deviations_line(r):
    cells = ["`%s`" % r["id"], r["prediction"], r["outcome"], r["miss"] + " (cause: %s)" % r["cause"], r["location"],
             r["stake"], r["update"], r["breach"]]
    return "| " + " | ".join(_cell(c) if i else c for i, c in enumerate(cells)) + " |"


def block_text(r):
    items = ["%d. **%s** %s" % (i + 1, h, " ".join(str(x).split())) for i, (h, x) in enumerate(zip(BLOCK_HEADS, r["block"]))]
    return "\n".join(["", "### %s `%s` (%s)" % (r["date"], r["id"], r["stake"])] + items)


def append_failures(root, lines, blocks):
    """Rows go after the last row of the last ledger table; medium and high blocks go at the end of the file."""
    p = os.path.join(root, FAILURES)
    L = open(p, encoding="utf-8").read().rstrip("\n").split("\n")
    if lines:
        last = max(i for i, l in enumerate(L) if re.match(r"^\| 20\d\d-\d\d-\d\d \| `", l))
        L[last + 1:last + 1] = lines
    text = "\n".join(L) + "\n"
    if blocks:
        text += "\n".join(block_text(r) for r in blocks) + "\n"
    open(p, "w", encoding="utf-8").write(text)


def append_deviations(root, path, lines):
    p = os.path.join(root, path)
    header = ("| prediction_id | locked_prediction | outcome | miss | location | stake_x_info | update | breach_check |\n"
              "|---|---|---|---|---|---|---|---|")
    text = open(p, encoding="utf-8").read() if os.path.isfile(p) else "# Deviations\n"
    L = text.rstrip("\n").split("\n")
    rows = [i for i, l in enumerate(L) if l.startswith("| `")]
    if rows and L[rows[-1]].count(" | ") == lines[0].count(" | "):
        L[rows[-1] + 1:rows[-1] + 1] = lines
    else:
        L += ["", "Rows logged with `tools/miss.py`:", "", header] + lines
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")


def log(root, rows):
    """Validate every row first; write only when all are good."""
    ids = existing_ids(root)
    checked = []
    for row in rows:
        r = validate(row, ids)
        _check_target(root, r)
        ids.add(r["id"])
        checked.append(r)
    proc = [r for r in checked if r["location"] == "process"]
    if proc:
        append_failures(root, [failures_line(r) for r in proc], [r for r in proc if r["stake"] != "low"])
    for r in checked:
        if r["location"] != "process":
            append_deviations(root, r["deviations"], [deviations_line(r)])
    return [r["id"] for r in checked]


# ------------------------------------------------------------------ corrections have rows
def _git(root, *a):
    return subprocess.run(["git", *a], cwd=root, capture_output=True, text=True)


def corrections_without_rows(root, base=None, ids=None):
    """[(sha, subject)] of commits since base whose subject corrects something and that name no row."""
    if base is None:
        mb = _git(root, "merge-base", "HEAD", "origin/main")
        if mb.returncode != 0:
            return None
        base = mb.stdout.strip()
    ids = existing_ids(root) if ids is None else ids
    # Commits from before this check existed (the commit that added tools/miss.py and its ancestors) are not judged.
    adopt = _git(root, "log", "--diff-filter=A", "--format=%H", "--", "tools/miss.py").stdout.split()
    if os.path.isfile(os.path.join(root, "tools", "miss.py")) and not adopt:
        return []  # not committed yet: nothing in the range comes after the check
    excl = ["^" + adopt[-1]] if adopt else []
    r = _git(root, "log", "--no-merges", "--format=%H%x1f%s%x1f%b%x1e", "%s..HEAD" % base, *excl)
    out = []
    for rec in r.stdout.split("\x1e"):
        if not rec.strip():
            continue
        sha, subj, body = (rec.strip("\n").split("\x1f") + ["", ""])[:3]
        if not CORRECTION.search(subj):
            continue
        text = subj + "\n" + body
        if re.search(r"^Miss: none \(\S.*\)$", text, re.M):
            continue
        if any(re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(i), text) for i in ids):
            continue
        out.append((sha[:10], subj))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for k in ("id", "prediction", "outcome", "miss", "cause", "date", "deviations", "batch"):
        ap.add_argument("--" + k)
    ap.add_argument("--location", default="process")
    ap.add_argument("--stake", default="low")
    ap.add_argument("--update", default="none yet")
    ap.add_argument("--check-corrections", nargs="?", const="", default=None)
    ap.add_argument("--check-logged", action="store_true", help="fail on a process miss logged elsewhere with no FAILURES row")
    ap.add_argument("--root", default=ROOT)
    a = ap.parse_args(argv)
    if a.check_corrections is not None:
        bad = corrections_without_rows(a.root, a.check_corrections or None)
        if bad is None:
            print("corrections: not checked (no origin/main to compare with)\nRESULT: PARTIAL")
            return 2
        for sha, s in bad:
            print("  FAIL commit %s corrects something but names no FAILURES/DEVIATIONS row: %s" % (sha, s))
        print("corrections: %d without a row; RESULT: %s" % (len(bad), "FAIL" if bad else "PASS"))
        return 1 if bad else 0
    if a.check_logged:
        bad = logged_without_row(a.root)
        for x in bad:
            print("  FAIL " + x)
        print("logged process misses: %d without a FAILURES row; RESULT: %s" % (len(bad), "FAIL" if bad else "PASS"))
        return 1 if bad else 0
    if a.batch:
        rows = json.load(open(a.batch, encoding="utf-8"))
    else:
        rows = [{k: v for k, v in dict(id=a.id, prediction=a.prediction, outcome=a.outcome, miss=a.miss, cause=a.cause,
                                       location=a.location, stake=a.stake, update=a.update, date=a.date,
                                       deviations=a.deviations).items() if v is not None}]
    try:
        done = log(a.root, rows)
    except MissError as e:
        print("miss.py: %s (nothing written)" % e)
        return 1
    print("logged %d row(s): %s" % (len(done), ", ".join(done)))
    refresh_counts(a.root)
    return 0


# Process misses logged outside FAILURES before tools/miss.py existed: (file, its old path, sections holding them).
PROCESS_MISS_SOURCES = [("records/notes/MISSES-LEDGER.md", "NOTES/MISSES-LEDGER.md", ("## 4.", "## 5."))]


def logged_without_row(root):
    """Process misses recorded elsewhere that no FAILURES row names: a row of a MISSES-LEDGER process section
    (named in FAILURES as "MISSES-LEDGER P5"), or a DEVIATIONS row whose location is process (named by its id)."""
    ftext = open(os.path.join(root, FAILURES), encoding="utf-8").read()
    named = set()
    for m in re.finditer(r"MISSES-LEDGER ((?:[A-Z]\d+(?:, )?)+)", ftext):
        named |= set(re.findall(r"[A-Z]\d+", m.group(1)))
    out = []
    for new, old, secs in PROCESS_MISS_SOURCES:
        path = new if os.path.isfile(os.path.join(root, new)) else old
        full = os.path.join(root, path)
        if not os.path.isfile(full):
            out.append("%s missing (process misses cannot be checked)" % new)
            continue
        sec = ""
        for line in open(full, encoding="utf-8"):
            if line.startswith("## "):
                sec = line
            m = re.match(r"^\| ([A-Z]\d+) \|", line)
            if m and sec.startswith(secs) and m.group(1) not in named:
                out.append("%s %s is a process miss that no FAILURES row names (add \"(MISSES-LEDGER %s)\" to the row "
                           "that covers it, or log one)" % (path, m.group(1), m.group(1)))
    # A DEVIATIONS process row is covered by a FAILURES row with the same id, or one whose id cell names it as
    # "(DEVIATIONS X-P1)"; a mention in another row's prose does not count.
    ids = set()
    for cell in re.findall(r"^\| 20\d\d-\d\d-\d\d \| ([^|]+)\|", ftext, re.M):
        ids |= set(re.findall(r"`([^`]+)`", cell))
        for m in re.finditer(r"DEVIATIONS ((?:[\w.\-]+(?:, )?)+)", cell):
            ids |= {x.strip() for x in m.group(1).split(",")}
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.startswith("DEVIATIONS") or not f.endswith(".md"):
                continue
            full = os.path.join(dirpath, f)
            header = None
            for line in open(full, encoding="utf-8", errors="replace"):
                if not line.startswith("|"):
                    header = None if not line.strip() else header
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if header is None:
                    header = [c.lower() for c in cells]
                    continue
                if "location" not in header or set("".join(cells)) <= set("-: "):
                    continue
                loc = cells[header.index("location")].lower() if len(cells) > header.index("location") else ""
                rid = cells[0].strip("` ")
                if loc.startswith("process") and rid not in ids:
                    out.append("%s: %s has location process and no FAILURES row" % (os.path.relpath(full, root), rid))
    return out


def refresh_counts(root):
    """Rewrite the generated counts on process/PROCESS.md (the gen:misses block) so a logged row never leaves them stale."""
    page = os.path.join(root, "process", "PROCESS.md")
    if not os.path.isfile(page):
        return
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import facts
    text = open(page, encoding="utf-8").read()
    new, _ = facts.render(root, "process/PROCESS.md", text)
    if new != text:
        open(page, "w", encoding="utf-8").write(new)
        print("refreshed the generated counts in process/PROCESS.md")


if __name__ == "__main__":
    sys.exit(main())
