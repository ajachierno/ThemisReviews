"""Price pass through the Amazon Creators API (no scraping).

    python -X utf8 research/api_pricepass.py <slug> [<slug>...]

For every listing on those pages it asks the API for price, availability and buy box, then
writes research/refresh/<today>-<slug>.json: the listing's last good capture (title, image,
rating, review count, bought line) with the price and availability replaced by the API's.
The API has no rating or review fields, so those stay as last captured; each record says so
in `rating_captured`. merge.py reads the file like any other refresh capture.

A listing is left out of the file (its previous capture stays in force) and printed as a
FLAG when the API does not return it, returns no price, has no buy-box winner, or returns a
title that no longer matches the captured one. Flags are for a full audit to settle; this
script never removes a pick.
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import creators_api  # noqa: E402
from scrape_data import load_scrape  # noqa: E402
import sales_rank  # noqa: E402
import sellers  # noqa: E402

RANKS = HERE.parent / "data" / "sales-rank.json"
SELLERS = HERE.parent / "data" / "sellers.json"

TODAY = dt.date.today().isoformat()


def words(s):
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def rank_flags(products, recs, today, path=None):
    """Record today's sales ranks in data/sales-rank.json; return {slug: [flag, ...]} for picks
    (products only, never the avoid pick) that are falling behind their page (sales_rank.py)."""
    path = path or RANKS
    hist = sales_rank.update(path, {a: (r.get("cat_rank"), r.get("cat_node"), r.get("site_rank"))
                                    for a, r in recs.items()}, today)
    out = {}
    for slug, asins in products.items():
        line = sales_rank.page_line([(recs.get(a) or {}).get("cat_rank") for a in asins])
        for a in asins:
            hit = sales_rank.slipping(hist, a, line)
            if hit:
                out.setdefault(slug, []).append(
                    f"{a} falling, #{hit[1]:,} in {hit[2]} (best #{sales_rank.best(hist, a):,} in its last "
                    f"{sales_rank.KEEP} checks, page line #{line:,.0f})")
    return out


def seller_flags(products, brands, recs, today, path=None):
    """Record today's buy-box seller in data/sellers.json; return {slug: [flag, ...]} for picks
    (products only) whose buy box flipped away from Amazon or the brand's store (sellers.py)."""
    path = path or SELLERS
    hist = sellers.update(path, {a: (r.get("seller"), r.get("condition")) for a, r in recs.items()}, today)
    out = {}
    for slug, asins in products.items():
        for a in asins:
            hit = sellers.flipped(hist, a, brands.get(a))
            if hit:
                out.setdefault(slug, []).append(f"{a} seller changed, {hit[0]} -> {hit[1]} "
                                                f"on the last {sellers.RUNS} checks")
    return out


def main(slugs):
    last = load_scrape()
    pages, products, brands = {}, {}, {}
    for s in slugs:
        d = json.loads((HERE.parent / "data" / "pages" / f"{s}.json").read_text(encoding="utf-8"))
        pages[s] = [p["asin"] for p in d["products"] + d.get("avoid", [])]
        products[s] = [p["asin"] for p in d["products"]]
        brands.update({p["asin"]: p.get("brand") for p in d["products"] + d.get("avoid", [])})
    asins = list(dict.fromkeys(a for v in pages.values() for a in v))
    items, errs = creators_api.get_items(asins)
    recs = {a: creators_api.record(a, items.get(a)) for a in asins}
    hard = [e for e in errs if "http" in e]
    if hard:
        print("API errors:", json.dumps(hard)[:800])
    flagged = {}
    for s, page_asins in pages.items():
        out, moves = {}, []
        for a in page_asins:
            r, old = recs[a], last.get(a)
            why = None
            if old is None:
                why = "no earlier capture"
            elif r["notfound"]:
                why = "not returned by the API"
            elif not r["price"]:
                why = f"no price ({r['avail']})"
            elif not r["buybox"]:
                why = f"no buy-box winner ({r['avail']})"
            else:
                a_w, o_w = words(r["title"]), words(old.get("title"))
                if len(a_w & o_w) < 0.5 * min(len(a_w), len(o_w)):
                    why = f"title changed: {r['title'][:70]!r}"
            if why:
                flagged.setdefault(s, []).append(f"{a} {why}")
                continue
            new = dict(old)
            if new.get("captured") != TODAY or "rating_captured" not in new:
                new["rating_captured"] = old.get("rating_captured") or old.get("captured")
            new.update(price=r["price"], availability=r["avail"], captured=TODAY,
                       price_source="creators_api")
            if old.get("price") != r["price"]:
                moves.append(f"{a} {old.get('price')} -> {r['price']}")
            out[a] = new
        f = HERE / "refresh" / f"{TODAY}-{s}.json"
        if out:
            f.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{s}: {len(out)} of {len(page_asins)} priced, {len(moves)} moved"
              + (f", {len(flagged[s])} FLAG" if s in flagged else ""))
        for m in moves:
            print("   ", m)
        for x in flagged.get(s, []):
            print("    FLAG", x)
    falling = rank_flags(products, recs, TODAY)
    for s, lines in falling.items():
        for x in lines:
            print(f"{s}: FLAG {x}")
    print(f"Sales ranks recorded in {RANKS.name}; {sum(len(v) for v in falling.values())} falling pick(s)")
    flips = seller_flags(products, brands, recs, TODAY)
    for s, lines in flips.items():
        for x in lines:
            print(f"{s}: FLAG {x}")
    print(f"Buy-box sellers recorded in {SELLERS.name}; {sum(len(v) for v in flips.values())} seller change(s)")
    print(f"\n{len(items)} of {len(asins)} listings returned by the API; "
          f"{sum(len(v) for v in flagged.values())} flagged on {len(flagged)} page(s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1:])
