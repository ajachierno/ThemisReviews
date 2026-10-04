"""Compact view of scraped products: price/rating/reviews/bought/seller + first bullets (trimmed)."""
import json, sys
d = json.load(open("prod-all.json", encoding="utf-8"))
n = int(sys.argv[1]) if sys.argv[1].isdigit() else 3
for a in sys.argv[2:] if sys.argv[1].isdigit() else sys.argv[1:]:
    v = d.get(a) or {}
    if not v.get("title"):
        print(f"## {a}: NOT SCRAPED"); continue
    seller = (v.get("seller") or "")[:22]; av = (v.get("availability") or "").split("{")[0].strip()[:28]
    print(f"## {a} | {v['price']} | {(v['rating'] or '')[:3]} | {v['reviews']} | {v.get('bought') or ''} | {seller} | {av}")
    print("   ", v["title"][:150])
    for b in v["bullets"][:n]: print("    -", b[:185])
