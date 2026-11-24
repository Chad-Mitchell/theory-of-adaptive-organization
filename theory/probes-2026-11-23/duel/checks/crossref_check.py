import json, urllib.request, time
DOIS = """10.1103/PRXQuantum.3.010319
10.1103/PhysRevE.95.062409
10.1103/PhysRevLett.131.077101
10.1119/1.12061
10.1103/PhysRev.109.571
10.1103/PhysRevLett.82.2207
10.1103/PhysRevA.86.012103
10.1103/PhysRevA.75.032110
10.1038/s41534-018-0064-4
10.1103/PhysRevLett.125.260501
10.1038/ncomms1761
10.1112/S002557931100132X
10.1088/1367-2630/13/6/063024
10.1103/PhysRevA.39.1665
10.1103/PhysRevX.7.031022
10.1515/crll.1916.146.53
10.1007/978-88-7642-378-9
10.1088/1367-2630/13/6/063001
10.1103/PhysRevA.84.012311
10.1073/pnas.1304884110
10.1088/1367-2630/15/5/053040
10.1103/PhysRevA.24.2889""".split()
for doi in DOIS:
    try:
        req = urllib.request.Request('https://api.crossref.org/works/'+doi, headers={'User-Agent':'gtao-duel (mailto:chad39@gmail.com)'})
        m = json.load(urllib.request.urlopen(req, timeout=30))['message']
        au = ','.join(a.get('family','?') for a in m.get('author',[])[:4])
        yr = (m.get('issued',{}).get('date-parts') or [[None]])[0][0]
        print('OK ', doi, '|', yr, '|', au, '|', (m.get('title') or ['?'])[0][:90], '|', (m.get('container-title') or [''])[0][:40], m.get('volume',''), m.get('page',''))
    except Exception as e:
        print('ERR', doi, e)
    time.sleep(0.3)
