"""Verify every DOI cited in theory/ROBUSTNESS.md against Crossref (network needed).
Writes crossref.out. Not run by pytest (network)."""
import json, urllib.request, urllib.parse, sys
DOIS = [
 "10.1287/mnsc.6.1.73", "10.1287/moor.23.4.769", "10.1287/opre.51.4.543.16101",
 "10.1007/s10957-006-9084-x", "10.1137/050622328", "10.1287/opre.1090.0741",
 "10.1257/aer.91.2.60", "10.1016/0304-4068(89)90018-9", "10.1103/PhysRevE.60.1412",
 "10.1073/pnas.012582499", "10.1038/nrg1471", "10.1073/pnas.231499798",
 "10.1016/0167-6687(91)90023-Q", "10.1287/mnsc.38.11.1562", "10.1109/24.877336",
 "10.1016/0169-5347(89)90138-9", "10.1137/1.9781611971194", "10.1515/9781400831050",
]
out = []
for d in DOIS:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(d)
    try:
        m = json.load(urllib.request.urlopen(url, timeout=30))["message"]
        a = ", ".join(x.get("family", "") for x in m.get("author", [])[:4])
        y = (m.get("issued", {}).get("date-parts") or [[0]])[0][0]
        line = "%s | OK | %s | %s | %s | %s" % (d, (m.get("title") or [""])[0][:100], a, y, (m.get("container-title") or [""])[0][:50])
    except Exception as e:
        line = "%s | NOT FOUND (%s)" % (d, e)
    print(line); out.append(line)
open("crossref.out", "w").write("\n".join(out) + "\n")
