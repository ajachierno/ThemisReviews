import unicodedata,re,sys
from scrape_data import load_scrape
d=load_scrape()
n=int(sys.argv[1])
for a in sys.argv[2:]:
    v=d[a];print('##',a,v.get('price'),(v.get('rating') or '')[:3],v.get('reviews'),(v.get('seller') or '')[:18],'|',v['title'][:95])
    for b in v.get('bullets',[])[:n]: print('  -',unicodedata.normalize('NFKC',re.sub(r'\s+',' ',b))[:n*40])
