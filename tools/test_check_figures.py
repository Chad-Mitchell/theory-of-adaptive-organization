"""Tests for tools/check_figures.py: front-page figures rebuild from their scripts."""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_figures as cf  # noqa: E402

SCRIPT = """import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
fig = plt.figure(figsize=(1, 1))
fig.patch.set_facecolor((10 / 255, 20 / 255, %d / 255))
fig.text(0.5, 0.5, "T42 \\u2022 WORKED-CLASS-ONLY")
fig.savefig(os.path.join(here, "f.png"), dpi=20)
"""


def _tree(blue=30, committed_blue=30, script=True):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "figures"))
    open(os.path.join(d, "README.md"), "w").write("![f](figures/f.png)\n")
    if script:
        open(os.path.join(d, "figures", "f.py"), "w").write(SCRIPT % blue)
    tmp = os.path.join(d, "_build.py")
    open(tmp, "w").write((SCRIPT % committed_blue).replace("here = os.path.dirname(os.path.abspath(__file__))",
                                                           "here = %r" % os.path.join(d, "figures")))
    subprocess.run([sys.executable, tmp], check=True)
    os.remove(tmp)
    subprocess.run(["git", "init", "-q", d], check=True)
    subprocess.run(["git", "-C", d, "add", "."], check=True)
    return d


def test_real_front_page_figures_rebuild():
    fails, infos = cf.check(cf.ROOT)
    assert fails == [] and infos


def test_matching_figure_passes():
    d = _tree()
    fails, _ = cf.check(d)
    shutil.rmtree(d)
    assert fails == []


def test_stale_figure_fails():
    d = _tree(blue=30, committed_blue=99)
    fails, _ = cf.check(d)
    shutil.rmtree(d)
    assert len(fails) == 1 and "does not match a rebuild" in fails[0]


def test_figure_with_no_script_fails():
    d = _tree(script=False)
    fails, _ = cf.check(d)
    shutil.rmtree(d)
    assert len(fails) == 1 and "has no script" in fails[0]


def test_the_check_does_not_touch_the_tree():
    d = _tree(blue=30, committed_blue=99)
    before = open(os.path.join(d, "figures", "f.png"), "rb").read()
    cf.check(d)
    after = open(os.path.join(d, "figures", "f.png"), "rb").read()
    shutil.rmtree(d)
    assert before == after


# ---------------------------------------------------------------- the words drawn in a figure
def test_figure_text_on_the_repo_passes_and_is_captured():
    fails, infos = cf.check(cf.ROOT)
    assert fails == []


def test_a_bare_renamed_id_in_figure_text_fails():
    out = cf.text_fails(cf.ROOT, ["R1: additive price sum (A1\u2013A7)."])
    assert len(out) == 1 and "write REP-R1" in out[0]


def test_a_panel_label_with_the_wrong_scope_fails():
    out = cf.text_fails(cf.ROOT, ["T42 \u2022 GENERAL"])
    assert len(out) == 1 and "T42 has scope WORKED-CLASS-ONLY" in out[0]


def test_a_hypothesis_line_not_on_readme_fails():
    out = cf.text_fails(cf.ROOT, ["The law of adaptive organization (hypothesis): selected systems are optimal."])
    assert len(out) == 1 and "byte for byte" in out[0]


def test_a_banned_word_in_figure_text_fails():
    out = cf.text_fails(cf.ROOT, ["The verdict is in."])
    assert out and all("banned word" in x for x in out)


def test_a_corrupt_committed_png_fails_without_a_crash():
    d = _tree()
    p = os.path.join(d, "figures", "f.png")
    data = bytearray(open(p, "rb").read())
    data[60] ^= 0xFF
    open(p, "wb").write(bytes(data))
    fails, _ = cf.check(d)
    shutil.rmtree(d)
    assert len(fails) == 1 and "unreadable" in fails[0]
