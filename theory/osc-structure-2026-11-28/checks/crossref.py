"""DOI lookup on Crossref for the prior art cited in this folder. No derivation or computation on the scored questions."""
import json, sys, time, urllib.request
DOIS = """10.1115/1.3653115
10.1109/TAC.1978.1101812
10.1112/jlms/s1-25.3.226
10.1111/j.1749-6632.1948.tb39854.x
10.1126/science.267326
10.1080/17442509208833780
10.1016/0005-1098(76)90006-6
10.1115/1.3658902
10.1287/opre.38.6.947
10.1073/pnas.6.7.410
10.1038/118558a0
10.1126/science.177.4052.900
10.1086/282272
10.1103/PhysRevLett.94.218102
10.1038/nphys3412
10.1103/PhysRev.150.1079
10.1103/PhysRev.96.1124
10.1080/17442508208833228
10.1103/PhysRevLett.95.200201
10.2307/1927758
10.2307/2225740
10.1137/0315046
10.1038/nrm2530
10.1119/1.2710480
10.1103/PhysRevLett.114.158101
10.1109/TAC.1976.1101236""".split()
for d in DOIS:
    time.sleep(1.5)
    try:
        with urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+d, headers={"User-Agent":"gtao-crossref (mailto:chad39@gmail.com)"}), timeout=20) as r:
            m = json.load(r)["message"]
        a = m.get("author") or [{}]
        yr = (m.get("issued",{}).get("date-parts") or [[None]])[0][0]
        print(f"OK  {d} | {a[0].get('family','?')} {yr} | {(m.get('title') or ['?'])[0][:90]} | {(m.get('container-title') or ['?'])[0][:40]}")
    except Exception as e:
        print(f"ERR {d} | {e}")
