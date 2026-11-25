#!/usr/bin/env python3
"""Pending-work and pointer check for the GTAO repository.

Added 24 November 2026 after a process miss: reviewed Lean batches sat
unmerged on the fork while STATUS.md still printed the old Lean total and
every existing check passed (check_fresh.py only compares STATUS.md with
main; nothing looked at the Lean count or at open, reviewed PRs).

Checks
  (a) pointers: STATUS.md's `main` is `SHA` is among the last
      check_fresh.WINDOW first-parent commits of main, and OPEN_WORK.md's
      header names a main SHA among the last OPEN_WORK_WINDOW.
  (b) Lean count: formal/lean/AUDIT.json records the AxiomAudit count and a
      sha256 of the Lean sources (GTAO.lean, GTAO/*.lean, the audit script,
      lakefile and toolchain pins). The sources must still hash to the
      recorded value (otherwise rerun tools/check_lean.sh in /tmp/gtao-lean
      and record the new count with --record-audit N), and STATUS.md's
      "**N declarations**" must equal the recorded count.
  (c) pending reviewed work (network): every open PR on the upstream repo
      and the fork that has a passing independent review (a review record
      or comment with "Blockers remaining: 0") older than PENDING_HOURS is
      listed and fails the check. No network, no gh, or an API error: (c)
      is skipped with a WARN line and does not fail.

Run from the repo root:
  python3 tools/check_pending.py              # (a), (b), (c)
  python3 tools/check_pending.py --offline    # (a), (b) only
  python3 tools/check_pending.py --record-audit 1185
Exit 0 = PASS, 1 = FAIL.
"""
from __future__ import annotations

import base64
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_fresh as fresh  # noqa: E402

UPSTREAM = "Chad-Mitchell/theory-of-adaptive-organization"
FORK = "mitchell-moving/theory-of-adaptive-organization"
PENDING_HOURS = 24
OPEN_WORK_WINDOW = 10
AUDIT_FILE = os.path.join("formal", "lean", "AUDIT.json")

OPEN_WORK_MAIN_RE = re.compile(r"on\s+`main`\s+`([0-9a-f]{7,40})`", re.I)
STATUS_LEAN_RE = re.compile(r"\*\*(\d[\d,]*)\s+declarations\*\*")
BLOCKERS_RE = re.compile(r"Blockers remaining:\s*(\d+)", re.I)
REVIEWED_HEAD_RE = re.compile(r"(?:Reviewed head|^Head|^Re-check of head)\s+`([0-9a-f]{7,40})`", re.I | re.M)
REVIEW_TITLE_RE = re.compile(r"\breview\b", re.I)


def repo_root():
    return os.path.dirname(HERE)


# ------------------------------------------------------------------ (a)
def check_pointers(root):
    fails = list(fresh.check(root))
    path = os.path.join(root, "OPEN_WORK.md")
    if not os.path.exists(path) or not fresh.is_git_repo(root):
        return fails
    head = "\n".join(open(path, encoding="utf-8").read().split("\n")[:5])
    m = OPEN_WORK_MAIN_RE.search(head)
    if not m:
        fails.append("pending: OPEN_WORK.md header has no 'on `main` `SHA`' pointer")
        return fails
    full = fresh.expand_sha(root, m.group(1))
    if not full:
        fails.append("pending: OPEN_WORK.md main SHA %s is not a commit in this repo" % m.group(1))
        return fails
    window = fresh.first_parent_window(root, fresh.history_tip(root), OPEN_WORK_WINDOW)
    if full not in window:
        fails.append(
            "pending: OPEN_WORK.md header names main %s, not among the last %d first-parent commits"
            % (m.group(1), OPEN_WORK_WINDOW))
    return fails


# ------------------------------------------------------------------ (b)
def lean_source_files(root):
    lean = os.path.join(root, "formal", "lean")
    files = [os.path.join(lean, "GTAO.lean")]
    files += sorted(glob.glob(os.path.join(lean, "GTAO", "*.lean")))
    for extra in ("scripts/AxiomAudit.lean", "lakefile.toml", "lake-manifest.json", "lean-toolchain"):
        files.append(os.path.join(lean, extra))
    return [f for f in files if os.path.exists(f)]


def lean_sources_sha256(root):
    h = hashlib.sha256()
    for f in lean_source_files(root):
        rel = os.path.relpath(f, root).replace(os.sep, "/")
        h.update(rel.encode() + b"\0")
        h.update(open(f, "rb").read())
        h.update(b"\0")
    return h.hexdigest()


def status_lean_count(text):
    m = STATUS_LEAN_RE.search(text)
    return int(m.group(1).replace(",", "")) if m else None


def check_lean(root):
    lean_dir = os.path.join(root, "formal", "lean")
    if not os.path.exists(os.path.join(lean_dir, "GTAO.lean")):
        return []
    path = os.path.join(root, AUDIT_FILE)
    if not os.path.exists(path):
        return ["lean: %s is missing; run tools/check_lean.sh, then --record-audit N" % AUDIT_FILE]
    audit = json.load(open(path, encoding="utf-8"))
    fails = []
    now = lean_sources_sha256(root)
    if audit.get("sources_sha256") != now:
        fails.append(
            "lean: Lean sources changed since the recorded audit (%s); rerun tools/check_lean.sh in "
            "/tmp/gtao-lean and record the count with: python3 tools/check_pending.py --record-audit N"
            % audit.get("audited_at", "?"))
    status = os.path.join(root, "STATUS.md")
    if os.path.exists(status):
        n = status_lean_count(open(status, encoding="utf-8").read())
        if n is None:
            fails.append("lean: STATUS.md has no '**N declarations**' Lean total")
        elif n != audit.get("audit_count"):
            fails.append("lean: STATUS.md says %d declarations; the recorded AxiomAudit count is %s"
                         % (n, audit.get("audit_count")))
    return fails


def record_audit(root, count, commit=None):
    data = {
        "audit_count": int(count),
        "sources_sha256": lean_sources_sha256(root),
        "audited_at": commit or (fresh.git(root, "rev-parse", "--short", "HEAD").stdout.strip() or "?"),
        "how": "tools/check_lean.sh in /tmp/gtao-lean; AxiomAudit 'N GTAO declarations'",
    }
    with open(os.path.join(root, AUDIT_FILE), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    return data


# ------------------------------------------------------------------ (c)
class Offline(Exception):
    pass


def gh_api(path):
    if not shutil.which("gh"):
        raise Offline("gh not installed")
    r = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github+json", path],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise Offline((r.stderr or r.stdout).strip()[:200])
    return json.loads(r.stdout or "null")


def parse_time(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def review_result(text):
    """(blockers, reviewed_head) from the last 'Blockers remaining' in a review text."""
    found = BLOCKERS_RE.findall(text or "")
    if not found:
        return None, None
    m = REVIEWED_HEAD_RE.search(text)
    return int(found[-1]), (m.group(1) if m else None)


def pending_items(api=gh_api, now=None, hours=PENDING_HOURS):
    """Open work PRs with a passing review older than `hours`.

    A review counts when it is (1) a PR whose title says review, opened
    against the work PR's head branch, whose added review file ends with
    "Blockers remaining: N", or (2) a comment on the work PR with that line.
    The latest such review governs: the item is pending when it says 0.
    """
    now = now or datetime.now(timezone.utc)
    prs = {}
    for repo in (UPSTREAM, FORK):
        for p in api("/repos/%s/pulls?state=open&per_page=100" % repo) or []:
            prs[(repo, p["number"])] = p
    work = {k: p for k, p in prs.items() if not REVIEW_TITLE_RE.search(p["title"])}
    reviews = {k: p for k, p in prs.items() if REVIEW_TITLE_RE.search(p["title"])}
    seen = {}  # work key -> list of (time, where, blockers, reviewed_head)

    def targets(owner, branch):
        return [k for k, p in work.items()
                if p["head"]["ref"] == branch and p["head"]["repo"] and p["head"]["repo"]["owner"]["login"] == owner]

    for (repo, n), r in reviews.items():
        owner = r["base"]["repo"]["owner"]["login"]
        tgt = targets(owner, r["base"]["ref"])
        if not tgt:
            continue
        files = api("/repos/%s/pulls/%d/files?per_page=100" % (repo, n)) or []
        for f in files:
            if not re.search(r"review", f["filename"], re.I) or f.get("status") != "added":
                continue
            c = api("/repos/%s/contents/%s?ref=%s" % (r["head"]["repo"]["full_name"], f["filename"], r["head"]["sha"]))
            text = base64.b64decode(c.get("content", "")).decode("utf-8", "replace")
            b, head = review_result(text)
            if b is not None:
                for k in tgt:
                    seen.setdefault(k, []).append((parse_time(r["created_at"]), "%s#%d" % (repo, n), b, head))
    for (repo, n), p in work.items():
        for c in api("/repos/%s/issues/%d/comments?per_page=100" % (repo, n)) or []:
            b, head = review_result(c.get("body", ""))
            if b is not None:
                seen.setdefault((repo, n), []).append((parse_time(c["created_at"]), c.get("html_url", ""), b, head))
    out = []
    for k, revs in seen.items():
        t, where, b, head = max(revs)  # the latest review governs
        if b == 0 and now - t > timedelta(hours=hours):
            p = work[k]
            cur = p["head"]["sha"]
            stale = head and not cur.startswith(head[:7])
            out.append("%s#%d (%s) head %s: passing review %s at %s, %.0f h ago%s" % (
                k[0], k[1], p["title"][:70], cur[:7], where, head[:7] if head else "?",
                (now - t).total_seconds() / 3600, "; head moved since that review" if stale else ""))
    return sorted(out)


def check_pending_work(api=gh_api):
    try:
        items = pending_items(api)
    except Offline as e:
        return [], ["WARN pending: skipped the open-PR check (%s)" % e]
    except Exception as e:  # network or API shape problem: never fail the offline checks
        return [], ["WARN pending: skipped the open-PR check (%s: %s)" % (type(e).__name__, e)]
    return ["pending: reviewed but unmerged > %dh: %s" % (PENDING_HOURS, x) for x in items], []


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    root = repo_root()
    if "--record-audit" in argv:
        n = argv[argv.index("--record-audit") + 1]
        d = record_audit(root, n)
        print("recorded %s" % json.dumps(d))
        return 0
    fails, warns = [], []
    fails += check_pointers(root)
    fails += check_lean(root)
    if "--offline" not in argv:
        f, w = check_pending_work()
        fails += f
        warns += w
    for w in warns:
        print("  " + w)
    for f in fails:
        print("  FAIL " + f)
    print("RESULT:", "PASS" if not fails else "FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
