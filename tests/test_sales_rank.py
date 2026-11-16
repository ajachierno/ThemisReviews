"""Plain-assert tests for sales rank flags and Amazon list prices. Run: python -X utf8 tests/test_sales_rank.py"""
import json
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "research"))
import sales_rank  # noqa: E402
import creators_api  # noqa: E402

ITEM = {
    "asin": "B0TEST0001",
    "itemInfo": {"title": {"displayValue": "Zigbee Smart Plug"}},
    "browseNodeInfo": {
        "browseNodes": [
            {"contextFreeName": "Smart Plugs", "displayName": "Smart Plugs", "salesRank": 7},
            {"contextFreeName": "391fa3a0-755b-400e-98cb-8baba1d2b47e_1901", "salesRank": 1},
        ],
        "websiteSalesRank": {"salesRank": 2200},
    },
    "offersV2": {"listings": [
        {"isBuyBoxWinner": True, "availability": {"message": "In Stock"},
         "price": {"money": {"amount": 19.99, "displayAmount": "$19.99"},
                   "savingBasis": {"money": {"amount": 29.99}, "savingBasisType": "LIST_PRICE"}}},
    ]},
}


def test_record_reads_rank_and_list_price():
    assert "browseNodeInfo.browseNodes.salesRank" in creators_api.RESOURCES
    r = creators_api.record("B0TEST0001", ITEM)
    assert (r["cat_rank"], r["cat_node"], r["site_rank"], r["list_price"]) == (7, "Smart Plugs", 2200, 29.99)
    assert creators_api.record("B0TEST0001", None)["list_price"] is None


def test_price_pass_flags_only_falling_picks():
    import api_pricepass
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "sales-rank.json"
        products = {"smart-plugs": ["A", "B", "D", "E"]}

        def day(d, a_rank):
            recs = {x: {"cat_rank": r, "cat_node": "Smart Plugs", "site_rank": None}
                    for x, r in (("A", a_rank), ("B", 12), ("D", 20), ("E", 30), ("C", 9000))}
            return api_pricepass.rank_flags(products, recs, d, path)

        for d, r in (("2026-11-12", 60), ("2026-11-13", 130), ("2026-11-14", 200)):
            assert day(d, r) == {}
        assert day("2026-11-15", 250) == {"smart-plugs": ["A falling, #250 in Smart Plugs "
                                                          "(best #60 in its last 30 checks, page line #100)"]}
        assert "C" in sales_rank.load(path), "avoid picks are recorded, never flagged"


def test_holiday_card_list_price():
    import build
    p = {"asin": "A", "price": 25.0, "rating": 4.5, "reviews_count": 10}
    cat = {"data_captured": "2026-11-10"}
    real = build.HOLIDAY_PRICES
    try:
        build.HOLIDAY_PRICES = {"A": {"checked": "2026-11-15", "price": 19.99, "rating": 4.5, "reviews_count": 10,
                                      "list_price": 29.99}}
        q, d = build.holiday_price(p, cat)
        assert (q["price"], q["list_price"], d) == (19.99, 29.99, "2026-11-15")
        assert build.list_note(q) == " &middot; Amazon list price $29.99 (33% off)"
        q, d = build.holiday_price({**p, "price": 19.99}, {"data_captured": "2026-11-15"})
        assert q.get("list_price") == 29.99, "same check, same price"
        q, d = build.holiday_price({**p, "price": 21.0}, {"data_captured": "2026-11-15"})
        assert build.list_note(q) == "", "a different price: no list price claim"
    finally:
        build.HOLIDAY_PRICES = real


def test_holiday_api_saves_list_price():
    import holiday_picks
    with tempfile.TemporaryDirectory() as tmp:
        holiday_picks.OUT = Path(tmp) / "holiday-prices.json"
        holiday_picks.OUT.write_text(json.dumps({"A": {"price": 5, "rating": 4.4, "reviews_count": 77,
                                                       "checked": "2026-11-01", "list_price": 9.0}}), encoding="utf-8")
        holiday_picks.award_asins = lambda: ["A", "B"]
        holiday_picks.TODAY = "2026-11-15"
        fake = types.ModuleType("creators_api")
        fake.get_items = lambda asins: ({"A": {}, "B": {}}, [])
        fake.record = lambda a, it: {"price": "$19.99", "buybox": True, "notfound": False,
                                     "list_price": 29.99 if a == "B" else None}
        scrape = types.ModuleType("scrape_data")
        scrape.load_scrape = lambda: {"B": {"rating": "4.2", "reviews": "300"}}
        real = {k: sys.modules.get(k) for k in ("creators_api", "scrape_data")}
        sys.modules.update(creators_api=fake, scrape_data=scrape)
        try:
            holiday_picks.api()
        finally:
            for k, v in real.items():
                if v is None:
                    sys.modules.pop(k, None)
                else:
                    sys.modules[k] = v
        got = json.loads(holiday_picks.OUT.read_text(encoding="utf-8"))
        assert got["B"]["list_price"] == 29.99
        assert "list_price" not in got["A"], "yesterday's list price doesn't carry over"


def test_record_reads_buy_box_seller():
    r = creators_api.record("B0TEST0001", {**ITEM, "offersV2": {"listings": [
        {"isBuyBoxWinner": True, "merchantInfo": {"name": "Amazon Resale"}, "condition": {"value": "Used"},
         "price": {"money": {"amount": 15.0}}}]}})
    assert (r["seller"], r["condition"]) == ("Amazon Resale", "Used")
    assert creators_api.record("B0TEST0001", None)["seller"] is None


def test_price_pass_seller_flags():
    import api_pricepass
    import sellers
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "sellers.json"
        products = {"smart-plugs": ["A"]}
        brands = {"A": "THIRDREALITY", "C": "X"}
        out = {}
        for d, s in (("2026-11-13", "ThirdReality Store"), ("2026-11-14", "PlugDeals"), ("2026-11-15", "PlugDeals")):
            recs = {a: {"seller": s, "condition": "New"} for a in ("A", "C")}
            out = api_pricepass.seller_flags(products, brands, recs, d, path)
        assert out == {"smart-plugs": ["A seller changed, ThirdReality Store -> PlugDeals on the last 2 checks"]}
        assert "C" in sellers.load(path), "avoid picks are recorded, never flagged"


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"ok ({len(tests)} tests)")
