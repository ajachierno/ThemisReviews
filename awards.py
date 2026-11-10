"""Score and award picks for ThemisReviews, all computed from the data (merge.py and build.py both use this).

Every award in research/editorial/<slug>.json is a rule, never a product:

    {"label": "Best Outdoor", "kind": "special", "rule": {"type": "feature", "key": "outdoor"}}

Rule types (the winner is always the highest score among the products that qualify):
    overall                      every product with at least 4.0 stars and 30 reviews (listing_age.py);
                                 every product on the page if none has both
    budget                       the cheapest third of the page, by price per item
    premium                      the priciest third of the page, by price per item
    feature  key [value] [also]  products whose feature `key` is true (or equals `value`, e.g. false);
                                 `also` adds more features that must match, e.g. {"switch": false}
    system   key                 products that work with that system slug (data/systems.json)
    brand    key                 products from that brand
    most_reviews                 the product with the most Amazon reviews
    top_rating                   the product with the highest star rating
    most_features                the product with the highest feature score

Ties go to the product with more reviews. Awards are handed out in the order listed and a product
holds at most one, so a later award goes to the best product that hasn't already won one. An award
with no qualifying product left is skipped for that build. The "why" line is written from the numbers.
"""
import json
import math
import re
from pathlib import Path

import listing_age

HERE = Path(__file__).resolve().parent

# "4-Pack", "3PCS", "Pack of 2", "(2-pack)" in the Amazon title or our model name. Kits are
# skipped: in "3-Pack Sensors + Hub" the count covers only part of what's in the box.
PACK_RE = re.compile(r"\b(\d{1,2})\s*-?\s*(?:pack|pk|pcs|count|ct)s?\b|\bpack\s+of\s+(\d{1,2})\b", re.I)
KIT_RE = re.compile(r"\bkit\b|gateway|\+\s*hub|with hub|hub mini|hub 2|\bvalve\b", re.I)

RULE_TYPES = {"overall", "budget", "premium", "feature", "system", "brand", "most_reviews", "top_rating", "most_features"}


def pack_size(p):
    text = f"{p.get('name', '')} {p.get('model', '')}"
    if KIT_RE.search(text):
        return 1
    sizes = {int(n) for m in PACK_RE.findall(text) for n in m if n}
    return sizes.pop() if len(sizes) == 1 and next(iter(sizes)) >= 2 else 1


def unit_price(p):
    return p["price"] / pack_size(p)


def feature_score(p, cat):
    return min(1.0, sum(cat["feature_weights"].get(k, 0) for k, on in p["features"].items() if on))


def score_product(p, cat):
    """100-point score: star rating, review volume (log scale, full credit at 200, newer listings boosted;
    see listing_age.py) and the page's weighted feature checklist."""
    w = cat["weights"]
    rating_s = p["rating"] / 5.0
    reviews_s, _mult = listing_age.review_subscore(p, cat, 20000)
    return round((w["rating"] * rating_s + w["reviews"] * reviews_s + w["features"] * feature_score(p, cat)) * 100)


def _systems():
    f = HERE / "data" / "systems.json"
    return {s["slug"]: s.get("name", s["slug"]) for s in json.loads(f.read_text(encoding="utf-8"))["systems"]} if f.exists() else {}


def _feature_label(cat, key):
    for f in cat.get("spec_fields", []) + cat.get("table_columns", []):
        if isinstance(f, dict) and f.get("key") == key and f.get("label"):
            return f["label"]
    return None


def check_rule(rule, cat, where=""):
    t = rule.get("type")
    assert t in RULE_TYPES, f"{where}: unknown award rule {rule}"
    if t == "feature":
        for k in [rule.get("key"), *rule.get("also", {})]:
            assert k in cat["feature_weights"], f"{where}: award rule feature {k!r} not in feature_weights"
    if t in ("system", "brand"):
        assert rule.get("key"), f"{where}: award rule {t} needs a key"


def _qualifies(rule, cat):
    t = rule["type"]
    prods = cat["products"]
    if t == "overall":
        ids = {p["asin"] for p in listing_age.overall_eligible(prods)}
        return lambda p: p["asin"] in ids
    if t in ("budget", "premium"):
        n = max(1, math.ceil(len(prods) / 3))
        by_price = sorted(prods, key=unit_price)
        pool = by_price[:n] if t == "budget" else by_price[-n:]
        ids = {p["asin"] for p in pool}
        return lambda p: p["asin"] in ids
    if t == "feature":
        want = {rule["key"]: rule.get("value", True), **rule.get("also", {})}
        return lambda p: all(bool(p["features"].get(k)) == v for k, v in want.items())
    if t == "system":
        return lambda p: rule["key"] in p.get("systems", [])
    if t == "brand":
        return lambda p: p.get("brand", "").lower() == rule["key"].lower()
    return lambda p: True


def _order(rule, cat):
    t = rule["type"]
    if t == "most_reviews":
        return lambda p: (-p["reviews_count"], -p["score"])
    if t == "top_rating":
        return lambda p: (-p["rating"], -p["reviews_count"])
    if t == "most_features":
        return lambda p: (-feature_score(p, cat), -p["score"], -p["reviews_count"])
    return lambda p: (-p["score"], -p["reviews_count"])


def _why(rule, p, cat, pool):
    t = rule["type"]
    facts = f'{p["rating"]} stars from {p["reviews_count"]:,} reviews, {"$"}{p["price"]:,.2f}'
    if t == "overall":
        if p["score"] >= max(x["score"] for x in cat["products"]):
            lead = f'Highest score on the page ({p["score"]})'
        else:
            lead = (f'Highest score ({p["score"]}) among picks with at least {listing_age.MIN_OVERALL_RATING:.1f} stars '
                    f'and {listing_age.MIN_OVERALL_REVIEWS} reviews')
    elif t == "budget":
        cap = max(unit_price(x) for x in pool)
        lead = f'Highest score ({p["score"]}) among the cheapest third of picks (up to {"$"}{cap:,.2f} each)'
    elif t == "premium":
        lead = f'Highest score ({p["score"]}) among the priciest third of picks'
    elif t == "feature":
        lab = _feature_label(cat, rule["key"])
        if not lab:
            lead = f'Highest score of the picks that fit this award ({p["score"]})'
        else:
            # The label is quoted as it appears in the specs ("Long Range: Yes"), so it reads
            # correctly whatever its wording or capitalization.
            yes_no = "Yes" if rule.get("value", True) else "No"
            lead = f'Highest score ({p["score"]}) among picks marked {yes_no} for {lab}'
    elif t == "system":
        lead = f'Highest score ({p["score"]}) among picks that work with {_systems().get(rule["key"], rule["key"])}'
    elif t == "brand":
        lead = f'Highest score ({p["score"]}) among {rule["key"]} picks'
    elif t == "most_reviews":
        lead = "Most Amazon reviews on the page"
    elif t == "top_rating":
        lead = "Highest star rating on the page"
    else:
        lead = "Most of this page's scored features"
    return f"{lead}: {facts}."


def resolve(cat):
    """Score every product and turn the page's award rules into awards with asin and why.
    Returns the resolved list (also stored in cat["awards"])."""
    for p in cat["products"]:
        p["score"] = score_product(p, cat)
    taken, out = set(), []
    for a in cat.get("awards", []):
        rule = a.get("rule")
        if not rule:  # already resolved (e.g. build reading merged data): re-resolve from the stored rule only
            continue
        ok = _qualifies(rule, cat)
        pool = [p for p in cat["products"] if ok(p)]
        cands = sorted((p for p in pool if p["asin"] not in taken), key=_order(rule, cat))
        if not cands:
            continue
        w = cands[0]
        taken.add(w["asin"])
        out.append({"label": a["label"], "kind": a.get("kind", "special"), "rule": rule, "asin": w["asin"],
                    "why": _why(rule, w, cat, pool)})
    cat["awards"] = out
    return out
