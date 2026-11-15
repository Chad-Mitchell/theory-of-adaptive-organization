import json,urllib.request,urllib.parse,time,sys
dois=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out=open(sys.argv[2],'a')
for d in dois:
    for k in range(5):
        try:
            u='https://api.crossref.org/works/'+urllib.parse.quote(d)
            r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'litcheck/1.0 (mailto:box@example.com)'}),timeout=30))['message']
            t=(r.get('title') or [''])[0][:90]; j=(r.get('container-title') or [''])[0][:40]
            y=(r.get('issued',{}).get('date-parts') or [[None]])[0][0]
            a=','.join(x.get('family','') for x in r.get('author',[])[:3])
            s=f"OK  {d} | {y} | {a} | {t} | {j} | v{r.get('volume','')} p{r.get('page','')}";break
        except Exception as e:
            s=f"ERR {d} {e}"
            if '404' in str(e): break
            time.sleep(3*(k+1))
    out.write(s+'\n'); out.flush(); time.sleep(1.2)
