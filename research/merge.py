"""Merge hand-written editorial (research/editorial/<slug>.json) with scraped Amazon data
(research/prod-all.json) into data/pages/<slug>.json.

Price, rating, review count, "bought" line, full title, and image always come from the
scrape, never from the editorial file. Usage: python merge.py <slug> [<slug> ...]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCRAPE = {**json.loads((HERE / "prod-all.json").read_text(encoding="utf-8")),
          **json.loads((HERE / "prod-hubs.json").read_text(encoding="utf-8"))}
OUT = HERE.parent / "data" / "pages"


def num(s, cast=float):
    if not s:
        return None
    m = re.search(r"[\d,]+(?:\.\d+)?", s)
    return cast(m.group(0).replace(",", "")) if m else None


def live(asin):
    d = SCRAPE.get(asin)
    if not d or not d.get("title"):
        raise SystemExit(f"{asin}: no scraped product page")
    price, rating, reviews = num(d["price"]), num(d["rating"]), num(d["reviews"], int)
    if price is None or rating is None or reviews is None:
        raise SystemExit(f"{asin}: missing price/rating/reviews in scrape: {d['price']} {d['rating']} {d['reviews']}")
    bought = d.get("bought")
    if bought:
        m = re.search(r"([\d.,]+K?\+?) bought", bought)
        bought = f"{m.group(1)} bought in past month" if m else None
    return {"name": re.sub(r"\s+", " ", d["title"]).strip(), "image": d["image"], "price": price,
            "rating": rating, "reviews_count": reviews, "bought": bought}


def merge(slug):
    import meta
    ed = json.loads((HERE / "editorial" / f"{slug}.json").read_text(encoding="utf-8"))
    m = meta.PAGES[slug]
    ed = {"slug": slug, **meta.COMMON, **{k: m[k] for k in ("title", "subtitle", "intro", "reviews_ceiling")},
          **ed,
          "buyers_guide": [meta.SHARED[g] if isinstance(g, str) else g for g in m["guide"]]}
    for group in ("products", "avoid"):
        for p in ed[group]:
            name_override = p.pop("name", None)
            p.update(live(p["asin"]))
            if name_override:
                p["name"] = name_override
    asins = {p["asin"] for p in ed["products"]}
    for a in ed["awards"]:
        assert a["asin"] in asins, f"{slug}: award {a['label']} points at {a['asin']} not in products"
    for p in ed["products"]:
        missing = set(ed["feature_weights"]) - set(p["features"])
        assert not missing, f"{slug}: {p['asin']} missing features {missing}"
    assert 1 <= len(ed["products"]) <= 10 and len(ed["avoid"]) <= 1, slug
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{slug}.json").write_text(json.dumps(ed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{slug}: {len(ed['products'])} products, {len(ed['avoid'])} avoid")


def merge_systems():
    ed = json.loads((HERE / "editorial" / "systems.json").read_text(encoding="utf-8"))
    for s in ed["systems"]:
        for item in (s, s.get("addon")):
            if item and item.get("asin"):
                d = live(item["asin"])
                item.update(price=d["price"], rating=d["rating"], reviews_count=d["reviews_count"])
    ed["data_captured"] = "2026-10-04"
    (OUT.parent / "systems.json").write_text(json.dumps(ed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"systems: {len(ed['systems'])}")


for s in sys.argv[1:]:
    merge_systems() if s == "systems" else merge(s)
