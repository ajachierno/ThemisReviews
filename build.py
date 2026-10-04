"""ThemisReviews static site generator.

Reads data/site.json and writes the static site into docs/ for GitHub Pages.
Zero dependencies. Run:  python build.py
"""
import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
OUT = ROOT / "docs"
ASSETS = OUT / "assets"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def esc(s):
    return html.escape(str(s), quote=True)


def jsonld(*objs):
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>'
        for o in objs)


def base_url(site):
    return f"https://{site['custom_domain']}" if site.get("custom_domain") else ""


def page(site, title, body, is_home=False, description=None, canonical="",
         structured_data="", updated=None):
    desc = description or site["description"]
    base = base_url(site)
    image = f"{base}/assets/logo.jpg" if base else "assets/logo.jpg"
    canonical_tag = f'\n<link rel="canonical" href="{esc(canonical)}">' if canonical else ""
    tag_state = ("" if site["affiliate_tag"] else
                 '<div class="notice">Preview build. Affiliate links are untagged until '
                 'the Amazon Associates account is approved.</div>')
    if is_home:
        header = f"""<header class="site home-head">
  <a class="banner" href="./"><img src="assets/logo.webp" width="1280" height="720"
    alt="{esc(site['brand'])}: Themis holding the scales of justice"></a>
</header>"""
    else:
        header = f"""<header class="site">
  <a class="logo" href="./"><img src="assets/favicon.png" width="48" height="48" alt="">
    <span>{esc(site['brand'])}</span></a>
  <span class="slogan">{esc(site['tagline'])}</span>
</header>"""
    home_link = "" if is_home else '<a href="./">&larr; All protocols</a> &nbsp; '
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">{canonical_tag}
<meta name="theme-color" content="#0b0a17">
<link rel="icon" href="assets/favicon.png">
<meta property="og:type" content="{"website" if is_home else "article"}">
<meta property="og:site_name" content="{esc(site['brand'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{esc(image)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&display=swap">
{structured_data}
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{header}
{tag_state}
<main>
{body}
</main>
<footer>
  <p class="disclosure"><b>Affiliate disclosure.</b> {esc(site['brand'])} is reader-supported.
  When you buy through links on this site we may earn an Amazon Associates commission, at no
  extra cost to you. Prices and ratings come from Amazon and change over time.</p>
  <p class="muted">{home_link}Last updated on {esc(updated or site['updated'])}. Not affiliated with Amazon,
  the Z-Wave Alliance, the Connectivity Standards Alliance, the Thread Group, Lutron, or any manufacturer.</p>
</footer>
<a href="#" class="to-top" aria-label="Back to top">&uarr;</a>
<script>(function(){{var b=document.querySelector('.to-top');
window.addEventListener('scroll',function(){{b.classList.toggle('show',window.scrollY>600);}},{{passive:true}});}})();</script>
</body>
</html>"""


# --------------------------------------------------------------------------- system icons
# Small original glyphs in each system's colors (not the companies' logos). Keys match
# data/systems.json slugs; every product's "systems" list renders as a row of these.
SYSTEM_ICONS = {
    "home-assistant": '<rect width="20" height="20" rx="5" fill="#18BCF2"/><path d="M10 4.2 16 9.4V15.6H4V9.4Z" fill="none" stroke="#fff" stroke-width="1.7" stroke-linejoin="round"/><circle cx="10" cy="11.6" r="1.6" fill="#fff"/>',
    "apple-home": '<rect width="20" height="20" rx="5" fill="#FF9500"/><path d="M10 4 16.4 9.7H14.6V15.8H5.4V9.7H3.6Z" fill="#fff"/>',
    "google-home": '<rect width="20" height="20" rx="5" fill="#fff"/><circle cx="7" cy="7" r="2.3" fill="#4285F4"/><circle cx="13" cy="7" r="2.3" fill="#EA4335"/><circle cx="7" cy="13" r="2.3" fill="#FBBC05"/><circle cx="13" cy="13" r="2.3" fill="#34A853"/>',
    "alexa": '<rect width="20" height="20" rx="5" fill="#0F1B2D"/><circle cx="10" cy="10" r="5.4" fill="none" stroke="#00CAFF" stroke-width="2.3"/>',
    "smartthings": '<rect width="20" height="20" rx="5" fill="#1F4FD6"/><path d="M10 5.2 14.6 13.4H5.4Z" fill="none" stroke="#fff" stroke-width="1.3"/><circle cx="10" cy="5.2" r="1.9" fill="#fff"/><circle cx="14.6" cy="13.4" r="1.9" fill="#fff"/><circle cx="5.4" cy="13.4" r="1.9" fill="#fff"/>',
    "hubitat": '<rect width="20" height="20" rx="5" fill="#2E8B3E"/><path d="M6 5V15M14 5V15M6 10H14" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>',
    "homey": '<rect width="20" height="20" rx="5" fill="#E9316B"/><circle cx="10" cy="10" r="5" fill="none" stroke="#fff" stroke-width="2"/><circle cx="10" cy="10" r="1.8" fill="#fff"/>',
}
SYSTEM_NAMES = {s["slug"]: s["name"] for s in json.loads((DATA / "systems.json").read_text(encoding="utf-8"))["systems"]}


def sys_icon(slug):
    name = esc(SYSTEM_NAMES[slug])
    return (f'<span class="sys-ico" tabindex="0" role="img" aria-label="{name}" title="{name}" data-tip="{name}">'
            f'<svg viewBox="0 0 20 20" width="17" height="17" aria-hidden="true">{SYSTEM_ICONS[slug]}</svg></span>')


def sys_icons(slugs):
    if not slugs:
        return '<span class="tiny muted">Standalone</span>'
    return '<span class="sys-icons">' + "".join(sys_icon(x) for x in SYSTEM_NAMES if x in slugs) + "</span>"


FACT_COLUMNS = [
    ("band", "Frequency"),
    ("topology", "Network"),
    ("hub", "Hub needed"),
    ("power", "Power use"),
    ("best_for", "Best for"),
]


def render_jump(protocols):
    links = "".join(f'<a href="#{esc(p["slug"])}">{esc(p["name"])}</a>' for p in protocols)
    return f"""
  <nav class="jump" aria-label="Jump to a section">
    <a href="#systems" class="jump-all">Systems</a><a href="#compare" class="jump-all">Protocols at a glance</a>{links}
  </nav>"""


def buy_cell(site, s):
    """Amazon link with live price when the hub is sold there at a fair price, else the maker's store."""
    if s.get("asin"):
        out = (f'<a class="btn small" href="{amazon_url(site, s["asin"])}" target="_blank" rel="sponsored nofollow noopener">'
               f'{money(s["price"])} on Amazon</a>'
               f'<div class="tiny muted">{s["rating"]} stars, {s["reviews_count"]:,} reviews</div>')
        if s.get("addon"):
            a = s["addon"]
            out += (f'<div class="tiny"><a href="{amazon_url(site, a["asin"])}" target="_blank" rel="sponsored nofollow noopener">'
                    f'{esc(a["label"])}: {money(a["price"])}</a></div>')
        return out
    return (f'<a class="btn small ghost-btn" href="{esc(s["store"])}" target="_blank" rel="noopener">Buy from {esc(s["maker"])}</a>'
            f'<div class="tiny muted">{esc(s["store_note"])}</div>')


def render_systems(site, data):
    systems = data["systems"]
    rows = "".join(f"""<tr>
        <td>{sys_icon(s['slug'])} <a class="sys-name" href="{esc(s['site'])}" target="_blank" rel="noopener">{esc(s['name'])}</a><div class="tiny muted">{esc(s['maker'])}</div></td>
        <td>{esc(s['hub'])}</td><td>{esc(s['radios'])}</td><td>{esc(s['local'])}</td>
        <td>{esc(s['phones'])}</td><td>{esc(s['best_for'])}</td><td class="buy">{buy_cell(site, s)}</td></tr>""" for s in systems)
    pc_rows = "".join(f"""<tr>
        <td>{sys_icon(s['slug'])} <a class="sys-name" href="{esc(s['site'])}" target="_blank" rel="noopener">{esc(s['name'])}</a></td>
        <td><ul class="pc-list pros">{''.join(f'<li>{esc(x)}</li>' for x in s['pros'])}</ul></td>
        <td><ul class="pc-list cons">{''.join(f'<li>{esc(x)}</li>' for x in s['cons'])}</ul></td></tr>""" for s in systems)
    return f"""
  <section id="systems">
    <h2>Start with your system</h2>
    <p class="group-sub">The system is the app and hub that runs everything. It decides which protocols you can use, so pick it before you buy switches and sensors. Names link to each system's site; prices are from Amazon on {esc(data['data_captured'])}.</p>
    <p class="swipe-hint">Swipe the tables sideways to see every column.</p>
    <div class="tablewrap"><table class="sys-table">
      <thead><tr><th>System</th><th>Hub to buy</th><th>Built-in radios</th><th>Runs locally</th><th>Phones</th><th>Best for</th><th>Where to buy</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <h3 class="sys-sub">Pros and cons</h3>
    <div class="tablewrap"><table class="sys-table sys-pc">
      <thead><tr><th>System</th><th>Pros</th><th>Cons</th></tr></thead>
      <tbody>{pc_rows}</tbody>
    </table></div>
  </section>"""


def render_compare(protocols):
    head = "".join(f"<th>{esc(label)}</th>" for _, label in FACT_COLUMNS)
    rows = "".join(
        f'<tr><td><a href="#{esc(p["slug"])}">{esc(p["name"])}</a></td>'
        + "".join(f"<td>{esc(p['facts'].get(key, ''))}</td>" for key, _ in FACT_COLUMNS)
        + "</tr>"
        for p in protocols)
    return f"""
  <section id="compare">
    <h2>At a glance</h2>
    <p class="swipe-hint">Swipe the table sideways to see every column.</p>
    <div class="tablewrap"><table>
      <thead><tr><th>Protocol</th>{head}</tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
  </section>"""


def render_subs(p):
    items = []
    for s in p["subs"]:
        if s.get("ready"):
            items.append(f'<li><a class="sub-link" href="{esc(s["slug"])}.html">'
                         f'{esc(s["title"])} <span class="arrow">&rarr;</span></a></li>')
        else:
            items.append(f'<li><span class="sub-link soon">{esc(s["title"])}'
                         f'<span class="soon-tag">Coming soon</span></span></li>')
    return f"""
    <details class="subs">
      <summary>{esc(p['name'])} product reviews <span class="count">{len(p['subs'])}</span></summary>
      <ul class="sub-grid">{''.join(items)}</ul>
    </details>"""


def render_protocol(p):
    pros = "".join(f"<li>{esc(x)}</li>" for x in p["pros"])
    cons = "".join(f"<li>{esc(x)}</li>" for x in p["cons"])
    return f"""
  <section class="proto" id="{esc(p['slug'])}">
    <div class="proto-head">
      <h2>{esc(p['name'])}</h2>
      <span class="proto-band">{esc(p['facts']['band'])}</span>
    </div>
    <p class="proto-sum">{esc(p['summary'])}</p>
    <p class="verdict"><b>Our take:</b> {esc(p['verdict'])}</p>
    <div class="pc">
      <div class="pros"><h3>Pros</h3><ul>{pros}</ul></div>
      <div class="cons"><h3>Cons</h3><ul>{cons}</ul></div>
    </div>{render_subs(p)}
  </section>"""


def build_home(site):
    protos = site["protocols"]
    body = f"""
  <section class="lead home">
    <h1>Pick your system, then your protocol</h1>
    <p class="sub">{esc(site['description'])}</p>
  </section>
  {render_jump(protos)}
  {render_systems(site, load("systems.json"))}
  {render_compare(protos)}
  <h2 class="section-head">Pros and cons by protocol</h2>
  <p class="group-sub">Open the reviews list under any protocol to see the device types we cover on it.</p>
  {''.join(render_protocol(p) for p in protos)}"""
    base = base_url(site)
    org = {"@context": "https://schema.org", "@type": "Organization", "name": site["brand"],
           "url": f"{base}/" if base else "", "logo": f"{base}/assets/logo.jpg" if base else ""}
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": site["brand"],
               "url": f"{base}/" if base else "", "description": site["description"]}
    (OUT / "index.html").write_text(
        page(site, f"{site['brand']}: smart home protocols compared", body, is_home=True,
             canonical=f"{base}/" if base else "", structured_data=jsonld(org, website)),
        encoding="utf-8")


# --------------------------------------------------------------------------- category pages
# Each ready sub-page has data/pages/<slug>.json: products (up to 10), one avoid pick,
# editorial awards, scoring weights, spec/table columns, and a buyer's guide.

def amazon_url(site, asin):
    base = f"https://{site['amazon_domain']}/dp/{asin}"
    return f"{base}?tag={site['affiliate_tag']}&linkCode=ll1" if site["affiliate_tag"] else base


def money(v):
    return f"${v:,.2f}"


def stars(rating):
    pct = round(rating / 5 * 100)
    return f'<span class="stars" style="--pct:{pct}%" aria-label="{rating} out of 5 stars"></span>'


def score_product(p, cat):
    """Same 100-point scale as ToolboxTop10: rating, review volume (log scale), features."""
    w = cat["weights"]
    rating_s = p["rating"] / 5.0
    reviews_s = min(1.0, math.log10(p["reviews_count"] + 1) / math.log10(cat.get("reviews_ceiling", 20000)))
    feat_s = min(1.0, sum(cat["feature_weights"].get(k, 0) for k, on in p["features"].items() if on))
    return round((w["rating"] * rating_s + w["reviews"] * reviews_s + w["features"] * feat_s) * 100)


def rank_products(cat):
    for p in cat["products"]:
        p["score"] = score_product(p, cat)
        p["awards"] = []
    ranked = sorted(cat["products"], key=lambda p: (-p["score"], -p["reviews_count"]))
    for i, p in enumerate(ranked, 1):
        p["rank"] = i
    by_asin = {p["asin"]: p for p in ranked}
    for a in cat.get("awards", []):
        by_asin[a["asin"]]["awards"].append(a)
    return ranked


def spec_value(p, field):
    if field.get("type") == "bool":
        return "Yes" if p["features"].get(field["key"]) else "No"
    v = p["specs"].get(field["key"])
    return "&mdash;" if v in (None, "") else esc(v)


def render_award(a, p, site):
    return f"""
    <a class="hero-card {esc(a['kind'])}" href="{amazon_url(site, p['asin'])}" target="_blank" rel="sponsored nofollow noopener">
      <span class="hero-tag">{esc(a['label'])}</span>
      <img src="{esc(p['image'])}" alt="{esc(p['name'])}" loading="lazy">
      <div class="hero-body">
        <div class="hero-brand">{esc(p['brand'])}</div>
        <div class="hero-name">{esc(p['brand'])} {esc(p['model'])}</div>
        <div class="hero-meta">{stars(p['rating'])} <b>{p['rating']}</b> <span class="muted">({p['reviews_count']:,})</span></div>
        <p class="hero-why">{esc(a['why'])}</p>
        <div class="hero-price">{money(p['price'])}</div>
        <span class="btn">View on Amazon &rarr;</span>
      </div>
    </a>"""


def render_table(ranked, avoid, columns):
    heads = "".join(f"<th>{esc(c['label'])}</th>" for c in columns)
    rows = []
    for p in ranked:
        cells = "".join(f"<td>{spec_value(p, c)}</td>" for c in columns)
        rows.append(f'<tr><td class="c">{p["rank"]}</td>'
                    f'<td><a href="#{esc(p["asin"])}">{esc(p["brand"])} {esc(p["model"])}</a></td>'
                    f'<td>{money(p["price"])}</td><td class="c">{p["rating"]}</td>'
                    f'<td class="c">{p["reviews_count"]:,}</td><td>{sys_icons(p["systems"])}</td>{cells}<td class="c"><b>{p["score"]}</b></td></tr>')
    for a in avoid:
        rows.append(f'<tr class="avoid-row"><td class="c">&#10005;</td>'
                    f'<td><a href="#avoid-{esc(a["asin"])}">{esc(a["brand"])} {esc(a["model"])}</a></td>'
                    f'<td>{money(a["price"])}</td><td class="c">{a["rating"]}</td>'
                    f'<td class="c">{a["reviews_count"]:,}</td><td>{sys_icons(a["systems"])}</td>'
                    f'<td colspan="{len(columns)}">{esc(a["flag"])}</td><td class="c"><b>AVOID</b></td></tr>')
    return (f'<div class="tablewrap"><table class="ptable"><thead><tr><th>#</th><th>Switch</th><th>Price</th>'
            f'<th>Rating</th><th>Reviews</th><th>Works with</th>{heads}<th>Score</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def render_card(p, site, spec_fields):
    url = amazon_url(site, p["asin"])
    badges = "".join(f'<span class="badge {esc(a["kind"])}">{esc(a["label"])}</span>' for a in p["awards"])
    specs = "".join(f'<div class="spec"><dt>{esc(f["label"])}</dt><dd>{spec_value(p, f)}</dd></div>'
                    for f in spec_fields)
    pros = "".join(f"<li>{esc(x)}</li>" for x in p["pros"])
    cons = "".join(f"<li>{esc(x)}</li>" for x in p["cons"])
    bought = f'<div class="tiny muted">{esc(p["bought"])}</div>' if p.get("bought") else ""
    return f"""
    <article class="card{' awarded' if p['awards'] else ''}" id="{esc(p['asin'])}">
      <div class="rank">#{p['rank']}</div>
      <div class="card-head">
        <div class="card-img"><img src="{esc(p['image'])}" alt="{esc(p['name'])}" loading="lazy"></div>
        <div class="card-title">
          <div class="badges">{badges}</div>
          <div class="brand">{esc(p['brand'])}</div>
          <h3>{esc(p['name'])}</h3>
          <div class="rate">{stars(p['rating'])} <b>{p['rating']}</b> <span class="muted">{p['reviews_count']:,} reviews</span></div>
          <div class="scorebar"><span style="width:{p['score']}%"></span><em>Score {p['score']}/100</em></div>
        </div>
        <div class="card-buy">
          <div class="price">{money(p['price'])}</div>
          <a class="btn" href="{url}" target="_blank" rel="sponsored nofollow noopener">Check price on Amazon</a>
          {bought}
        </div>
      </div>
      <p class="verdict">{esc(p['verdict'])}</p>
      <dl class="specs">{specs}</dl>
      <div class="pc">
        <div class="pros"><h4>Pros</h4><ul>{pros}</ul></div>
        <div class="cons"><h4>Cons</h4><ul>{cons}</ul></div>
      </div>
    </article>"""


def render_avoid(avoid, site, noun):
    cards = []
    for a in avoid:
        reasons = "".join(f"<li>{esc(r)}</li>" for r in a["reasons"])
        cards.append(f"""
      <article class="avoid-card" id="avoid-{esc(a['asin'])}">
        <span class="avoid-flag">&#10005; Avoid</span>
        <div class="avoid-head">
          <div class="card-img"><img src="{esc(a['image'])}" alt="{esc(a['name'])}" loading="lazy"></div>
          <div class="card-title">
            <div class="brand">{esc(a['brand'])}</div>
            <h3>{esc(a['name'])}</h3>
            <div class="rate">{stars(a['rating'])} <b>{a['rating']}</b> <span class="muted">{a['reviews_count']:,} reviews &middot; {money(a['price'])}</span></div>
          </div>
        </div>
        <p class="verdict"><b>{esc(a['verdict'])}</b></p>
        <div class="reasons"><h4>Why we'd skip it</h4><ul>{reasons}</ul></div>
        <a class="btn ghost" href="{amazon_url(site, a['asin'])}" target="_blank" rel="sponsored nofollow noopener">See the listing on Amazon (so you recognize it)</a>
      </article>""")
    return f"""
  <section class="avoid" id="avoid">
    <h2>The one to avoid</h2>
    <p class="avoid-lead">This {esc(noun)} turns up in the search results but has problems serious enough that we'd keep looking.</p>
    {''.join(cards)}
  </section>"""


def render_family_links(site, cat):
    """Links to the same product type on the other protocols (e.g. every light-switch page)."""
    links = []
    for proto in site["protocols"]:
        for s in proto["subs"]:
            if s.get("ready") and s.get("family") == cat.get("family") and s["slug"] != cat["slug"]:
                links.append(f'<a class="sub-link" href="{esc(s["slug"])}.html">{esc(s["title"])} <span class="arrow">&rarr;</span></a>')
    if not links:
        return ""
    return f"""
  <section id="other">
    <h2>{esc(cat['family_title'])} on other protocols</h2>
    <div class="sub-grid flat">{''.join(links)}</div>
  </section>"""


def build_category(site, proto, sub):
    cat = load(f"pages/{sub['slug']}.json")
    ranked = rank_products(cat)
    by_asin = {p["asin"]: p for p in ranked}
    awards = "".join(render_award(a, by_asin[a["asin"]], site) for a in cat["awards"])
    cards = "".join(render_card(p, site, cat["spec_fields"]) for p in ranked)
    guide = "".join(f"<details><summary>{esc(g['q'])}</summary><p>{esc(g['a'])}</p></details>"
                    for g in cat["buyers_guide"])
    n = len(ranked)
    jump = ('<nav class="jump" aria-label="On this page"><a href="#picks" class="jump-all">Top picks</a>'
            '<a href="#compare">Compare</a><a href="#ranked">Full list</a>'
            + ('<a href="#avoid" class="avoid-link">Avoid</a>' if cat["avoid"] else "")
            + '<a href="#guide">Buyer\'s guide</a></nav>')
    body = f"""
  <nav class="crumbs"><a href="./">Home</a> &rsaquo; <a href="./#{esc(proto['slug'])}">{esc(proto['name'])}</a> &rsaquo; {esc(sub['title'])}</nav>
  <section class="lead">
    <h1>{esc(cat['title'])}</h1>
    <p class="sub">{esc(cat['subtitle'])}</p>
    <p class="intro">{esc(cat['intro'])}</p>
    <p class="muted tiny">Prices, ratings, and review counts captured from Amazon on {esc(cat['data_captured'])}.</p>
  </section>
  {jump}
  <section id="picks">
    <h2>Our picks</h2>
    <div class="heroes">{awards}</div>
  </section>
  <section id="compare">
    <h2>Side-by-side</h2>
    <p class="swipe-hint">Swipe the table sideways to see every column.</p>
    {render_table(ranked, cat['avoid'], cat['table_columns'])}
    <p class="tiny muted legend">Works with: hover or tap an icon for the system name. A system is shown when it supports the product directly or through the hub the listing requires.{(' ' + esc(cat['systems_note'])) if cat.get('systems_note') else ''}</p>
  </section>
  <section id="ranked">
    <h2>The full ranking</h2>
    <p class="group-sub">Scored out of 100: {round(cat['weights']['rating']*100)}% customer rating, {round(cat['weights']['reviews']*100)}% review volume, {round(cat['weights']['features']*100)}% features.</p>
    {cards}
  </section>
  {render_avoid(cat['avoid'], site, cat.get('noun', 'product')) if cat['avoid'] else ''}
  <section id="guide" class="guide">
    <h2>Buyer's guide</h2>
    {guide}
  </section>
  {render_family_links(site, cat)}"""
    base = base_url(site)
    url = f"{base}/{sub['slug']}.html" if base else ""
    items = {"@context": "https://schema.org", "@type": "ItemList", "name": cat["title"],
             "itemListElement": [{"@type": "ListItem", "position": p["rank"], "name": p["name"],
                                  "url": amazon_url(site, p["asin"])} for p in ranked]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": g["q"],
                           "acceptedAnswer": {"@type": "Answer", "text": g["a"]}} for g in cat["buyers_guide"]]}
    (OUT / f"{sub['slug']}.html").write_text(
        page(site, f"{cat['title']} ({cat['data_captured'][:4]}) | {site['brand']}", body,
             description=cat["intro"], canonical=url, structured_data=jsonld(items, faq),
             updated=cat["data_captured"]),
        encoding="utf-8")
    picks = ", ".join(f"{a['label']} = {by_asin[a['asin']]['brand']} {by_asin[a['asin']]['model']}" for a in cat["awards"])
    print(f"  {sub['slug']}: {n} products + {len(cat['avoid'])} avoid; {picks}")
    return url


def build_sitemap(site, urls):
    base = base_url(site)
    if not base:
        return
    locs = "".join(f"<url><loc>{esc(u)}</loc><lastmod>{esc(site['updated'])}</lastmod></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")


def main():
    site = load("site.json")
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "styles.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    if site.get("custom_domain"):
        (OUT / "CNAME").write_text(site["custom_domain"] + "\n", encoding="utf-8")
    build_home(site)
    print(f"Built home page with {len(site['protocols'])} protocols")
    urls = [f"{base_url(site)}/"]
    for proto in site["protocols"]:
        for sub in proto["subs"]:
            if sub.get("ready"):
                urls.append(build_category(site, proto, sub))
    build_sitemap(site, urls)
    print(f"{len(urls) - 1} category pages -> {OUT}")


CSS = r"""
:root{
  --bg:#0b0a17; --card:#15132a; --card-2:#1d1a38; --ink:#efe9dc; --muted:#a7a1bd; --line:#2c2850;
  --gold:#d8b25a; --gold-ink:#f0d48c; --purple:#7a5bc7; --purple-ink:#b9a3f0;
  --pro:#5fc98f; --con:#ff8a7a;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 12px 34px rgba(0,0,0,.55);
  --radius:14px; --max:1060px;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  background-image:radial-gradient(1200px 600px at 80% -10%,rgba(122,91,199,.18),transparent 60%);
  font:16px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
main{max-width:var(--max);margin:0 auto;padding:0 20px 40px}
h1,h2,.logo span{font-family:Cinzel,Georgia,serif;letter-spacing:.01em}
h1{font-size:2.1rem;line-height:1.15;margin:.2em 0}
h2{font-size:1.6rem;margin:2.2rem 0 1rem;color:var(--gold-ink)}
h3{margin:0 0 6px;font-size:1rem}
.muted{color:var(--muted)}
/* header */
header.site{max-width:var(--max);margin:0 auto;padding:16px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.logo{display:inline-flex;align-items:center;gap:12px}
.logo img{width:48px;height:48px;border-radius:50%;border:1px solid var(--gold)}
.logo span{font-size:1.4rem;color:var(--gold-ink)}
.slogan{color:var(--muted);font-size:.95rem}
.home-head{padding-top:20px}
.banner{display:block;line-height:0;width:100%;max-width:820px;margin:0 auto}
.banner img{width:100%;height:auto;border-radius:var(--radius);box-shadow:var(--shadow);border:1px solid var(--line)}
.notice{max-width:var(--max);margin:0 auto 8px;padding:8px 20px;color:var(--gold-ink);font-size:.85rem}
/* lead */
.lead{padding:14px 0 8px}
.lead .sub{font-size:1.15rem;color:var(--muted);margin:.3em 0;max-width:75ch}
.group-sub{color:var(--muted);margin:-6px 0 16px}
.section-head{margin-top:2.6rem}
/* jump bar */
.jump{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0}
.jump a{background:var(--card-2);border:1px solid var(--line);border-radius:20px;
  padding:6px 14px;font-size:.88rem;font-weight:600}
.jump a:hover{border-color:var(--gold);color:var(--gold-ink)}
.jump .jump-all{border-color:var(--purple);color:var(--purple-ink)}
/* comparison table */
.swipe-hint{display:none}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:var(--card)}
table{border-collapse:collapse;width:100%;min-width:860px;font-size:.88rem}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:rgba(122,91,199,.12);font-size:.76rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
td:first-child{white-space:nowrap;font-weight:700}
td:first-child a{color:var(--gold-ink)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover td{background:rgba(216,178,90,.04)}
/* protocol cards */
section[id]{scroll-margin-top:16px}
.proto{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);
  border-top:3px solid var(--gold);padding:22px 24px;margin:22px 0}
.proto-head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.proto-head h2{margin:0}
.proto-band{font-size:.8rem;color:var(--purple-ink);border:1px solid var(--line);
  background:var(--card-2);border-radius:20px;padding:2px 10px}
.proto-sum{margin:.6em 0 0;font-size:1.05rem}
.verdict{margin:14px 0 18px;padding:12px 16px;background:var(--card-2);
  border-left:3px solid var(--purple);border-radius:8px;color:var(--ink)}
.verdict b{color:var(--purple-ink)}
.pc{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.pc ul{margin:0;padding-left:20px} .pc li{margin:5px 0}
.pros h3{color:var(--pro)} .cons h3{color:var(--con)}
.pros li::marker{color:var(--pro)} .cons li::marker{color:var(--con)}
/* sub-section dropdown */
details.subs{margin:20px 0 0;border:1px solid var(--line);border-radius:10px;background:var(--card-2)}
details.subs>summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:10px;
  padding:12px 16px;font-weight:700;color:var(--gold-ink)}
details.subs>summary::-webkit-details-marker{display:none}
details.subs>summary::after{content:"";margin-left:auto;width:9px;height:9px;
  border-right:2px solid var(--gold);border-bottom:2px solid var(--gold);transform:rotate(45deg);transition:transform .15s}
details.subs[open]>summary::after{transform:rotate(-135deg)}
details.subs>summary:hover{color:var(--gold)}
details.subs>summary:focus-visible{outline:2px solid var(--gold);outline-offset:2px;border-radius:10px}
.count{font-size:.75rem;background:var(--purple);color:#fff;border-radius:20px;padding:1px 8px}
.sub-grid{list-style:none;margin:0;padding:4px 16px 16px;display:grid;
  grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px}
.sub-link{display:flex;align-items:center;justify-content:space-between;gap:8px;
  background:var(--card);border:1px solid var(--line);border-radius:9px;padding:10px 12px;font-size:.92rem}
a.sub-link{color:var(--gold-ink);border-color:rgba(216,178,90,.45)}
a.sub-link:hover{border-color:var(--gold);background:var(--card-2)}
.sub-link.soon{color:var(--muted)}
.soon-tag{flex:none;font-size:.68rem;text-transform:uppercase;letter-spacing:.04em;
  border:1px solid var(--line);border-radius:20px;padding:1px 8px}
/* footer */
footer{max-width:var(--max);margin:0 auto;padding:24px 20px 50px;border-top:1px solid var(--line)}
.disclosure{font-size:.85rem;color:var(--muted);max-width:80ch}
footer .muted{font-size:.85rem}
footer a{color:var(--gold-ink)}
.to-top{display:none}
/* systems */
.sys-icons{display:inline-flex;gap:3px;flex-wrap:nowrap;vertical-align:middle}
.sys-ico{position:relative;display:inline-flex;line-height:0;border-radius:5px;cursor:help;vertical-align:middle}
.sys-ico svg{display:block;border-radius:5px;box-shadow:0 0 0 1px rgba(255,255,255,.12)}
.sys-ico:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.sys-ico::after{content:attr(data-tip);position:absolute;left:50%;bottom:calc(100% + 7px);transform:translateX(-50%);
  background:#0b0a17;color:var(--ink);border:1px solid var(--gold);border-radius:6px;padding:4px 8px;
  font-size:.75rem;font-weight:600;line-height:1.2;white-space:nowrap;pointer-events:none;opacity:0;transition:opacity .12s;z-index:5}
.sys-ico:hover::after,.sys-ico:focus::after{opacity:1}
.ptable th,.ptable td{padding:10px 7px}
.ptable th:first-child,.ptable td:first-child{padding-left:12px}
.ptable td:nth-child(2){white-space:normal;min-width:130px}
.ptable td:nth-child(n+7){min-width:80px}
.ptable th{font-size:.7rem;letter-spacing:.02em}
.legend{margin:8px 0 0}
.sys-table{min-width:1000px}
.sys-table td{white-space:normal;font-size:.86rem}
.sys-table td:first-child{white-space:nowrap}
.sys-name{color:var(--gold-ink);font-weight:700;text-decoration:underline;text-decoration-color:rgba(216,178,90,.4);text-underline-offset:3px}
.sys-table .buy{min-width:170px}
.sys-table .buy a:not(.btn){color:var(--gold-ink)}
.btn.small{padding:6px 12px;font-size:.82rem;white-space:nowrap}
.btn.ghost-btn{background:var(--card-2);color:var(--ink);border:1px solid var(--line)}
.btn.ghost-btn:hover{border-color:var(--gold);filter:none}
.sys-sub{margin:26px 0 12px;font-size:1.1rem;color:var(--gold-ink)}
.sys-pc{min-width:760px}
.sys-pc td:nth-child(2),.sys-pc td:nth-child(3){width:45%}
.pc-list{margin:0;padding-left:18px} .pc-list li{margin:3px 0}
.pc-list.pros li::marker{color:var(--pro)} .pc-list.cons li::marker{color:var(--con)}
/* category pages */
.tiny{font-size:.8rem} .c{text-align:center}
.crumbs{font-size:.85rem;color:var(--muted);margin:4px 0 0} .crumbs a{color:var(--gold-ink)}
.lead .intro{max-width:75ch;margin:.6em 0}
.stars{--pct:100%;display:inline-block;width:88px;height:16px;vertical-align:-2px;
  background:linear-gradient(90deg,var(--gold) var(--pct),#3a3558 var(--pct));
  -webkit-mask-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='17.6' height='16' viewBox='0 0 20 20'%3E%3Cpath d='M10 1l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 14.9 4.8 17.6l1-5.8L1.5 7.7l5.9-.9z'/%3E%3C/svg%3E");
  mask-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='17.6' height='16' viewBox='0 0 20 20'%3E%3Cpath d='M10 1l2.6 5.3 5.9.9-4.3 4.1 1 5.8L10 14.9 4.8 17.6l1-5.8L1.5 7.7l5.9-.9z'/%3E%3C/svg%3E");
  -webkit-mask-size:17.6px 16px;mask-size:17.6px 16px;-webkit-mask-repeat:repeat-x;mask-repeat:repeat-x}
.btn{display:inline-block;background:var(--gold);color:#1a1405;font-weight:700;padding:9px 16px;border-radius:9px;font-size:.92rem}
.btn:hover{filter:brightness(1.08)}
.btn.ghost{background:transparent;color:var(--gold-ink);padding:6px 0}
.heroes{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin-top:20px}
.hero-card{display:flex;flex-direction:column;gap:10px;background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);
  padding:22px 18px 18px;border-top:4px solid var(--pro);position:relative;transition:transform .1s}
.hero-card:hover{transform:translateY(-2px)}
.hero-card img{width:100%;height:150px;object-fit:contain;background:#fff;border-radius:10px}
.hero-tag{position:absolute;top:-12px;left:16px;background:var(--pro);color:#08130c;font-size:.72rem;font-weight:800;
  letter-spacing:.04em;text-transform:uppercase;padding:3px 10px;border-radius:20px}
.hero-card.budget{border-top-color:#5b9bff} .hero-card.budget .hero-tag{background:#5b9bff;color:#06101f}
.hero-card.premium{border-top-color:var(--purple)} .hero-card.premium .hero-tag{background:var(--purple);color:#fff}
.hero-card.special{border-top-color:var(--gold)} .hero-card.special .hero-tag{background:var(--gold);color:#1a1405}
.hero-brand{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.hero-name{font-weight:700}
.hero-why{margin:4px 0 0;font-size:.9rem;color:var(--muted)}
.hero-price{font-size:1.4rem;font-weight:800;margin-top:auto}
.hero-card .btn{text-align:center}
.ptable{min-width:900px}
.ptable td{white-space:nowrap} .ptable td:nth-child(n+7){white-space:normal} .ptable td:first-child{font-weight:400}
.ptable a{color:var(--gold-ink);font-weight:600}
tr.avoid-row td{background:#2a1420;color:#ff9d94;font-weight:600;white-space:normal}
tr.avoid-row a{color:#ff9d94;text-decoration:underline}
.card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px;margin:18px 0;position:relative;overflow:hidden}
.card.awarded{border:1px solid rgba(216,178,90,.35)}
.rank{position:absolute;top:0;left:0;background:var(--ink);color:var(--bg);font-weight:800;font-size:.95rem;padding:4px 12px;border-bottom-right-radius:12px}
.card.awarded .rank{background:var(--gold)}
.card-head{display:grid;grid-template-columns:132px 1fr auto;gap:18px;align-items:start}
.card-img img{width:132px;height:132px;object-fit:contain;background:#fff;border-radius:10px}
.badges{display:flex;flex-wrap:wrap;gap:6px;min-height:4px}
.badge{display:inline-block;background:var(--pro);color:#08130c;font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.03em;padding:2px 9px;border-radius:20px}
.badge.budget{background:#5b9bff;color:#06101f} .badge.premium{background:var(--purple);color:#fff} .badge.special{background:var(--gold);color:#1a1405}
.card-title .brand{font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-top:6px}
.card-title h3{margin:.1em 0 .4em;font-size:1.08rem;line-height:1.35}
.rate b{margin:0 4px 0 6px}
.scorebar{position:relative;height:8px;background:var(--line);border-radius:6px;margin:12px 0 0;max-width:280px}
.scorebar span{position:absolute;left:0;top:0;bottom:0;background:linear-gradient(90deg,var(--purple),var(--gold));border-radius:6px}
.scorebar em{position:absolute;right:-2px;top:12px;font-size:.75rem;color:var(--muted);font-style:normal}
.card-buy{text-align:right}
.price{font-size:1.6rem;font-weight:800}
.card-buy .btn{margin:8px 0 6px}
.card .verdict{margin:22px 0 14px}
.specs{display:grid;grid-template-columns:repeat(4,1fr);gap:10px 18px;margin:0 0 16px;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.spec dt{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
.spec dd{margin:2px 0 0;font-weight:600;font-size:.92rem}
.pc h4{margin:0 0 6px} .pros h4{color:var(--pro)} .cons h4{color:var(--con)}
.avoid h2{color:#ff6b5c}
.avoid-lead{max-width:75ch;color:var(--muted)}
.avoid-card{position:relative;background:var(--card);border:2px solid #e0483c;border-radius:var(--radius);padding:22px;margin:18px 0;box-shadow:var(--shadow)}
.avoid-flag{position:absolute;top:-13px;left:18px;background:#c0261e;color:#fff;font-weight:800;font-size:.78rem;letter-spacing:.05em;text-transform:uppercase;padding:4px 14px;border-radius:20px}
.avoid-head{display:grid;grid-template-columns:110px 1fr;gap:16px;align-items:center}
.avoid-card .card-img img{width:110px;height:110px}
.avoid-card .verdict{background:none;border:0;padding:0;color:#ff9d94}
.reasons h4{margin:0 0 6px;color:#ff6b5c} .reasons ul{margin:0 0 16px;padding-left:20px} .reasons li{margin:6px 0}
.guide details{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:8px 0}
.guide summary{font-weight:700;cursor:pointer}
.guide details p{margin:.6em 0 0;color:var(--muted)}
.sub-grid.flat{padding:0}
@media (max-width:720px){
  .heroes{grid-template-columns:1fr}
  .card{padding:16px}
  .card-head{grid-template-columns:96px 1fr;gap:12px}
  .card-img img{width:96px;height:96px}
  .card-buy{grid-column:1/-1;display:grid;grid-template-columns:1fr auto;align-items:center;gap:8px 12px;text-align:left}
  .card-buy .price{font-size:1.45rem}
  .card-buy .btn{grid-row:2;grid-column:1/-1;text-align:center;padding:13px 16px;margin:0}
  .specs{grid-template-columns:repeat(2,1fr)}
  .ptable td:nth-child(2),.ptable th:nth-child(2){position:sticky;left:0;z-index:1;background:var(--card);white-space:normal;min-width:120px}
  .ptable th:nth-child(2){background:#1e1a3a}
  #compare .ptable tr>:first-child{position:static;box-shadow:none}
}
@media (max-width:720px){
  header.site{padding:10px 16px}
  .home-head{padding-top:12px}
  .slogan{display:none}
  main{padding:0 16px 32px}
  h1{font-size:1.6rem}
  h2{font-size:1.3rem;margin:1.8rem 0 .8rem}
  .lead .sub{font-size:1rem}
  .jump{flex-wrap:nowrap;overflow-x:auto;position:sticky;top:0;z-index:20;margin:12px -16px 0;
    padding:8px 16px;background:rgba(11,10,23,.94);backdrop-filter:blur(6px);
    border-bottom:1px solid var(--line);scrollbar-width:none}
  .jump::-webkit-scrollbar{display:none}
  .jump a{flex:none}
  section[id]{scroll-margin-top:60px}
  .swipe-hint{display:block;margin:-4px 0 8px;font-size:.8rem;color:var(--muted)}
  #compare tr>:first-child{position:sticky;left:0;z-index:1;background:var(--card);
    box-shadow:6px 0 8px -6px rgba(0,0,0,.9)}
  #compare th:first-child{background:#1e1a3a}
  .proto{padding:18px 16px}
  .pc{grid-template-columns:1fr}
  .sub-grid{grid-template-columns:1fr;padding:4px 12px 12px}
  .to-top{display:flex;align-items:center;justify-content:center;position:fixed;right:16px;bottom:18px;z-index:30;
    width:44px;height:44px;border-radius:50%;background:var(--gold);color:#1a1405;font-weight:800;font-size:1.2rem;
    box-shadow:0 4px 14px rgba(0,0,0,.6);opacity:0;pointer-events:none;transition:opacity .2s}
  .to-top.show{opacity:1;pointer-events:auto}
}
"""

if __name__ == "__main__":
    main()
