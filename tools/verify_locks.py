#!/usr/bin/env python3
"""Verify the repository's hash locks and account for every one that does not verify.

Read-only. It never edits a locked file. Added 24 November 2026 (process/LOCK_ERRATA.md).

A lock file is any `*.sha256`, `SHA256SUMS*`, `LOCK*.txt`, `SHA256*.txt` or `*SHA256.txt`. Every 64-hex hash in one is
tied to a file in any format the tree uses: `<hex>  <path>`, `<path>  sha256 <hex>`, a
`sha256: <hex>` line under the path, `<name>_sha256 <hex>` (with `<name>_path`), and a bare
hash in a sidecar named for its file (PREREG.sha256 beside PREREG.md). A hash no format ties to a
file is counted and reported, not dropped. For each pair this script computes the sha256 of the
tracked file and puts it in one class:

  OK          the file hashes to the locked value;
  SCRUB       the file differs only by the public-readiness scrub `d513528`
              (18 November 2026), which replaced box paths: `<local>` stands
              for `/workspace`, `<repo>` for `/workspace/theory-of-adaptive-organization`.
              The script PROVES this by reversing the substitution in memory
              and checking that the locked hash comes back;
  POST_LOCK   the file was changed after the lock, by a commit named in
              process/LOCK_ERRATA.md. With git history the script finds the
              lock-time blob and confirms it hashes to the locked value;
  UNVERIFIABLE no committed version, with or without the reverse
              substitution, hashes to the locked value;
  MISSING     the locked file is raw external data that was never committed.

The expected members of every class except OK are pinned below, and the current
git blob of each file that no lock covers (stores.py, F1 outcome.py, glucose
analyze.py) is pinned too, so a later edit to one of them fails. The script
fails if a lock stops verifying that is not pinned, if a pinned SCRUB file no
longer reverses, or if a count changes. New locks that verify (OK) are free.

Prose quotes of hashes in reviews and worklogs are not locks and are not scanned. A file that
changed or never matched needs a record that names it (process/LOCK_ERRATA.md, or DECLARED_IN).
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import movemap  # noqa: E402  the one move map: lock lines and pins resolve across the 27 Nov layout move

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK_FILE_RE = re.compile(r"(\.sha256|SHA256SUMS[^/]*|LOCK[^/]*\.txt|SHA256[^/]*\.txt|[^/]*SHA256\.txt)$")
LINE_RE = re.compile(r"^\s*([0-9a-f]{64})\s+\*?(\S.*?)\s*$")
SKIP_DIRS = {".git", ".lake", "lake-packages", "node_modules", "__pycache__"}

SCRUB_MAP = ((b"<repo>", b"/workspace/theory-of-adaptive-organization"), (b"<local>", b"/workspace"))

# Pinned: files whose lock verifies only after reversing the scrub (13).
SCRUB = {
    "prereg/WIKIDATA-BAND/PREREG.md", "prereg/vigil-ona/ona_analyze.py",
    "tests/C3b/PREREG_ADDENDUM_A2.md", "tests/C3b/PREREG_ADDENDUM_A3.md",
    "tests/DECISIVE/banks/PREREG.md",
    "tests/F1/code/analyze.py", "tests/F1/code/analyze_E.py", "tests/F1/code/build_dataset.py",
    "tests/F1/code/covid.py", "tests/F1/code/extract.py", "tests/F1/code/measures.py",
    "tests/F1/code/power.py", "tests/F1/code/sim_dataset.py",
}
# Pinned: changed after the lock. path -> (lock-time commit, lock-time blob, later commit, later blob)
POST_LOCK = {
    "night2/GITHUB/code/pull.py": ("86aa1cc", "44563ed734645b4a9ca649b99663b898897ed4fc", "d9152f2", "ee4f718e0f63121508916eab14d979e9c09b0fe6"),
    "theory/layers_checks/stores.py": ("e50e92f", "c7c1e06bc098e40c2395ef94b4d1a953243a020a", "a1a98aa", "71a113e05eab9f62b70cedbfcf27f0d698bc2f92"),
}
# Pinned: no committed version matches.
UNVERIFIABLE = {"tests/DECISIVE/glucose/code/analyze.py", "tests/F1/code/outcome.py",
                "core/keystone_checks/waterfill_2026-11-20/worlds.py", "theory/measured/ecoli/ecoli_calc.py"}
# Where each file in POST_LOCK or UNVERIFIABLE has its change declared: (record, a string the record must contain).
# Default: process/LOCK_ERRATA.md naming the file. A mismatch with no record that names it fails. The lock-time bytes of
# worlds.py (changed before the official start, D1) and of ecoli_calc.py (the Riccati deviation; its record cites
# commit 6903de9, which is not in this repository) are in no committed version, so they stay UNVERIFIABLE.
DECLARED_IN = {
    "core/keystone_checks/waterfill_2026-11-20/worlds.py": ("core/keystone_checks/waterfill_2026-11-20/DEVIATIONS_2026-11-20.md", "worlds.py"),
    "theory/measured/ecoli/ecoli_calc.py": ("theory/measured/ecoli/DEVIATIONS.md", "arm_a_poles_riccati"),
}
# Pinned: the current git blob of every file whose lock does not verify and whose bytes are not themselves
# locked by another hash. Without this, a later edit to these three files would go unnoticed.
CURRENT_BLOB = {
    "theory/layers_checks/stores.py": "71a113e05eab9f62b70cedbfcf27f0d698bc2f92",
    "tests/F1/code/outcome.py": "3126c5e00f096ce7632f4ea18557fc9b1e734ed5",
    "tests/DECISIVE/glucose/code/analyze.py": "1c9a5051eeb9e058da452ed3a5b86fb0ca4f5e4b",
}
# Pinned: locked files that are raw external data and were never committed, by lock file.
MISSING = {
    "night2/GITHUB/data/SHA256SUMS": 1,
    "prereg/WIKIDATA-BAND/data/SHA256SUMS": 2,
    "prereg/vigil-ona/SHA256SUMS_raw.txt": 30,
    "tests/F1/raw/companyfacts.sha256": 1,
    "tests/F1/raw/submissions.sha256": 1,
    "tests/LFK_SPF/data/RAW_SHA256.txt": 50,
}


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob(b):
    """The git blob id of these bytes (what `git hash-object` prints)."""
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def unscrub(b):
    for a, c in SCRUB_MAP:
        b = b.replace(a, c)
    return b


def lock_files(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if LOCK_FILE_RE.search(f):
                yield os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")


HEX_RE = re.compile(r"(?<![0-9a-fA-F])([0-9a-f]{64})(?![0-9a-fA-F])")
PATH_RE = re.compile(r"[A-Za-z0-9_.\-/]+")


def _resolve(lf, token, root):
    """The tracked file a path token in lock file lf names, or None (as written, root-relative, or across the move)."""
    token = token.strip("`'\"()[]:,*")
    token = token[2:] if token.startswith("./") else token
    if not token:
        return None
    hit = next((c for c in movemap.resolve_lock_line(lf, token) if os.path.isfile(os.path.join(root, c))), None)
    if hit or "." not in os.path.basename(token):
        return hit
    # A lock written from another working tree (`waterfill/worlds.py` for a file now beside the lock): the one file of
    # that name under the lock file's own folder.
    base, here = os.path.basename(token), os.path.dirname(lf)
    found = [os.path.relpath(os.path.join(dp, base), root).replace(os.sep, "/")
             for dp, _dn, fn in os.walk(os.path.join(root, here)) if base in fn]
    return found[0] if len(found) == 1 else None


def _named_for(lf, stem, root, hx):
    """The file in the lock file's folder named for `stem` (PREREG.sha256 beside PREREG.md; a `prereg_sha256` key):
    the one whose hash is the locked value if several share the stem (run_sim1.json, run_sim1.py), else the first."""
    here = os.path.dirname(lf)
    cands = [(here + "/" if here else "") + f for f in sorted(os.listdir(os.path.join(root, here) if here else root))
             if f.split(".")[0].lower() == stem.lower() and not LOCK_FILE_RE.search(f)
             and os.path.isfile(os.path.join(root, here, f))]
    for c in cands:
        if sha256(open(os.path.join(root, c), "rb").read()) == hx:
            return c
    return cands[0] if cands else None


def entries(root):
    """[(lock_file, target_path_or_None, locked_hash, target_rel)] for every hash a lock file ties to a file, in any of
    its formats: `<hex>  <path>`; `<path>  sha256 <hex>`; a path line followed by an indented `sha256: <hex>`; a
    `<name>_sha256 <hex>` key; a bare hash in a sidecar named for its file. A hash no format ties to a file is
    returned with target "?" so the caller can count it; it is never silently dropped."""
    out = []
    for lf in sorted(lock_files(root)):
        lines = open(os.path.join(root, lf), encoding="utf-8", errors="replace").read().splitlines()
        for n, line in enumerate(lines):
            m = LINE_RE.match(line)
            if m:
                hx, p = m.groups()
                p = p[2:] if p.startswith("./") else p
                # As written (relative to the lock file, then root-relative), then against the lock file's folder before
                # the move, mapped forward: a moved lock file keeps lines written relative to where it was.
                cands = movemap.resolve_lock_line(lf, p)
                hit = _resolve(lf, p, root)
                out.append((lf, hit, hx, cands[0]))
                continue
            for hm in HEX_RE.finditer(line):
                hx = hm.group(1)
                before = line[:hm.start()]
                hit = None
                for tok in PATH_RE.findall(before) + PATH_RE.findall(line[hm.end():]):   # `<path>  sha256 <hex>`
                    hit = hit or _resolve(lf, tok, root)
                if hit is None and re.match(r"\s*sha256:?\s*$", before):  # path on the line above
                    for prev in reversed(lines[:n]):
                        if prev.strip():
                            hit = next((h for h in (_resolve(lf, t, root) for t in PATH_RE.findall(prev)) if h), None)
                            break
                if hit is None:                                           # `<name>_sha256 <hex>`
                    k = re.search(r"([A-Za-z0-9]+)_sha256\s*$", before)
                    if k:                                                 # `<name>_path <path>` names the file outright
                        for other in lines:
                            pm = re.match(r"%s_path\s+(\S+)" % re.escape(k.group(1)), other)
                            hit = hit or (_resolve(lf, pm.group(1), root) if pm else None)
                        hit = hit or _named_for(lf, k.group(1), root, hx)
                if hit is None and not before.strip() and len([x for x in lines if HEX_RE.search(x)]) == 1:
                    hit = _named_for(lf, os.path.basename(lf).split(".")[0], root, hx)   # bare hash in a sidecar
                out.append((lf, hit if hit else "?", hx, hit or "?"))
    return out


def commit_matches(pin, names):
    """True if `pin` (a possibly short hash) names one of the commits in `names`."""
    pin = (pin or "").lower()
    return any(c.lower().startswith(pin) or pin.startswith(c.lower()) for c in names if c)


def git_history_sha256(root, path):
    """{commit sha: sha256} for every committed version of path, or None without history."""
    if not os.path.exists(os.path.join(root, ".git")):
        return None
    out = {}
    # The file's history under its present name and, for a moved file, under its name before the move.
    for name in dict.fromkeys((path, movemap.backward(path))):
        r = subprocess.run(["git", "log", "--all", "--format=%H", "--", name], cwd=root, capture_output=True, text=True)
        if r.returncode != 0:
            continue
        for c in r.stdout.split():
            b = subprocess.run(["git", "show", "%s:%s" % (c, name)], cwd=root, capture_output=True)
            if b.returncode == 0:
                out[c] = sha256(b.stdout)
    return out or None


LOCKED_BLOBS = "process/LOCKED_BLOBS.txt"


def frozen_rows(text):
    """{path: blob} for LOCKED_BLOBS rows whose reason starts with `frozen:`."""
    out = {}
    for line in (text or "").splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) == 3 and not parts[0].startswith("#") and re.fullmatch(r"[0-9a-f]{40}", parts[1]) \
                and parts[2].startswith("frozen:"):
            out[parts[0]] = parts[1]
    return out


def base_blob_list(root):
    """LOCKED_BLOBS.txt on origin/main, or None when there is no such ref (a copy without .git)."""
    if not os.path.exists(os.path.join(root, ".git")):
        return None
    r = subprocess.run(["git", "show", "origin/main:" + LOCKED_BLOBS], cwd=root, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def frozen_fails(root, base_text=None):
    """A frozen file must keep the blob in its row, and a frozen row already on origin/main must not change."""
    p = os.path.join(root, LOCKED_BLOBS)
    now = frozen_rows(open(p, encoding="utf-8").read() if os.path.isfile(p) else "")
    fails = []
    for path, blob in sorted(now.items()):
        fp = os.path.join(root, movemap.forward(path) if not os.path.exists(os.path.join(root, path)) else path)
        if not os.path.isfile(fp):
            fails.append("frozen: %s is missing" % path)
        elif git_blob(open(fp, "rb").read()) != blob:
            fails.append("frozen: %s was edited (git blob %s, frozen %s); it is not edited, see process/PROCESS.md" % (
                path, git_blob(open(fp, "rb").read())[:8], blob[:8]))
    for path, blob in sorted(frozen_rows(base_text).items()):
        if now.get(path) != blob:
            fails.append("frozen: the frozen row for %s on origin/main was changed or dropped" % path)
    return fails


def verify(root=ROOT, history=True, scrub=None, post=None, unverifiable=None, missing_pin=None, blobs=None):
    """(fails, counts, notes). The pins default to the module's tables."""
    scrub = SCRUB if scrub is None else scrub
    post = POST_LOCK if post is None else post
    unverifiable = UNVERIFIABLE if unverifiable is None else unverifiable
    missing_pin = MISSING if missing_pin is None else missing_pin
    blobs = CURRENT_BLOB if blobs is None else blobs
    # The pins are keyed by the path before the move. A file found at its moved path is looked up under its old
    # name (movemap.backward), so the same pins hold before and after the move.
    key = movemap.backward
    fails, notes = [], []
    counts = {"OK": 0, "SCRUB": 0, "POST_LOCK": 0, "UNVERIFIABLE": 0, "MISSING": 0}
    missing, unpaired = {}, []
    seen_scrub, seen_post, seen_unv, seen_later = set(), set(), set(), set()
    for lf, hit, hx, target in entries(root):
        if hit == "?":
            unpaired.append("%s: hash %s names no file" % (lf, hx[:12]))
            continue
        if hit is None:
            missing[key(lf)] = missing.get(key(lf), 0) + 1
            counts["MISSING"] += 1
            continue
        b = open(os.path.join(root, hit), "rb").read()
        k = key(hit)
        if k in blobs and k not in scrub and git_blob(b) != blobs[k]:
            fails.append("locks: %s changed since it was pinned (git blob %s, now %s); it is outside every lock, so any edit needs a new entry in process/LOCK_ERRATA.md and here" % (hit, blobs[k][:8], git_blob(b)[:8]))
        # Always check the declared later blob, even when this clone has no lock-time history
        # (B-281-1: a shallow clone must still catch a tamper of pull.py).
        if k in post and k not in seen_later:
            seen_later.add(k)
            want = post[k][3] if len(post[k]) > 3 else None
            if want and git_blob(b) != want:
                fails.append("locks: %s changed since the declared later version (git blob %s, now %s)" % (hit, want[:8], git_blob(b)[:8]))
        if sha256(b) == hx:
            counts["OK"] += 1
        elif k in scrub:
            if sha256(unscrub(b)) == hx:
                counts["SCRUB"] += 1
                seen_scrub.add(k)
            else:
                fails.append("locks: %s was pinned as scrub-only but reversing the substitution no longer gives the locked hash" % hit)
        elif k in post:
            counts["POST_LOCK"] += 1
            seen_post.add(k)
            h = git_history_sha256(root, hit) if history else None
            if h is None:
                notes.append("post-lock history for %s not checked (no git history)" % hit)
            else:
                matching = [c for c, v in h.items() if v == hx]
                if commit_matches(post[k][0], matching):
                    pass
                elif commit_matches(post[k][0], h):
                    fails.append("locks: %s: commit %s is in history but does not hash to the locked value" % (hit, post[k][0]))
                else:
                    notes.append("post-lock history for %s: lock-time commit %s is not in this clone; the erratum in process/LOCK_ERRATA.md still stands" % (hit, post[k][0]))
        elif k in unverifiable:
            counts["UNVERIFIABLE"] += 1
            seen_unv.add(k)
            history_has = history and git_history_sha256(root, hit)
            if history_has and any(v == hx for v in history_has.values()):
                fails.append("locks: %s is pinned unverifiable but a committed version now hashes to the locked value; move it to POST_LOCK" % hit)
        else:
            fails.append("locks: %s (locked in %s) does not match its hash and is not accounted for in process/LOCK_ERRATA.md" % (hit, lf))
    for k in sorted(seen_post | seen_unv):
        rec, needle = DECLARED_IN.get(k, ("process/LOCK_ERRATA.md", os.path.basename(k)))
        rp = next((os.path.join(root, x) for x in (rec, movemap.forward(rec)) if os.path.isfile(os.path.join(root, x))), None)
        if rp is None or needle not in open(rp, encoding="utf-8", errors="replace").read():
            fails.append("locks: %s changed or never matched its lock, and %s does not name it; declare the change there" % (k, rec))
    for name, want, seen in (("scrub-only", set(scrub), seen_scrub), ("post-lock", set(post), seen_post),
                             ("unverifiable", set(unverifiable), seen_unv)):
        for g in sorted(want - seen):
            if any(os.path.isfile(os.path.join(root, x)) for x in (g, movemap.forward(g))):
                fails.append("locks: pinned %s file %s now verifies or lost its lock line; update tools/verify_locks.py and process/LOCK_ERRATA.md" % (name, g))
    if unpaired:
        notes.append("%d hash(es) in lock files name no file and are not verified: %s" % (len(unpaired), "; ".join(unpaired[:6])))
    fails.extend(frozen_fails(root, base_blob_list(root)))
    if missing != missing_pin:
        fails.append("locks: locked-but-uncommitted files changed: pinned %s, found %s" % (missing_pin, missing))
    return fails, counts, notes


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    fails, counts, notes = verify(ROOT)
    print("locks: %(OK)d OK; %(SCRUB)d scrub-only (proved by reversing the substitution); %(POST_LOCK)d changed after the lock (declared); "
          "%(UNVERIFIABLE)d unverifiable; %(MISSING)d raw data never committed" % counts)
    for n in notes:
        print("  note: " + n)
    for f in fails:
        print("  FAIL " + f)
    print("RESULT:", "FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
