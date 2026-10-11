import unicodedata,re,sys
from scrape_data import load_scrape
d=load_scrape()
for a in sys.argv[2:]:
    t=unicodedata.normalize('NFKC',' || '.join(d[a]['bullets']))
    print(a,[t[max(0,m.start()-80):m.end()+140] for m in re.finditer(sys.argv[1],t,re.I)][:4])
