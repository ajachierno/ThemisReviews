import re,sys
from scrape_data import load_scrape
d=load_scrape()
pat=sys.argv[1]
for a in sys.argv[2:]:
    v=d.get(a) or {};t=(v.get('title') or '')+' || '+' || '.join(v.get('bullets',[]))
    if not v.get('title'): print(a,'NOT SCRAPED');continue
    h=[t[max(0,x.start()-60):x.end()+60] for x in re.finditer(pat,t,re.I)][:2]
    print(a,'|',' ## '.join(h)[:300] or '-- none')
