import json, sys
d = json.load(open('search-batch10.json', encoding='utf-8'))
b = json.load(open('batch10.json'))
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
