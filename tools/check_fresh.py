#!/usr/bin/env python3
"""Fail if a maintained page hand-keeps a fact that has another single source.

Since 25 November 2026 no page carries the current `main` SHA, the open-PR list
or a PR head: those change at every merge or push, so a committed copy is stale
as soon as it lands. `tools/brief.py` prints them live. Versions have one source
(the THEORY.md title, the latest CLAIM_MAP note) and the Lean total has one
(formal/lean/AUDIT.json).

What fails, on every maintained page (check_consistency.MAINTAINED_DOCS, every
root .md, process/*.md, formal/lean/README.md):
  - any SHA that is a prefix of one of the last RECENT first-parent commits of
    `main`, in any wording, unless it sits in a history block or right after
    "merged as";
  - the pointer wordings in RULES (they also work with no git history);
  - a hand-typed PR head: "head `sha`" or "PR #N (head";
  - a root .md file outside ROOT_ALLOW (a status page that comes back).
Text between `<!-- history:begin` and `<!-- history:end -->` is a dated record
and is skipped, as are the copies in files this repo may not edit (ALLOW).

Run from the repo root:  python3 tools/check_fresh.py
Exit 0 = no hand pointer. Exit 1 = at least one.
"""
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_consistency import MAINTAINED_DOCS  # noqa: E402

ROOT_ALLOW = {"README.md", "CORE.md", "THEORY.md", "LICENSE.md"}
EXTRA = ["formal/lean/README.md", "applications/README.md"]
LIVE_GLOBS = ["*.md", "process/*.md"]
# Append-only logs and dated-note ledgers: they cite past commits on purpose.
SKIP = {"process/FAILURES.md", "measurement/CLAIM_MAP_v2.md"}
RECENT = 50
SHA = r"`?[0-9a-f]{7,40}\b`?"
HEX = re.compile(r"(?<![0-9A-Za-z/#])([0-9a-f]{7,40})(?![0-9A-Za-z])")
MERGED_AS = re.compile(r"merged\s+as\s*`?$", re.I)
# "on/beside `main` `SHA`" is a pointer only in an As-of header; table rows use the words historically.
ASOF = re.compile(r"^\*\*As of:\*\*.*(?:\n(?!\n|#|\|).*)*", re.M)
ASOF_SHA = re.compile(r"(?:on|beside)\s+`main`\s+`[0-9a-f]{7,40}`", re.I)
RULES = [
    ("main SHA pointer", re.compile(
        r"`main`\s+is\s+" + SHA + r"|\bmain\s+is\s+" + SHA
        + r"|current to\s+`?\bmain\b`?\s+" + SHA
        + r"|\b(?:current|latest)\s+`?(?:main|merge|head)`?\s*(?:is|:)?\s*" + SHA
        + r"|\bas\s+of\s+`?(?:main|head)`?\s*(?:is|at|:)?\s*" + SHA
        + r"|\bHEAD\s+(?:is|at|:)\s*" + SHA, re.I)),
    ("open-PR list", re.compile(r"\bopen\s+(?:upstream\s+|fork\s+)?(?:PRs?|pull requests?)\b[^.\n]{0,40}?:\s*(?:PR\s*)?#\d+", re.I)),
    ("PR head", re.compile(r"\bhead\s+`[0-9a-f]{7,40}`|\bPR\s*#\d+\s*\(head\b", re.I)),
    ("version string", re.compile(r"`?THEORY(?:\.md)?`?\s*\(?v\d+\.\d+(?:\.\d+)?[a-z]?\s+draft|`THEORY\.md`\s+v\d+\.\d+"
                                  r"|CLAIM_MAP_v2\.md`?\s*\(v2\.\d+|\(v\d+\.\d+(?:\.\d+)?[a-z]?\s+draft\)")),
    ("Lean total", re.compile(r"\*\*\d[\d,]*\s+declarations\*\*|machine-checks\s+\**\d[\d,]*", re.I)),
]
# Copies in files that may not be edited here; check_consistency.py keeps them equal to their source.
ALLOW = {
    ("CORE.md", "is the canonical statement (v"),
    ("THEORY.md", "Claim statuses: `measurement/CLAIM_MAP_v2.md` (v"),
}
HIST = re.compile(r"<!-- history:begin.*?<!-- history:end -->", re.S)


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def live_pages(root):
    pages = [p for p in list(MAINTAINED_DOCS) + EXTRA if os.path.isfile(os.path.join(root, p))]
    for g in LIVE_GLOBS:
        pages += sorted(os.path.relpath(p, root) for p in glob.glob(os.path.join(root, g)))
    seen, out = set(), []
    for p in pages:
        if p not in seen and p not in SKIP:
            seen.add(p)
            out.append(p)
    return out


def recent_main(root, n=RECENT):
    """Full SHAs of the last n first-parent commits of main (empty without git)."""
    for ref in ("origin/main", "upstream/main", "main", "HEAD"):
        try:
            r = subprocess.run(["git", "-C", root, "rev-list", "--first-parent", "-n", str(n), ref],
                               capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return []
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.split()
    return []


def hand_pointers(text, path="", recent=()):
    """[(line number, rule, excerpt)] for hand-kept live facts in text."""
    text = HIST.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        allowed = any(path == p and frag in line for p, frag in ALLOW)
        hit = False
        for name, rx in RULES:
            m = rx.search(line)
            if not m or allowed:
                continue
            if name == "main SHA pointer" and MERGED_AS.search(line[:m.start()]):
                continue
            hit = True
            out.append((i, name, line[max(0, m.start() - 30):m.end() + 30].strip()))
        if hit or allowed or not recent:
            continue
        for m in HEX.finditer(line):
            tok = m.group(1)
            if MERGED_AS.search(line[:m.start()]):
                continue
            if any(full.startswith(tok) for full in recent):
                out.append((i, "recent main SHA", line[max(0, m.start() - 30):m.end() + 30].strip()))
                break
    for para in ASOF.finditer(text):
        for m in ASOF_SHA.finditer(para.group(0)):
            out.append((text.count("\n", 0, para.start() + m.start()) + 1, "main SHA pointer", m.group(0)))
    return sorted(set(out))


def stray_root_pages(root):
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "*.md"))
                  if os.path.basename(p) not in ROOT_ALLOW)


def check(root=None, recent=None):
    root = root or repo_root()
    recent = recent_main(root) if recent is None else list(recent)
    fails = []
    for p in stray_root_pages(root):
        fails.append("root page %s is not in the allow-list %s; status and open work live in README.md"
                     % (p, sorted(ROOT_ALLOW)))
    for p in live_pages(root):
        with open(os.path.join(root, p), encoding="utf-8") as fh:
            for ln, name, ex in hand_pointers(fh.read(), p, recent):
                fails.append("hand pointer (%s) at %s:%d: %s; read it live or from its one source" % (name, p, ln, ex))
    return fails


def main(argv=None):
    argv = sys.argv if argv is None else argv
    fails = check(argv[1] if len(argv) > 1 else None)
    for f in fails:
        print("  FAIL " + f)
    print("RESULT:", "FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
