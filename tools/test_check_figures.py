"""Tests for tools/check_figures.py: front-page figures rebuild from their scripts."""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_figures as cf  # noqa: E402

SCRIPT = """import os
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
Image.new("RGB", (4, 4), (10, 20, %d)).save(os.path.join(here, "f.png"))
"""


def _tree(blue=30, committed_blue=30, script=True):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "figures"))
    open(os.path.join(d, "README.md"), "w").write("![f](figures/f.png)\n")
    if script:
        open(os.path.join(d, "figures", "f.py"), "w").write(SCRIPT % blue)
    from PIL import Image
    Image.new("RGB", (4, 4), (10, 20, committed_blue)).save(os.path.join(d, "figures", "f.png"))
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
