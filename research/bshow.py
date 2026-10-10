import json, sys
import os
d, b = [], {}
for n in ('10', '10b', '11'):
    if os.path.exists(f'search-batch{n}.json'): d += json.load(open(f'search-batch{n}.json', encoding='utf-8'))
for n in ('10', '11'):
    b.update(json.load(open(f'batch{n}.json')))
for r in d: r['query'] = r['query'].strip()
for slug in sys.argv[1:]:
    print(f"\n##### {slug}")
    seen = set()
    for q in b[slug]['q']:
        for r in d:
            if r['query'] != q or r.get('sponsored') or not r.get('asin') or r['asin'] in seen:
                continue
            seen.add(r['asin'])
            rev = (r.get('reviews') or '').replace(' ratings', '').replace(' rating', '')[:9]
            print(f"{r['asin']} {str(r.get('price') or '-'):>9} {(r.get('rating') or '-')[:3]} {rev:>9} | {r['title'][:105]}")
