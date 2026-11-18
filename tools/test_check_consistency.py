#!/usr/bin/env python3
"""Mutation test for tools/check_consistency.py: plant known errors in a temp
copy of the maintained docs and confirm each one is caught. Exit 0 = every
planted error was detected and the clean copy passes."""
import os, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUTATIONS = [
    ("BRIEF.md", "\n\nN26 OPEN.\n", "N-status"),
    ("README.md", "\n\nGTAO is a universal law of adaptive organization.\n", "law"),
    ("STATUS.md", "\n\nThe MV gates become binding once Chad signs off.\n", "gates-await-sign-off"),
    ("README.md", "\n\nThe MATCH1 measles test passed.\n", "unlabeled field verdict"),
    ("THEORY.md", "\n\nGTAO is a theory of everything.\n", "theory-of-everything"),
    ("STATUS.md", "\n\nThe theory is silent on black holes.\n", "stale-scope"),
    ("BRIEF.md", "\n\nSee CLAIM_MAP N99.\n", "N-ref"),
]
def run(d):
    r = subprocess.run([sys.executable, os.path.join(d, "tools", "check_consistency.py")], cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout
def copy():
    d = tempfile.mkdtemp()
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x != ".git"]
        for f in files:
            if f.endswith((".md", ".py")):
                src = os.path.join(root, f); dst = os.path.join(d, os.path.relpath(src, ROOT))
                os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(src, dst)
    return d
ok = True
d = copy(); rc, out = run(d); shutil.rmtree(d)
print("clean copy:", "PASS" if rc == 0 else "FAIL"); ok &= rc == 0
for f, text, key in MUTATIONS:
    d = copy()
    with open(os.path.join(d, f), "a", encoding="utf-8") as fh: fh.write(text)
    rc, out = run(d); shutil.rmtree(d)
    caught = rc != 0 and key in out
    print("planted %-24s in %-10s -> %s" % (key, f, "caught" if caught else "MISSED")); ok &= caught
# version drift
d = copy(); p = os.path.join(d, "README.md"); s = open(p).read().replace("(v1.4.19 draft", "(v1.4.18 draft"); open(p, "w").write(s)
rc, out = run(d); shutil.rmtree(d); caught = rc != 0 and "versions" in out
print("planted %-24s in %-10s -> %s" % ("stale version pointer", "README.md", "caught" if caught else "MISSED")); ok &= caught
print("RESULT:", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
