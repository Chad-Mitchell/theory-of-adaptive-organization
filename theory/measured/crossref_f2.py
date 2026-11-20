import json, sys, time, urllib.request, urllib.parse
for d in open('dois_f2.txt').read().split():
    u = 'https://api.crossref.org/works/' + urllib.parse.quote(d)
    try:
        m = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'gtao-measure (mailto:chad39@gmail.com)'}), timeout=30))['message']
        au = '; '.join(a.get('family', '') for a in m.get('author', [])[:4])
        yr = (m.get('issued', {}).get('date-parts') or [[None]])[0][0]
        print(f"OK\t{d}\t{yr}\t{au}\t{(m.get('title') or [''])[0][:90]}\t{(m.get('container-title') or [''])[0]}")
    except Exception as e:
        print(f"FAIL\t{d}\t{e}")
    time.sleep(0.3)
