"""X (twitter-text v3) weighted length: weight 1 for code points in [0,4351],[8192,8205],[8208,8223],[8242,8247]; else 2; URLs = 23; NFC."""
import re, sys, unicodedata
R=[(0,4351),(8192,8205),(8208,8223),(8242,8247)]
URL=re.compile(r'https?://\S+|\[LINK\]')
def wlen(t):
    t=unicodedata.normalize('NFC',t); n=0
    for m in URL.finditer(t): n+=23
    t=URL.sub('',t)
    for ch in t:
        cp=ord(ch); n+= 1 if any(a<=cp<=b for a,b in R) else 2
    return n
if __name__=='__main__':
    txt=open(sys.argv[1]).read()
    posts=[p.strip() for p in txt.split('\n---\n')[1:]]
    for p in posts:
        body='\n'.join(p.split('\n')[1:]).strip()
        print(p.split('\n')[0], wlen(body), 'OK' if wlen(body)<=280 else 'OVER')
