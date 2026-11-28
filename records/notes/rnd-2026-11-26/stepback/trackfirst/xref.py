import sys,json,urllib.request,urllib.parse
def get(d):
    try:
        m=json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/"+urllib.parse.quote(d),headers={'User-Agent':'gtao-notes'}),timeout=20))['message']
        a=', '.join(x.get('family','?') for x in m.get('author',[])[:4]); yr=m.get('issued',{}).get('date-parts',[[None]])[0][0]
        return f"OK\t{d}\t{yr}\t{a}\t{(m.get('title') or [''])[0][:100]}\t{(m.get('container-title') or [''])[0][:40]}\t{m.get('volume','')}:{m.get('page','')}"
    except Exception as e: return f"FAIL\t{d}\t{e}"
def search(q,n=4):
    u="https://api.crossref.org/works?rows=%d&query.bibliographic=%s"%(n,urllib.parse.quote(q))
    js=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'gtao-notes'}),timeout=20))['message']['items']
    return [f"  {it.get('DOI')}\t{it.get('issued',{}).get('date-parts',[[None]])[0][0]}\t{[a.get('family') for a in it.get('author',[])][:3]}\t{(it.get('title') or [''])[0][:90]}" for it in js]
if sys.argv[1]=='get':
    for d in sys.argv[2:]: print(get(d))
else:
    for q in sys.argv[2:]:
        print('Q:',q); print('\n'.join(search(q)))
