"""check_figures.py: every figure a front page shows is rebuilt from its script and matches the committed image.

A front page (README.md, CORE.md) that shows `![...](figures/NAME.png)` needs `figures/NAME.py` beside it. The check
copies the figure folders to a temporary folder (the rest of the tree linked), deletes the image there, runs the script (nice 19), and compares the
rebuilt image with the committed one: bytes first, then pixels. A hand-edited or stale image fails (R1: a figure is a
generated copy of its script). The temporary folder is deleted.

  python3 tools/check_figures.py [ROOT]
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["README.md", "CORE.md"]
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+\.png)\)")
TIMEOUT = 600


def shown(root):
    out = []
    for p in PAGES:
        f = os.path.join(root, p)
        if os.path.isfile(f):
            for m in IMAGE.finditer(open(f, encoding="utf-8").read()):
                if m.group(1) not in out:
                    out.append(m.group(1))
    return out


def _tracked(root):
    r = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True, text=True)
    if r.returncode == 0:
        return [x for x in r.stdout.split("\n") if x]
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", ".lake")]
        out += [os.path.relpath(os.path.join(dp, f), root) for f in fn]
    return out


def _same_pixels(a, b):
    try:
        import matplotlib.image as mi
        import numpy as np
    except ImportError:
        return None
    try:
        x, y = mi.imread(a), mi.imread(b)
    except Exception as e:  # a corrupt or non-PNG file is a FAIL, not a crash
        return "unreadable (%s: %s)" % (type(e).__name__, str(e)[:80])
    return x.shape == y.shape and bool(np.array_equal(x, y))


# Runs a figure script and records every text artist on each figure it saves.
RUNNER = """import json, runpy, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.figure as mf
from matplotlib.text import Text
texts = []
_save = mf.Figure.savefig
def _rec(self, *a, **k):
    texts.extend(t.get_text() for t in self.findobj(Text) if t.get_text().strip())
    return _save(self, *a, **k)
mf.Figure.savefig = _rec
sys.argv = [sys.argv[1]]
dump = %r
runpy.run_path(sys.argv[0], run_name="__main__")
json.dump(texts, open(dump, "w", encoding="utf-8"))
"""
PANEL = re.compile(r"^(.+?) \u2022 (GENERAL|WORKED-CLASS-ONLY|SYNTHESIS|CONJECTURE)$|^(GENERAL|WORKED-CLASS-ONLY|SYNTHESIS|CONJECTURE) \u2022 (.+)$")
HYP_START = "The law of adaptive organization"


def text_fails(root, texts):
    """Checks on the words drawn in a figure: banned words; a bare id whose claim has a prefixed headline id; a panel
    label "IDS \u2022 SCOPE" whose headline ids have another scope; a hypothesis line not on README byte for byte."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import banned_words
    import check_claims
    cm = os.path.join(root, "measurement", "CLAIM_MAP_v2.md")
    rows = check_claims.parse_ledger(open(cm, encoding="utf-8").read())[0] if os.path.isfile(cm) else []
    scope = {r["id"]: r.get("scope", "") for r in rows}
    readme = open(os.path.join(root, "README.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(root, "README.md")) else ""
    out = []
    for t in texts:
        flat = " ".join(t.split())
        for w in banned_words.hits(flat):
            out.append("banned word %r in %r" % (w, flat[:80]))
        for bare, twin, _ in check_claims.ambiguous_ids(flat, rows):
            out.append("%r names %s, which is also a different lettered row; write %s" % (flat[:80], bare, twin))
        m = PANEL.match(flat)
        if m:
            ids_part, word = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
            for i in re.findall(r"(?:[A-Z]+-)?[A-Z]{1,3}\d+[a-z]?", ids_part):
                if i in scope and scope[i] != word:
                    out.append("panel label %r: %s has scope %s in the ledger" % (flat, i, scope[i]))
        if flat.startswith(HYP_START) and flat not in readme:
            out.append("hypothesis line %r is not on README.md byte for byte" % flat[:80])
    return out


def check(root=ROOT):
    """(fails, infos)."""
    fails, infos = [], []
    figs = shown(root)
    if not figs:
        return fails, ["no figures shown on the front pages"]
    work = tempfile.mkdtemp(prefix="gtao-figures.")
    try:
        # The figure folders are copied (tracked files only); every other top-level entry is linked read-only by
        # path, so a script that reads the rest of the tree finds it and nothing it writes lands in the tree.
        fig_tops = {f.split("/", 1)[0] for f in figs}
        tracked = _tracked(root)
        for top in sorted({rel.split("/", 1)[0] for rel in tracked} - fig_tops):
            os.symlink(os.path.join(root, top), os.path.join(work, top))
        for rel in tracked:
            if rel.split("/", 1)[0] in fig_tops and os.path.isfile(os.path.join(root, rel)):
                dst = os.path.join(work, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(os.path.join(root, rel), dst)
        for png in figs:
            script = png[:-4] + ".py"
            if not os.path.isfile(os.path.join(root, png)):
                fails.append("figure %s is shown on a front page but missing" % png)
                continue
            if not os.path.isfile(os.path.join(root, script)):
                fails.append("figure %s has no script %s to rebuild it" % (png, script))
                continue
            out = os.path.join(work, png)
            if os.path.exists(out):
                os.remove(out)
            dump = os.path.join(work, ".figure_text.json")
            with open(os.path.join(work, ".figure_text_runner.py"), "w") as fh:
                fh.write(RUNNER % dump)
            r = subprocess.run(["nice", "-n", "19", sys.executable, ".figure_text_runner.py", script, dump], cwd=work, capture_output=True,
                               text=True, timeout=TIMEOUT, env=dict(os.environ, MPLBACKEND="Agg"))
            if r.returncode != 0 or not os.path.isfile(out):
                fails.append("figure %s: %s did not rebuild it (exit %d): %s"
                             % (png, script, r.returncode, (r.stderr or r.stdout).strip()[-200:]))
                continue
            texts = json.load(open(dump, encoding="utf-8")) if os.path.isfile(dump) else []
            if not texts:
                fails.append("figure %s: no drawn text captured from %s" % (png, script))
            fails.extend("figure %s text: %s" % (png, x) for x in text_fails(root, texts))
            if open(out, "rb").read() == open(os.path.join(root, png), "rb").read():
                infos.append("figure %s: rebuilt from %s, byte-identical" % (png, script))
                continue
            same = _same_pixels(out, os.path.join(root, png))
            if isinstance(same, str):
                fails.append("figure %s: the committed or rebuilt image is %s" % (png, same))
            elif same:
                infos.append("figure %s: rebuilt from %s, same pixels (metadata differs)" % (png, script))
            elif same is None:
                fails.append("figure %s: rebuilt image differs in bytes and pixels could not be compared" % png)
            else:
                fails.append("figure %s does not match a rebuild from %s; run the script and commit its output" % (png, script))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return fails, infos


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    root = argv[0] if argv else ROOT
    fails, infos = check(root)
    for x in infos:
        print("  " + x)
    for x in fails:
        print("  FAIL " + x)
    print("figures: %d shown; RESULT: %s" % (len(shown(root)), "FAIL" if fails else "PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
