#!/usr/bin/env python3
"""Resolve every DOI cited in theory/swarm-2026-11-27/ on api.crossref.org.

Run from the repo root (needs network):
  nice -n 19 python3 theory/swarm-2026-11-27/checks/crossref_check.py > theory/swarm-2026-11-27/checks/crossref.out
Prints one line per DOI: status, first author family name, year, container,
volume, first page, title. Not run by the test suite (network)."""
import json
import re
import sys
import time
import urllib.request

DOIS = [
    "10.2307/1913390",            # Crawford & Sobel 1982
    "10.2307/1914085",            # Groves 1973
    "10.1007/BF01726210",         # Clarke 1971
    "10.1111/j.1540-6261.1961.tb02789.x",  # Vickrey 1961
    "10.2307/1911219",            # Green & Laffont 1977
    "10.2307/1911954",            # Holmstrom 1979 (restricted domains)
    "10.2307/1912821",            # Laffont & Maskin 1980
    "10.2307/1912822",            # Walker 1980
    "10.1016/0047-2727(79)90043-4",  # d'Aspremont & Gerard-Varet 1979
    "10.2307/2298018",            # Mailath & Postlewaite 1990
    "10.1007/s11229-021-03141-4", # Everitt, Hutter, Kumar & Krakovna 2021
    "10.2307/1925895",            # Samuelson 1954
    "10.1006/game.1996.0044",     # Monderer & Shapley 1996
    "10.1016/S0165-1765(99)00196-2",  # Voorneveld 2000
    "10.1016/j.geb.2004.10.007",  # Dubey, Haimanko & Zapechelnyuk 2006
    "10.1007/s00199-008-0419-8",  # Jensen 2010 (online 2008)
    "10.1016/0047-2727(86)90024-1",  # Bergstrom, Blume & Varian 1986
    "10.1137/0317054",            # Topkis 1979
    "10.2307/2938316",            # Milgrom & Roberts 1990
    "10.1016/0304-4068(90)90005-T",  # Vives 1990
    "10.2140/pjm.1955.5.285",     # Tarski 1955
    "10.1086/226707",             # Granovetter 1978
    "10.2307/134972",             # d'Aspremont, Jacquemin, Gabszewicz & Weymark 1983
    "10.1016/0047-2727(93)90037-T",  # Carraro & Siniscalco 1993
    "10.1093/oep/46.Supplement_1.878",  # Barrett 1994
    "10.1007/BF01753431",         # Shapley 1971
    "10.2307/1911749",            # Rosen 1965
    "10.1103/PhysRevX.4.031015",  # Horowitz & Esposito 2014
    "10.1145/958942.958945",      # Cho & Garcia-Molina 2003
    "10.2307/1927082",            # Olson & Zeckhauser 1966
    "10.1023/A:1017501703105",    # Tseng 2001
]


def main():
    bad = 0
    for doi in DOIS:
        req = urllib.request.Request("https://api.crossref.org/works/" + doi,
                                     headers={"User-Agent": "gtao-doi-check/1.0 (mailto:chad39@gmail.com)"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                m = json.load(r)["message"]
            au = (m.get("author") or [{}])[0].get("family", "?")
            yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
            ct = (m.get("container-title") or ["?"])[0]
            print("OK  %s | %s | %s | %s | vol %s | p %s | %s" % (
                doi, au, yr, ct, m.get("volume", "-"), m.get("page", "-"),
                " ".join(re.sub(r"<[^>]+>", "", (m.get("title") or ["?"])[0]).split())))
        except Exception as e:  # noqa: BLE001
            bad += 1
            print("BAD %s | %s" % (doi, e))
        time.sleep(0.2)
    print("resolved %d of %d" % (len(DOIS) - bad, len(DOIS)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
