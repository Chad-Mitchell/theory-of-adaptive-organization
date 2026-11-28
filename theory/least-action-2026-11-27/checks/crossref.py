"""Look up each cited DOI on Crossref and print title, venue, year (citation check only; no claim is computed here)."""
import json, sys, time, urllib.request
DOIS = [
 "10.1103/PhysRev.91.1505",            # Onsager, Machlup 1953
 "10.1007/BF01609446",                 # Duerr, Bach 1978
 "10.1007/978-3-642-25847-3",          # Freidlin, Wentzell, 3rd ed.
 "10.1090/S0002-9947-1966-0201892-6",  # Schilder 1966
 "10.3934/dcds.2014.34.1533",          # Leonard 2014, Schroedinger problem survey
 "10.1103/PhysRev.150.1079",           # Nelson 1966
 "10.1103/PhysRevD.27.1774",           # Guerra, Morato 1983
 "10.1016/0022-1236(81)90079-3",       # Yasue 1981
 "10.1103/RevModPhys.85.1115",         # Presse et al. 2013, max caliber
 "10.1088/1751-8113/44/22/225303",     # Caticha 2011
 "10.1143/PTPS.130.17",                # Sekimoto 1998
 "10.1088/0034-4885/75/12/126001",     # Seifert 2012
 "10.1103/PhysRevLett.98.108301",      # Schmiedl, Seifert 2007
 "10.1103/PhysRevLett.106.250601",     # Aurell et al. 2011
 "10.1007/s002110050002",              # Benamou, Brenier 2000
 "10.1038/nrn2787",                    # Friston 2010
 "10.1016/j.plrev.2021.11.001",        # Aguilera et al. 2022
 "10.1080/17442508208833228",          # Fleming, Mitter 1982
 "10.1103/PhysRevLett.95.200201",      # Kappen 2005
 "10.1119/1.2710480",                  # Gray, Taylor 2007
 "10.1103/RevModPhys.20.367",          # Feynman 1948
]
for d in DOIS:
    try:
        with urllib.request.urlopen(f"https://api.crossref.org/works/{d}", timeout=20) as r:
            m = json.load(r)["message"]
        a = m.get("author", [{}])
        first = a[0].get("family", "?") if a else "?"
        y = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        print(f"OK   {d} | {first} {y} | {(m.get('title') or ['?'])[0]} | {(m.get('container-title') or [''])[0]}")
    except Exception as e:
        print(f"FAIL {d} | {e}")
    time.sleep(0.3)
