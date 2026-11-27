"""Tests for tools/check_public_units.py (UNITS-PUBLIC-1)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_public_units as cpu  # noqa: E402


def test_block_without_units_fails():
    t = "x <!-- public-formula: post 1 -->\n$$J=a+b$$\nrule <!-- /public-formula -->\n"
    assert any("no 'Units:'" in f for f in cpu.check_text(t, "p.md"))


def test_block_with_units_passes():
    t = "x <!-- public-formula: post 1 -->\n$$J=a+b$$\nrule. Units: a, b are cost per time. <!-- /public-formula -->\n"
    assert cpu.check_text(t, "p.md") == []


def test_unclosed_block_fails():
    t = "<!-- public-formula: post 1 -->\nUnits: x\n"
    assert any("never closed" in f for f in cpu.check_text(t, "p.md"))


def test_units_after_close_does_not_count():
    t = "<!-- public-formula: post -->\n$$J$$\n<!-- /public-formula --> Units: too late\n"
    assert cpu.check_text(t, "p.md")


def test_one_line_block():
    assert cpu.check_text("<!-- public-formula: p --> J = a. Units: a in s. <!-- /public-formula -->", "p.md") == []


def test_unmarked_page_passes():
    assert cpu.check_text("$$J=a+b$$\n", "p.md") == []


def test_repo_passes():
    assert cpu.check(cpu.repo_root()) == []


def test_memory_page_is_marked():
    p = os.path.join(cpu.repo_root(), "applications", "GROK_BOT_MEMORY_2026-11-23.md")
    if not os.path.isfile(p):
        p = os.path.join(cpu.repo_root(), "theory", "applications", "GROK_BOT_MEMORY_2026-11-23.md")
    assert cpu.OPEN.search(open(p, encoding="utf-8").read())
