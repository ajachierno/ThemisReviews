"""Best of 2026: every category's Best Overall, Best Budget and Money No Object in one table.

Until FREEZE_DATE the page shows the live awards (each review page's overall, budget and premium
award rules, with that page's own label). The first build on or after FREEZE_DATE
writes data/best-of-2026.json; from then on the picks, ratings and review counts come only
from that file and never change. Prices keep moving: research/holiday_picks.py (scrape or api) re-reads the
frozen ASINs too, and with_prices() lays the newer prices over the frozen rows at build time.
The page is noindex and unlinked until REVEAL_DATE.
"""
import json
from pathlib import Path

SLUG = "best-of-2026"
FREEZE_DATE = "2026-12-31"
REVEAL_DATE = "2027-01-01"
DATA = Path(__file__).resolve().parent / "data"
FROZEN = DATA / "best-of-2026.json"
_HP = DATA / "holiday-prices.json"
HOLIDAY_PRICES = json.loads(_HP.read_text(encoding="utf-8")) if _HP.exists() else {}
RULES = ("overall", "budget", "premium")


def pages(site):
    """[(proto, sub, cat)] of every ready review page, ranked (tests swap this out)."""
    import build
    return build.ranked_pages(site)


def live_rows(site):
    """One row per award per review page, in site order, from today's awards. A pick whose
    holiday-prices.json check is newer than the page's capture takes those numbers."""
    rows = []
    for _proto, sub, cat in pages(site):
        by = {p["asin"]: p for p in cat["products"]}
        captured = cat.get("data_captured") or site["updated"]
        for rule in RULES:
            a = next((a for a in cat.get("awards", []) if a.get("rule", {}).get("type") == rule and a["asin"] in by), None)
            if not a:
                continue
            award, p = a["label"], by[a["asin"]]
            nums, date = p, captured
            hp = HOLIDAY_PRICES.get(p["asin"])
            if hp and hp["checked"] > captured:
                nums, date = hp, hp["checked"]
            rows.append({"slug": sub["slug"], "category": sub["title"], "award": award, "asin": p["asin"],
                         "title": f"{p['brand']} {p['model']}", "rating": nums["rating"],
                         "reviews_count": nums["reviews_count"], "price": nums["price"], "price_date": date})
    return rows


def load_frozen():
    return json.loads(FROZEN.read_text(encoding="utf-8")) if FROZEN.exists() else None


def ensure_frozen(site, today):
    """Write the frozen file once, on the first call on or after FREEZE_DATE. True if written."""
    if today < FREEZE_DATE or FROZEN.exists():
        return False
    FROZEN.write_text(json.dumps(live_rows(site), indent=1) + "\n", encoding="utf-8")
    return True


def with_prices(rows, holiday_prices):
    """Copies of rows with price and price_date from a newer holiday-prices check; nothing else changes."""
    out = []
    for r in rows:
        hp = holiday_prices.get(r["asin"])
        out.append({**r, "price": hp["price"], "price_date": hp["checked"]}
                   if hp and hp["checked"] > r["price_date"] else dict(r))
    return out


def rows_for_page(site):
    frozen = load_frozen()
    return with_prices(frozen, HOLIDAY_PRICES) if frozen is not None else live_rows(site)


def is_public(today):
    return today >= REVEAL_DATE


def frozen_asins():
    out = []
    for r in load_frozen() or []:
        if r["asin"] not in out:
            out.append(r["asin"])
    return out
