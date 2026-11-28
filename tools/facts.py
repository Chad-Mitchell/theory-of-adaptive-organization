#!/usr/bin/env python3
"""Numbers on maintained pages: generated blocks for live counts, and a quote check for counts from finished runs.

A live count (it changes as the repository changes: the ledger tally, misses logged, the Lean total) is written only
between `<!-- gen:NAME -->` and `<!-- /gen:NAME -->` markers, by one generator per NAME reading its one source. A quoted
count (a measurement from a finished run, such as 12,093 draws or 3/8) is checked against the frozen file it cites.

  python3 tools/facts.py --write    rewrite every gen block from its source (nothing outside the markers)
  python3 tools/facts.py --check    FAIL on a stale block, an unknown block, or a quoted count its frozen source lacks
  python3 tools/facts.py --list-escapes

The quote check. On the front pages (QUOTE_PAGES), outside gen blocks and math, a count token is a grouped number
(12,093), a ratio (3/8, 29 of 42), or a number or number word followed by a counted noun. Each token must sit in a
paragraph or table row that cites a source by path, and appear (commas, number words and "a of b" normalized) in a
cited source that is frozen: hash-locked, in LOCKED_BLOBS.txt, under records/, THEORY.md, or a run file
(RESULTS*, DEVIATIONS*, RUN_LOG*, *.out) in a folder, or below a folder, that holds a PREREG*.md. A count whose only
source is a maintained page fails: make it a gen block. `<!-- q:ok reason -->` in the paragraph exempts a number that
is not a count; --list-escapes prints every use.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import movemap  # noqa: E402

CLAIM_MAP = "measurement/CLAIM_MAP_v2.md"
FAILURES = "process/FAILURES.md"
GEN = re.compile(r"<!-- gen:([a-z]+) -->(.*?)<!-- /gen:\1 -->", re.S)
GEN_OPEN = re.compile(r"<!-- /?gen:([a-z]+) -->")
EXTRA_PAGES = []
QUOTE_PAGES = ["README.md", "CORE.md"]


class Pending(Exception):
    """A generator whose structured source does not exist yet; the block keeps its text (GEN_PENDING)."""


def _read(root, p):
    fp = os.path.join(root, p)
    return open(fp, encoding="utf-8").read() if os.path.isfile(fp) else ""


def pages(root):
    from check_consistency import MAINTAINED_DOCS
    return [p for p in list(MAINTAINED_DOCS) + EXTRA_PAGES if os.path.isfile(os.path.join(root, p))]


# ------------------------------------------------------------------ generators (pure functions of committed files)
def tally_counts(root):
    """{status: rows} from the CLAIM_MAP tally block, which check_consistency.py recomputes from every row."""
    m = re.search(r"<!-- tally:begin -->(.*?)<!-- tally:end -->", _read(root, CLAIM_MAP), re.S)
    out = {}
    for line in (m.group(1) if m else "").splitlines():
        c = [x.replace("*", "").strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 2 and c[1].isdigit() and c[0] != "Total":
            out[c[0]] = int(c[1])
    return out


def gen_field(root):
    t = tally_counts(root)
    passed = sum(v for k, v in t.items() if k.startswith("NOT A TEST") and "proxy: passed" in k)
    failed = sum(v for k, v in t.items() if k.startswith("NOT A TEST") and "proxy: failed" in k)
    other = sum(v for k, v in t.items() if k.startswith("NOT A TEST")) - passed - failed
    tail = ", %d other" % other if other else ""
    return "NOT A TEST (%d rows: %d passed on proxy, %d failed on proxy%s) or INCONCLUSIVE (%d rows)" % (
        passed + failed + other, passed, failed, tail, t.get("INCONCLUSIVE", 0))


ROOT_CAUSES = ("R1", "R2", "R3", "R4", "R5", "R6", "R7")


def failures_rows(text):
    """[(id, cells)] for every ledger row of process/FAILURES.md (every table)."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^\| (20\d\d-\d\d-\d\d) \| `([^`]+)`", line)
        if m:
            out.append((m.group(2), [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]))
    return out


def gen_misses(root):
    rows = failures_rows(_read(root, FAILURES))
    by = {r: 0 for r in ROOT_CAUSES}
    none = 0
    for _id, cells in rows:
        codes = set(re.findall(r"\bR[1-7]\b", cells[5] if len(cells) > 5 else ""))
        for c in codes:
            by[c] += 1
        none += not codes
    return "%d rows. By root cause (a row can carry two): %s; no code: %d" % (
        len(rows), ", ".join("%s %d" % (k, v) for k, v in by.items()), none)


def gen_scored(root):
    raise Pending("needs a per-test bars table with a source path per bar (FAILURES SCORED-UNSOURCED)")


GENERATORS = {"field": gen_field, "misses": gen_misses, "scored": gen_scored}
# Shrink-only: blocks whose generator has no structured source yet. Each keeps its text, says so, and has a FAILURES
# row; tools/test_facts.py asserts this set equals the blocks whose generator is pending.
GEN_PENDING = {"measurement/CLAIM_MAP_v2.md:scored"}


def render(root, page, text):
    """(new text, [problems]) with every gen block re-rendered."""
    problems = []

    def one(m):
        name = m.group(1)
        if name not in GENERATORS:
            problems.append("%s: unknown gen block %r" % (page, name))
            return m.group(0)
        try:
            body = GENERATORS[name](root)
        except Pending:
            if "%s:%s" % (page, name) not in GEN_PENDING:
                problems.append("%s: gen block %r has no source yet and is not on GEN_PENDING" % (page, name))
            return m.group(0)
        return "<!-- gen:%s -->%s<!-- /gen:%s -->" % (name, body, name)

    new = GEN.sub(one, text)
    opens = GEN_OPEN.findall(text)
    if len(opens) != 2 * len(GEN.findall(text)):
        problems.append("%s: unmatched gen marker" % page)
    return new, problems


def pending_blocks(root):
    out = set()
    for p in pages(root):
        for name, _ in GEN.findall(_read(root, p)):
            try:
                GENERATORS.get(name, lambda r: None)(root)
            except Pending:
                out.add("%s:%s" % (p, name))
    return out


def used_blocks(root):
    return {name for p in pages(root) for name, _ in GEN.findall(_read(root, p))}


# ------------------------------------------------------------------ scored results (one definition, shared)
STATUS_WORD = re.compile(r"\b(HIT|MISS|INCONCLUSIVE|CONSISTENCY_CHECK|FAILED|PASSED|SIM-PASS|SIM-FAIL|open miss|clean miss|not tested)\b")
RESULTS_NAME = re.compile(r"(^|/)RESULTS[^/]*\.md$")


def tracked(root):
    r = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.split("\n")
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", ".lake")]
        out += [os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/") for f in fn]
    return out


def scored_results(root, files=None):
    """Every tracked RESULTS*.md with at least one line carrying a status word: the one definition of scored,
    used by the LEDGER-1 rule (check_claims.py) and the gate check (check_pending.py)."""
    out = []
    for f in (files if files is not None else tracked(root)):
        if RESULTS_NAME.search(f) and not movemap.backward(f).startswith("reference/"):
            if STATUS_WORD.search(_read(root, f)):
                out.append(f)
    return sorted(out)


def scored_folders(root, files=None):
    return sorted({os.path.dirname(f) for f in scored_results(root, files)})


# ------------------------------------------------------------------ the quote check
WORDS = {w: str(i) for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve".split())}
NOUNS = r"(?:rows|draws|seeds|bars|hits|misses|identities|bodies|declarations)"
TOKEN = re.compile(r"(?<![\w.,/§\-−])(?:\d{1,3}(?:,\d{3})+|\d+/\d+|\d+ of \d+)(?![\w/]|,\d)"
                   r"|(?<![\w.,/§\-−])(?:\d+|" + "|".join(WORDS) + r")\s+" + NOUNS + r"\b", re.I)
PATHREF = re.compile(r"`([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-*]*)+)(?::[\d\-, ]+)?`|\]\(([^)#\s]+)")
ESCAPE = re.compile(r"<!--\s*q:ok\s+\S.*?-->")
MATH = re.compile(r"\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$|\$[^$\n]+\$", re.S)
FROZEN_RUN_FILE = re.compile(r"(^|/)(RESULTS[^/]*\.md|DEVIATIONS[^/]*\.md|RUN_LOG[^/]*\.md|[^/]+\.out)$")


def norm(s, ratios=True):
    s = s.lower()
    s = re.sub(r"(?<=\d),(?=\d{3})", "", s)
    s = re.sub(r"\b(" + "|".join(WORDS) + r")\b", lambda m: WORDS[m.group(1)], s)
    if ratios:
        s = re.sub(r"(\d+) of (\d+)", r"\1/\2", s)
    return s


_LOCKED = {}


def locked_paths(root):
    """Hash-locked files and every LOCKED_BLOBS.txt path (cached per root)."""
    if root not in _LOCKED:
        import verify_locks
        got = {hit for _lf, hit, _hx, _t in verify_locks.entries(root) if hit}
        for line in _read(root, "process/LOCKED_BLOBS.txt").splitlines():
            parts = line.split(None, 2)
            if len(parts) == 3 and not parts[0].startswith("#"):
                got.add(parts[0])
        _LOCKED[root] = got
    return _LOCKED[root]


def is_frozen(root, path):
    p = path.strip("/")
    if p in locked_paths(root) or movemap.forward(p).startswith("records/") or p == "THEORY.md":
        return True
    if FROZEN_RUN_FILE.search(p):
        d = os.path.dirname(p)
        while d:
            fd = os.path.join(root, d)
            if os.path.isdir(fd) and any(f.startswith("PREREG") and f.endswith(".md") for f in os.listdir(fd)):
                return True
            d = os.path.dirname(d)
    return False


def source_files(root, ref):
    """Repository files a cited path names (a file, or the text files of a folder)."""
    p = ref.split("#")[0].rstrip("/")
    for cand in (p, movemap.forward(p)):
        fp = os.path.join(root, cand)
        if os.path.isfile(fp):
            return [cand]
        if os.path.isdir(fp):
            out = []
            for dp, dn, fn in os.walk(fp):
                out += [os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/") for f in fn
                        if f.endswith((".md", ".out", ".txt", ".json"))]
            return sorted(out)
    return []


def blocks(text):
    """[(first line number, block text)]: paragraphs, with each table row its own block."""
    out, cur, start = [], [], 1
    for i, line in enumerate(text.split("\n"), 1):
        if line.startswith("|"):
            if cur:
                out.append((start, "\n".join(cur)))
                cur = []
            out.append((i, line))
        elif not line.strip():
            if cur:
                out.append((start, "\n".join(cur)))
                cur = []
        else:
            if not cur:
                start = i
            cur.append(line)
    if cur:
        out.append((start, "\n".join(cur)))
    return out


def quote_fails(root, pages_=None):
    fails = []
    for page in pages_ or QUOTE_PAGES:
        text = GEN.sub(lambda m: " " * 0 + "\n" * m.group(0).count("\n"), _read(root, page))
        for ln, blk in blocks(text):
            if ESCAPE.search(blk):
                continue
            plain = MATH.sub(lambda m: "\n" * m.group(0).count("\n"), blk)
            toks = [m for m in TOKEN.finditer(plain)]
            if not toks:
                continue
            refs = [a or b for a, b in PATHREF.findall(blk)]
            files = [f for r in refs for f in source_files(root, r) if f != page]
            frozen = [f for f in files if is_frozen(root, f)]
            corpus = "\n".join(_read(root, f) for f in frozen)
            c1, c2 = norm(corpus), norm(corpus, ratios=False)
            for m in toks:
                tok = m.group(0)
                line = ln + plain[:m.start()].count("\n")
                core = norm(tok).split()[0]
                rx = re.compile(r"(?<![\d/.])" + re.escape(core) + r"(?![\d/]|\.\d)")
                if not files:
                    fails.append("quote: %s:%d %r cites no source; cite the frozen file that holds it" % (page, line, tok))
                elif not frozen:
                    fails.append("quote: %s:%d %r cites only maintained pages (%s); make it a gen block or cite the run's frozen file" % (page, line, tok, ", ".join(sorted(set(files))[:2])))
                elif not (rx.search(c1) or rx.search(c2)):
                    fails.append("quote: %s:%d %r is not in its cited frozen source (%s)" % (page, line, tok, ", ".join(sorted(set(frozen))[:2])))
    return fails


def escapes(root):
    return ["%s:%d %s" % (p, i, m.group(0)) for p in pages(root) for i, l in enumerate(_read(root, p).split("\n"), 1)
            for m in ESCAPE.finditer(l)]


# ------------------------------------------------------------------ entry point
def check(root=ROOT, write=False):
    fails = []
    for p in pages(root):
        text = _read(root, p)
        new, problems = render(root, p, text)
        fails += problems
        if new != text:
            if write:
                open(os.path.join(root, p), "w", encoding="utf-8").write(new)
            else:
                for (n1, b1), (n2, b2) in zip(GEN.findall(text), GEN.findall(new)):
                    if b1 != b2:
                        fails.append("gen: %s block %r is stale; expected %r (run tools/facts.py --write)" % (p, n1, b2))
    pend = pending_blocks(root)
    if pend != GEN_PENDING:
        fails.append("gen: pending blocks %s differ from GEN_PENDING %s (the list only shrinks)" % (sorted(pend), sorted(GEN_PENDING)))
    unused = set(GENERATORS) - used_blocks(root)
    if unused:
        fails.append("gen: generators with no block on any page: %s" % sorted(unused))
    fails += quote_fails(root)
    return fails


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--list-escapes" in argv:
        for e in escapes(ROOT):
            print(e)
        return 0
    write = "--write" in argv
    fails = check(ROOT, write=write)
    for f in fails:
        print("  FAIL " + f)
    print("facts: %s; blocks in use: %s; RESULT: %s" % ("written" if write else "checked",
          ", ".join(sorted(used_blocks(ROOT))) or "none", "FAIL" if fails else "PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
