"""Print bullets matching keywords: python bul.py ASIN[,ASIN...] [keyword ...]"""
import sys
from scrape_data import load_scrape
d = load_scrape()
kw = [k.lower() for k in sys.argv[2:]] or None
for a in sys.argv[1].split(','):
    p = d.get(a)
    if not p:
        print('##', a, 'NOT SCRAPED'); continue
    print('##', a, p['title'][:120])
    for b in p.get('bullets', []):
        if not kw or any(k in b.lower() for k in kw):
            print('  -', b[:260])
