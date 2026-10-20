"""Picks-only price pass for the holiday deal pages (themisreviews-holiday-pages skill).

A holiday page shows every live review page's Best Overall and Best Budget. Re-reading every
listing on 160+ pages each day isn't practical, so this re-reads just those award listings:

  python research/holiday_picks.py asins    # list the award ASINs the holiday pages show
  python research/holiday_picks.py scrape   # re-read them into research/refresh/<today>-holiday-picks.json
                                            # (visible Chrome window, ~10 s each; re-run to retry failures)
  python research/holiday_picks.py apply    # write data/holiday-prices.json from today's capture

build.py overlays data/holiday-prices.json on the holiday pages only, with each pick's own
"regular price on <date>". Review pages keep their own numbers and "prices checked" date until
their next refresh (merge.py picks up the newer capture then, newest wins per listing).
Entries that didn't capture keep their previous values and date.
"""
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
TODAY = datetime.date.today().isoformat()
CAPTURE = HERE / "refresh" / f"{TODAY}-holiday-picks.json"
OUT = ROOT / "data" / "holiday-prices.json"
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  same ranking and award logic the holiday pages use


def num(s, cast=float):
    if s in (None, ""):
        return None
    if isinstance(s, (int, float)):
        return cast(s)
    m = re.search(r"[\d,]+(?:\.\d+)?", str(s))
    return cast(m.group(0).replace(",", "")) if m else None


def award_asins():
    site = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
    out = []
    for p in site["protocols"]:
        for s in p["subs"]:
            if not s.get("ready"):
                continue
            cat = json.loads((ROOT / "data" / "pages" / f"{s['slug']}.json").read_text(encoding="utf-8"))
            build.rank_products(cat)
            for x in build.page_overall_budget(cat):
                if x and x["asin"] not in out:
                    out.append(x["asin"])
    return out


def scrape():
    asins = award_asins()
    CAPTURE.parent.mkdir(exist_ok=True)
    print(f"Scraping {len(asins)} award listings into {CAPTURE.name}")
    subprocess.run([sys.executable, "-X", "utf8", str(HERE / "amz.py"), "products", str(CAPTURE), *asins], check=False)


def apply():
    if not CAPTURE.exists():
        sys.exit(f"No capture for today. Run: python research/holiday_picks.py scrape")
    cap = json.loads(CAPTURE.read_text(encoding="utf-8"))
    prices = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    ok, failed = 0, []
    for asin in award_asins():
        d = cap.get(asin) or {}
        price, rating, reviews = num(d.get("price")), num(d.get("rating")), num(d.get("reviews"), int)
        if not d.get("title") or None in (price, rating, reviews):
            failed.append(asin)
            continue
        prices[asin] = {"price": price, "rating": rating, "reviews_count": reviews, "checked": TODAY}
        ok += 1
    OUT.write_text(json.dumps(prices, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"holiday-prices: {ok} updated today, {len(failed)} not captured: {' '.join(failed)}")


if __name__ == "__main__":
    {"asins": lambda: print(len(award_asins()), *award_asins()), "scrape": scrape, "apply": apply}[sys.argv[1]]()
