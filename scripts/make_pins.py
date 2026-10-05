#!/usr/bin/env python3
"""Generate Pinterest pins (1000x1500 PNG) from the ranked review pages, plus a CSV for
Pinterest's bulk upload (Settings > Import content > Upload .csv).

Pins are text graphics in the site's colors. No Amazon product photos (the Associates
agreement doesn't allow re-hosting them) and no prices except on the dated Black Friday
cheat sheet, because a pin keeps circulating long after a price moves.

Images go to docs/pins/ so GitHub Pages serves them at a public URL, which the bulk
upload requires. Needs Pillow (the site build does not):

    python scripts/make_pins.py --start 2026-10-06 --per-day 5
    python scripts/make_pins.py --only sample      # one of each format, no CSV
"""
import argparse
import csv
import datetime
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (reuses the site's loading, ranking and gift rules)

OUT = ROOT / "docs" / "pins"
CSV_DIR = ROOT / "marketing" / "pins"
FONTS = Path(__file__).parent / "fonts"
WORDMARK = Path(__file__).parent / "wordmark.png"
W, H = 1000, 1500
PAD = 64

BG, CARD, LINE = "#15141a", "#221f3a", "#36315c"
INK, MUTED = "#efe9dc", "#a7a1bd"
GOLD, OVERALL, BUDGET, AVOID, PURPLE, STAR = "#d8b25a", "#3fbf7f", "#5b9bff", "#e0483c", "#9a7ce0", "#f0c24a"
DOMAIN = "themisreviews.com"

# Pinterest boards, by device family. Families not listed go to the general board.
BOARDS = {
    "gifts": "Smart Home Gift Ideas (Holiday 2026)",
    "lighting": "Smart Lighting: Switches, Dimmers & Bulbs",
    "security": "Smart Home Security: Locks, Cameras & Sensors",
    "climate": "Smart Home Climate & Safety",
    "hubs": "Smart Home Hubs & DIY (Home Assistant, Zigbee, Z-Wave)",
    "general": "Smart Home Ideas & Gadgets",
    "guides": "Smart Home Tips: Zigbee vs Z-Wave vs Matter",
}
FAMILY_BOARD = {
    "light-switches": "lighting", "dimmers": "lighting", "bulbs": "lighting", "smart-plugs": "lighting",
    "door-sensors": "security", "motion-sensors": "security", "locks": "security",
    "indoor-cameras": "security", "outdoor-cameras": "security", "doorbells": "security",
    "garage-openers": "security", "trackers": "security",
    "leak-sensors": "climate", "thermostats": "climate", "temperature-sensors": "climate",
    "smoke-detectors": "climate", "air-quality-monitors": "climate", "water-valves": "climate",
    "weather-stations": "climate",
    "hubs": "hubs", "buttons": "hubs",
}


def font(weight, size):
    return ImageFont.truetype(str(FONTS / f"inter-{weight}.ttf"), size)


def wrap(draw, text, fnt, width, max_lines):
    """Greedy word wrap by pixel width; ellipsis on the last line if it overflows."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textlength(last + "…", font=fnt) > width:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last.rstrip(",.;:—- ") + "…"
    return lines


def text_block(draw, xy, text, fnt, fill, width, max_lines, gap=1.18):
    x, y = xy
    for ln in wrap(draw, text, fnt, width, max_lines):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * gap)
    return y


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    draw.polygon(pts, fill=fill)


def rating_line(draw, x, y, p, size=30):
    star(draw, x + size * 0.5, y + size * 0.55, size * 0.52, STAR)
    f = font(700, size)
    draw.text((x + size * 1.25, y), f"{p['rating']}", font=f, fill=INK)
    tx = x + size * 1.25 + draw.textlength(f"{p['rating']}", font=f) + 14
    draw.text((tx, y + 2), f"{p['reviews_count']:,} reviews", font=font(400, size - 4), fill=MUTED)


def pill(draw, x, y, text, fill, fnt, ink="#ffffff", padx=18, pady=8):
    tw = draw.textlength(text, font=fnt)
    h = fnt.size + pady * 2
    draw.rounded_rectangle((x, y, x + tw + padx * 2, y + h), radius=h // 2, fill=fill)
    draw.text((x + padx, y + pady - 2), text, font=fnt, fill=ink)
    return x + tw + padx * 2


def canvas():
    img = Image.new("RGB", (W, H), BG)
    wm = Image.open(WORDMARK).convert("RGB")
    ww = 400
    wm = wm.resize((ww, int(wm.height * ww / wm.width)), Image.LANCZOS)
    # Feather the edges so the artwork's starry background fades into the pin.
    mask = Image.new("L", wm.size, 255)
    md = ImageDraw.Draw(mask)
    fade = 28
    for i in range(fade):
        a = int(255 * i / fade)
        md.rectangle((i, i, wm.width - 1 - i, wm.height - 1 - i), outline=a)
    img.paste(wm, ((W - ww) // 2, 26), mask)
    return img, ImageDraw.Draw(img)


def header(draw, kicker, title, color=GOLD, y=262):
    kf = font(700, 30)
    draw.text(((W - draw.textlength(kicker, font=kf)) // 2, y), kicker, font=kf, fill=color)
    tf = font(900, 72)
    y += 54
    for ln in wrap(draw, title, tf, W - PAD * 2, 3):
        draw.text(((W - draw.textlength(ln, font=tf)) // 2, y), ln, font=tf, fill=INK)
        y += 82
    return y + 22


def footer(draw, cta, color=GOLD):
    cf = font(900, 38)
    ink = "#1d1405" if color == GOLD else "#ffffff"
    bw = draw.textlength(cta, font=cf) + 80
    x0, y0 = (W - bw) // 2, H - 190
    draw.rounded_rectangle((x0, y0, x0 + bw, y0 + 84), radius=18, fill=color)
    draw.text((x0 + 40, y0 + 20), cta, font=cf, fill=ink)
    uf = font(700, 30)
    draw.text(((W - draw.textlength(DOMAIN, font=uf)) // 2, H - 80), DOMAIN, font=uf, fill=MUTED)


def name(p):
    return f"{p['brand']} {p['model']}"


def product_rows(draw, y, items, bottom):
    """items: [(label, label_color, p)] stacked cards filling y..bottom."""
    n = len(items)
    gap = 18
    h = (bottom - y - gap * (n - 1)) // n
    big = h >= 230
    for i, (label, color, p) in enumerate(items):
        top = y + i * (h + gap)
        draw.rounded_rectangle((PAD, top, W - PAD, top + h), radius=22, fill=CARD)
        draw.rounded_rectangle((PAD, top, PAD + 10, top + h), radius=5, fill=color)
        x = PAD + 40
        cy = top + (26 if big else 18)
        pill(draw, x, cy, label, color, font(900, 24 if big else 21))
        cy += 52 if big else 44
        cy = text_block(draw, (x, cy), name(p), font(700, 38 if big else 32), INK,
                        W - PAD * 2 - 80, 2 if big else 1)
        rating_line(draw, x, cy + 6, p, 30 if big else 26)
        sf = font(900, 30 if big else 26)
        s = f"Score {p['score']}"
        draw.text((W - PAD - 36 - draw.textlength(s, font=sf), top + (30 if big else 20)), s, font=sf, fill=GOLD)
    return y + n * h + (n - 1) * gap


def board_for(cat):
    return BOARDS[FAMILY_BOARD.get(cat.get("family"), "general")]


def short_title(sub):
    """'Zigbee leak sensors' -> 'Zigbee Leak Sensors' for pin headlines."""
    keep = {"Wi-Fi", "Z-Wave", "Zigbee", "Matter", "Thread", "Bluetooth", "Lutron", "Caseta", "MHz", "CO", "RF", "SDR"}
    return " ".join(w if w in keep or not w.islower() else w.capitalize() for w in sub["title"].split())


# ----------------------------------------------------------------------- formats
def pin_top3(sub, cat, year):
    ranked = sorted(cat["products"], key=lambda p: p["rank"])
    ov, bu = build.page_overall_budget(cat)
    picks, seen = [("Best Overall", OVERALL, ov)], {ov["asin"]}
    if bu:
        seen.add(bu["asin"])
    nxt = next((p for p in ranked if p["asin"] not in seen), None)
    if nxt:
        picks.append(("Top score" if nxt["rank"] == 1 else f"Ranked #{nxt['rank']}", PURPLE, nxt))
    if bu and bu is not ov:
        picks.append(("Best Budget", BUDGET, bu))
    t = short_title(sub)
    img, d = canvas()
    y = header(d, "RANKED FROM REAL AMAZON REVIEWS", f"The Best {t} ({year})")
    product_rows(d, y, picks, H - 230)
    footer(d, "See the full ranking")
    title = f"The Best {t} ({year}): Top Picks Ranked From Real Reviews"
    desc = (f"Which {sub['title'].lower()} are worth buying? We scored every one on Amazon rating, "
            f"review count, and the features that matter. Best Overall: {name(ov)}."
            + (f" Best Budget: {name(bu)}." if bu and bu is not ov else "")
            + " See the full ranking, which smart home systems each works with, and the one to avoid.")
    kw = [f"best {sub['title'].lower()}", f"{sub['title'].lower()} {year}", "smart home",
          "smart home ideas", "home automation", "smart home gadgets"]
    return img, title, desc, f"{sub['slug']}.html", kw


def pin_avoid(sub, cat, year):
    a = cat["avoid"][0]
    ov, _bu = build.page_overall_budget(cat)
    t = short_title(sub)
    img, d = canvas()
    y = header(d, t.upper(), "Don't Buy This One.", AVOID)
    d.rounded_rectangle((PAD, y, W - PAD, H - 230), radius=22, fill=CARD, outline=AVOID, width=4)
    x, cy, tw = PAD + 44, y + 36, W - PAD * 2 - 88
    pill(d, x, cy, "AVOID", AVOID, font(900, 26))
    cy += 70
    cy = text_block(d, (x, cy), name(a), font(900, 44), INK, tw, 2)
    rating_line(d, x, cy + 8, a, 28)
    cy += 70
    d.text((x, cy), "WHY WE'D SKIP IT", font=font(700, 26), fill=AVOID)
    cy += 46
    reasons = [a.get("flag", "")] + [r.split(". ")[0].rstrip(".") for r in a["reasons"]]
    reasons = [r for r in dict.fromkeys(reasons) if r][:3]
    for r in reasons:
        if cy > H - 520:
            break
        d.ellipse((x, cy + 12, x + 12, cy + 24), fill=AVOID)
        cy = text_block(d, (x + 30, cy), r, font(400, 32), INK, tw - 30, 3) + 14
    cy = max(cy + 10, H - 470)
    d.line((x, cy, W - PAD - 44, cy), fill=LINE, width=2)
    cy += 26
    d.text((x, cy), "BUY THIS INSTEAD", font=font(700, 26), fill=OVERALL)
    cy += 44
    cy = text_block(d, (x, cy), name(ov), font(700, 36), INK, tw, 2)
    rating_line(d, x, cy + 6, ov, 28)
    footer(d, "See the full ranking")
    title = f"{t} to Avoid: Skip the {name(a)}"[:100]
    desc = (f"Shopping for {sub['title'].lower()} on Amazon? Skip the {name(a)}. {a['verdict']} "
            f"Buy this instead: the {name(ov)}, our Best Overall. See every pick ranked from real reviews.")
    kw = [f"{sub['title'].lower()} to avoid", f"best {sub['title'].lower()}", "smart home",
          "amazon buying guide", "home automation"]
    return img, title, desc, f"{sub['slug']}.html#avoid", kw


def pin_gifts(cfg, chunk, part, parts):
    band = f"Under ${cfg['max_price']}" if not cfg.get("min_price") else f"${int(cfg['min_price'])}–${cfg['max_price']}"
    img, d = canvas()
    kicker = "HOLIDAY GIFT GUIDE 2026" + (f" · {part}/{parts}" if parts > 1 else "")
    y = header(d, kicker, f"Smart Home Gifts {band}")
    items = [(cat.get("family_title", ""), GOLD, p) for p, cat, _sub in chunk]
    product_rows(d, y, items, H - 230)
    footer(d, "See every gift pick")
    title = f"Smart Home Gifts {band} (2026)" + (f", Part {part}" if parts > 1 else "")
    desc = (f"Smart home gift ideas {band.lower()}, each the top-rated pick in its category from real "
            f"Amazon reviews, for techies, new homeowners, and anyone who likes gadgets. "
            + "; ".join(f"{cat.get('family_title', '')}: {name(p)}" for p, cat, _s in chunk) + ".")
    kw = [f"smart home gifts {band.lower()}", "gifts for him", "tech gifts", "gadget gifts",
          "christmas gift ideas", "gifts for dad", "smart home ideas"]
    return img, title, desc, f"{cfg['slug']}.html", kw


def pin_black_friday(cfg, rows):
    img, d = canvas()
    y = header(d, "BLACK FRIDAY · NOV 27, 2026", "Smart Home Price Cheat Sheet")
    d.text((PAD, y), "Our #1 pick and its regular price. Beat it or skip it.", font=font(400, 30), fill=MUTED)
    y += 64
    rf, pf, cf = font(700, 30), font(900, 32), font(400, 22)
    row_h = 80
    for sub, ov in rows[:8]:
        d.rounded_rectangle((PAD, y, W - PAD, y + row_h - 10), radius=14, fill=CARD)
        d.text((PAD + 28, y + 6), sub["title"].upper(), font=cf, fill=MUTED)
        nm = wrap(d, name(ov), rf, W - PAD * 2 - 240, 1)[0]
        d.text((PAD + 28, y + 32), nm, font=rf, fill=INK)
        pr = build.money(ov["price"])
        d.text((W - PAD - 28 - d.textlength(pr, font=pf), y + 20), pr, font=pf, fill=GOLD)
        y += row_h
    d.text((PAD, y + 6), "Regular Amazon prices captured Oct 2026. Prices change.", font=font(400, 24), fill=MUTED)
    footer(d, "Full price-to-beat list")
    title = "Black Friday 2026 Smart Home Deals: Price Cheat Sheet"
    desc = ("Is that Black Friday smart home deal real? Our top-ranked video doorbells, cameras, smart "
            "plugs, thermostats, locks and more, with the regular price we recorded. Beat it or skip it. "
            "Black Friday is Nov 27, 2026; Cyber Monday is Nov 30.")
    kw = ["black friday smart home deals", "black friday 2026", "cyber monday deals",
          "smart home deals", "tech deals"]
    return img, title, desc, f"{cfg['slug']}.html", kw


def pin_protocol(p):
    img, d = canvas()
    y = header(d, "SMART HOME PROTOCOLS, EXPLAINED", f"{p['name']}: Pros and Cons")
    x, tw = PAD + 44, W - PAD * 2 - 88
    for label, color, items in (("PROS", OVERALL, p.get("pros", [])), ("CONS", AVOID, p.get("cons", []))):
        d.text((x, y), label, font=font(900, 30), fill=color)
        y += 50
        for it in items[:3]:
            d.ellipse((x, y + 12, x + 12, y + 24), fill=color)
            y = text_block(d, (x + 30, y), it, font(400, 32), INK, tw - 30, 2) + 12
        y += 20
    if p.get("verdict"):
        d.line((x, y, W - PAD - 44, y), fill=LINE, width=2)
        y += 24
        d.text((x, y), "OUR TAKE", font=font(700, 26), fill=GOLD)
        text_block(d, (x, y + 44), p["verdict"], font(700, 32), INK, tw, 4)
    footer(d, "Compare every protocol")
    title = f"{p['name']} Smart Home: Pros, Cons, and Who It's For"
    desc = (f"Should you build your smart home on {p['name']}? {p.get('summary', '')} "
            f"See the pros and cons of Z-Wave, Zigbee, Wi-Fi, Thread, Matter, and more, side by side.")
    kw = [f"{p['name'].lower()} smart home", "zigbee vs z-wave", "matter smart home",
          "smart home for beginners", "home automation", "home assistant"]
    return img, title, desc, f"#{p['slug']}", kw


# ------------------------------------------------------------------------ driver
def all_pins():
    """[(id, board, (img, title, desc, path, kw))] in posting order: gifts first (the
    season is now), Black Friday next, then top-3 / avoid / protocol pins interleaved."""
    site = build.load("site.json")
    year = str(site["updated"])[:4]
    pages = build.ranked_pages(site)
    pins = []
    for cfg in build.SEASONAL.get("gifts", []):
        if not cfg.get("enabled"):
            continue
        picks = build.gift_picks(pages, cfg)
        picks.sort(key=lambda x: -x[0]["score"])
        chunks = [picks[i:i + 5] for i in range(0, len(picks), 5)]
        chunks = [c for c in chunks if len(c) >= 3]
        for i, c in enumerate(chunks, 1):
            pins.append((f"gifts-{cfg['max_price']}-{i}", BOARDS["gifts"], pin_gifts(cfg, c, i, len(chunks))))
    bf = build.SEASONAL.get("black_friday")
    bf_pin = None
    if bf and bf.get("enabled"):
        popular = ["wifi-doorbells", "wifi-outdoor-cameras", "wifi-indoor-cameras", "wifi-smart-plugs",
                   "wifi-bulbs", "wifi-thermostats", "wifi-locks", "bluetooth-trackers",
                   "wifi-robot-vacuums", "wifi-smart-speakers", "wifi-garage-openers", "matter-smart-plugs"]
        rows = []
        for _p, sub, cat in pages:
            if sub["slug"] in popular:
                rows.append((popular.index(sub["slug"]), sub, build.page_overall_budget(cat)[0]))
        rows = [(s, o) for _i, s, o in sorted(rows, key=lambda r: r[0])]
        bf_pin = ("black-friday-cheat-sheet", BOARDS["gifts"], pin_black_friday(bf, rows))
    top3 = [(f"top3-{sub['slug']}", board_for(cat), pin_top3(sub, cat, year)) for _p, sub, cat in pages]
    avoid = [(f"avoid-{sub['slug']}", board_for(cat), pin_avoid(sub, cat, year))
             for _p, sub, cat in pages if cat.get("avoid")]
    proto = [(f"protocol-{p['slug']}", BOARDS["guides"], pin_protocol(p)) for p in site["protocols"] if p.get("pros")]
    evergreen = []
    for i in range(max(len(top3), len(avoid), len(proto))):
        evergreen += top3[i:i + 1] + avoid[i:i + 1] + proto[i:i + 1]
    return site, pins, bf_pin, evergreen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default=str(datetime.date.today() + datetime.timedelta(days=1)))
    ap.add_argument("--per-day", type=int, default=5)
    ap.add_argument("--bf-date", default="2026-11-01", help="publish date for the Black Friday pin")
    ap.add_argument("--only", choices=["sample"], help="write one pin of each format, no CSV")
    ap.add_argument("--pages", nargs="+", help="only top-3/avoid pins for these page slugs (a follow-up batch)")
    args = ap.parse_args()
    site, seasonal, bf_pin, evergreen = all_pins()
    ordered = seasonal + evergreen
    if args.pages:
        want = set(args.pages)
        ordered = [p for p in evergreen if p[0].split("-", 1)[1] in want and not p[0].startswith("protocol-")]
        bf_pin = None
    if args.only == "sample":
        keep = {seasonal[0][0] if seasonal else "", "black-friday-cheat-sheet", "top3-wifi-smart-plugs",
                "avoid-wifi-indoor-cameras", "protocol-zigbee"}
        ordered = [p for p in seasonal + ([bf_pin] if bf_pin else []) + evergreen if p[0] in keep]
    OUT.mkdir(parents=True, exist_ok=True)
    base = f"https://{site['custom_domain']}"
    hours = [14, 16, 18, 20, 22, 23, 15, 17, 19, 21][:args.per_day]  # UTC = US daytime/evening
    start = datetime.date.fromisoformat(args.start)
    rows = []

    def save(pid, board, payload, when):
        img, title, desc, path, kw = payload
        img.quantize(256, dither=Image.Dither.NONE).save(OUT / f"{pid}.png", optimize=True)
        link = f"{base}/{path}" if not path.startswith("#") else f"{base}/{path}"
        rows.append({"Title": title[:100], "Media URL": f"{base}/pins/{pid}.png", "Pinterest board": board,
                     "Thumbnail": "", "Description": desc[:499], "Link": link,
                     "Publish date": when.strftime("%Y-%m-%dT%H:%M:%S"), "Keywords": ", ".join(kw)})

    for i, (pid, board, payload) in enumerate(ordered):
        day, slot = divmod(i, args.per_day)
        save(pid, board, payload, datetime.datetime.combine(start + datetime.timedelta(days=day), datetime.time(hours[slot])))
    if bf_pin and args.only != "sample":
        save(*bf_pin, datetime.datetime.combine(datetime.date.fromisoformat(args.bf_date), datetime.time(15)))
    print(f"wrote {len(rows)} pin(s) to {OUT}")
    if args.only != "sample":
        CSV_DIR.mkdir(parents=True, exist_ok=True)
        rows.sort(key=lambda r: r["Publish date"])
        path = CSV_DIR / f"batch-{args.start}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {path} ({len(rows)} rows, {rows[0]['Publish date']} .. {rows[-1]['Publish date']})")


if __name__ == "__main__":
    main()
