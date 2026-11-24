import json,sys,urllib.request,urllib.parse
import time
for d in open(sys.argv[1]).read().split():
    time.sleep(3)
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request('https://api.crossref.org/works/'+urllib.parse.quote(d),headers={'User-Agent':'gtao-review (mailto:chad39@gmail.com)'}),timeout=30))['message']
        au='; '.join(a.get('family','?') for a in r.get('author',[])[:5])
        print(f"OK  {d} | {r.get('title',[''])[0][:90]} | {au} | {r.get('container-title',[''])[0] if r.get('container-title') else ''} {r.get('volume','')}:{r.get('page',r.get('article-number',''))} | {r.get('issued',{}).get('date-parts',[[None]])[0][0]}")
    except Exception as e: print('FAIL',d,e)
