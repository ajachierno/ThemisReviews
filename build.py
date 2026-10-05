"""ThemisReviews static site generator.

Reads data/site.json and writes the static site into docs/ for GitHub Pages.
Zero dependencies. Run:  python build.py
"""
import datetime
import html
import json
import math
import re
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
         structured_data="", updated=None, noindex=False, image=None):
    desc = description or site["description"]
    base = base_url(site)
    image = image or (f"{base}/assets/logo.jpg" if base else "assets/logo.jpg")
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    pin_tag = (f'\n<meta name="p:domain_verify" content="{esc(site["pinterest_verify"])}">'
               if site.get("pinterest_verify") else "")
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
<meta name="robots" content="{robots}">{canonical_tag}
<meta name="theme-color" content="#0b0a17">{pin_tag}
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
{REVEAL_JS}
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


def sys_icons(slugs, empty_label="Standalone"):
    if not slugs:
        return f'<span class="tiny muted">{esc(empty_label)}</span>'
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
    def facts(s):
        items = [("Hub", s["hub"]), ("Radios", s["radios"]), ("Runs locally", s["local"]), ("Phones", s["phones"])]
        return "".join(f'<div class="fact"><span>{esc(k)}</span>{esc(v)}</div>' for k, v in items)
    rows = "".join(f"""<tr>
        <td class="sys-cell"><span class="sys-head">{sys_icon(s['slug'])} <a class="sys-name" href="{esc(s['site'])}" target="_blank" rel="noopener">{esc(s['name'])}</a></span>
          <div class="tiny muted">{esc(s['maker'])}</div><div class="best-for"><span>Best for</span>{esc(s['best_for'])}</div></td>
        <td><ul class="pc-list pros">{''.join(f'<li>{esc(x)}</li>' for x in s['pros'])}</ul></td>
        <td><ul class="pc-list cons">{''.join(f'<li>{esc(x)}</li>' for x in s['cons'])}</ul></td>
        <td class="facts">{facts(s)}</td>
        <td class="buy">{buy_cell(site, s)}</td></tr>""" for s in systems)
    return f"""
  <section id="systems">
    <h2>Start with your system</h2>
    <p class="group-sub">The system is the app and hub that runs everything. It decides which protocols you can use, so pick it before you buy switches and sensors. Names link to each system's site; prices are from Amazon on {esc(data['data_captured'])}.</p>
    <p class="swipe-hint">Swipe the table sideways to see every column.</p>
    <div class="tablewrap"><table class="sys-table">
      <thead><tr><th>System</th><th>Pros</th><th>Cons</th><th>Setup</th><th>Where to buy</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
  </section>"""


def render_quicknav(protocols, compact=False, current=None, families=None):
    """Protocol dropdown -> review dropdown -> Go. Planned pages show as disabled options.
    compact: slim toolbar for category pages (no heading, adds a Home button).
    current: (protocol_slug, page_slug) to preselect on a category page."""
    data = {p["slug"]: [{"slug": x["slug"], "title": x["title"], "ready": bool(x.get("ready"))} for x in p["subs"]]
            for p in protocols}
    opts = "".join(f'<option value="{esc(p["slug"])}">{esc(p["name"])}</option>' for p in protocols)
    js = """(function(){
  var subs = __DATA__;
  var proto = document.getElementById('qn-protocol'), sub = document.getElementById('qn-review'), go = document.getElementById('qn-go');
  function fill(){
    var list = subs[proto.value] || [];
    sub.innerHTML = '<option value="">Choose a review\u2026</option>';
    list.forEach(function(x){
      var o = document.createElement('option');
      o.value = x.ready ? x.slug : '';
      o.textContent = x.ready ? x.title : x.title + ' (coming soon)';
      o.disabled = !x.ready;
      sub.appendChild(o);
    });
    sub.disabled = !list.length; go.disabled = true;
  }
  function open(){ if(sub.value){ window.location.href = sub.value + '.html'; } }
  proto.addEventListener('change', fill);
  sub.addEventListener('change', function(){ go.disabled = !sub.value; });
  var cur = __CURRENT__;
  if(cur){ proto.value = cur[0]; fill(); sub.value = cur[1]; go.disabled = true; }
  sub.addEventListener('keydown', function(e){ if(e.key === 'Enter'){ open(); } });
  go.addEventListener('click', open);
})();""".replace("__DATA__", json.dumps(data)).replace("__CURRENT__", json.dumps(list(current) if current else None))
    if compact:
        return f"""
  <nav class="quicknav quicknav-bar" aria-label="Jump straight to reviews">
    <div class="quicknav-controls">
      <a class="back-home" href="./">&larr; Home</a>
      <select id="qn-protocol" aria-label="Protocol">
        <option value="">Choose a protocol&hellip;</option>
        {opts}
      </select>
      <select id="qn-review" aria-label="Review" disabled>
        <option value="">Choose a review&hellip;</option>
      </select>
      <button type="button" id="qn-go" class="btn" disabled>Go</button>
    </div>
    <script>{js}</script>
  </nav>"""
    type_opts = "".join(f'<option value="{esc(slug)}">{esc(title)}</option>' for _f, title, slug, _m in (families or []))
    type_js = """(function(){
  var t=document.getElementById('qn-type'), g=document.getElementById('qn-type-go');
  var modes=document.querySelectorAll('input[name=qn-mode]');
  function setMode(){
    var m=document.querySelector('input[name=qn-mode]:checked').value;
    document.getElementById('qn-by-protocol').hidden = m!=='protocol';
    document.getElementById('qn-by-type').hidden = m!=='type';
  }
  modes.forEach(function(r){ r.addEventListener('change', setMode); });
  t.addEventListener('change', function(){ g.disabled=!t.value; });
  function open(){ if(t.value){ window.location.href=t.value+'.html'; } }
  g.addEventListener('click', open);
  t.addEventListener('keydown', function(e){ if(e.key==='Enter'){ open(); } });
  setMode();
})();"""
    type_ui = f"""
    <div class="qn-modes" role="radiogroup" aria-label="Search by">
      <span class="qn-modes-label">Search by</span>
      <label><input type="radio" name="qn-mode" value="protocol" checked> Protocol</label>
      <label><input type="radio" name="qn-mode" value="type"> Product type</label>
    </div>""" if families else ""
    type_controls = f"""
    <div class="quicknav-controls" id="qn-by-type" hidden>
      <select id="qn-type" aria-label="Product type">
        <option value="">Choose a product type&hellip;</option>
        {type_opts}
      </select>
      <button type="button" id="qn-type-go" class="btn" disabled>Go</button>
    </div>
    <script>{type_js}</script>""" if families else ""
    return f"""
  <section class="quicknav" aria-labelledby="qn-h">
    <h2 id="qn-h">Jump straight to reviews</h2>{type_ui}
    <div class="quicknav-controls" id="qn-by-protocol">
      <select id="qn-protocol" aria-label="Protocol">
        <option value="">Choose a protocol&hellip;</option>
        {opts}
      </select>
      <select id="qn-review" aria-label="Review" disabled>
        <option value="">Choose a review&hellip;</option>
      </select>
      <button type="button" id="qn-go" class="btn" disabled>Go</button>
    </div>
    <script>{js}</script>{type_controls}
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
  {render_seasonal_strip()}
  {render_quicknav(protos, families=family_index(site))}
  <div class="or-divider" role="separator">- OR -</div>
  <p class="or-note">Not sure where to start? Explore the pros and cons of each smart home system and protocol below, then dive into the reviews that fit your setup.</p>
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


def render_table(ranked, avoid, columns, noun="product"):
    heads = "".join(f"<th>{esc(c['label'])}</th>" for c in columns)
    rows = []
    for p in ranked:
        cells = "".join(f"<td>{spec_value(p, c)}</td>" for c in columns)
        rows.append(f'<tr><td class="c">{p["rank"]}</td>'
                    f'<td><a href="#{esc(p["asin"])}">{esc(p["brand"])} {esc(p["model"])}</a></td>'
                    f'<td>{money(p["price"])}</td><td class="c">{p["rating"]}</td>'
                    f'<td class="c">{p["reviews_count"]:,}</td><td>{sys_icons(p["systems"], p.get("systems_label", "Standalone"))}</td>{cells}<td class="c"><b>{p["score"]}</b></td></tr>')
    for a in avoid:
        rows.append(f'<tr class="avoid-row"><td class="c">&#10005;</td>'
                    f'<td><a href="#avoid-{esc(a["asin"])}">{esc(a["brand"])} {esc(a["model"])}</a></td>'
                    f'<td>{money(a["price"])}</td><td class="c">{a["rating"]}</td>'
                    f'<td class="c">{a["reviews_count"]:,}</td><td>{sys_icons(a["systems"], a.get("systems_label", "Standalone"))}</td>'
                    f'<td colspan="{len(columns)}">{esc(a["flag"])}</td><td class="c"><b>AVOID</b></td></tr>')
    return (f'<div class="tablewrap"><table class="ptable"><thead><tr><th>#</th><th>{esc(noun.capitalize())}</th><th>Price</th>'
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


def render_sibling_links(proto, cat):
    """Links to the other finished review pages for the same protocol (e.g. Z-Wave switches <-> dimmers)."""
    links = [f'<a class="sub-link" href="{esc(s["slug"])}.html">{esc(s["title"])} <span class="arrow">&rarr;</span></a>'
             for s in proto["subs"] if s.get("ready") and s["slug"] != cat["slug"]]
    if not links:
        return ""
    return f"""
  <section id="more">
    <h2>More {esc(proto['name'])} reviews</h2>
    <div class="sub-grid flat">{''.join(links)}</div>
  </section>"""


def render_family_links(site, cat):
    """Links to the same product type on the other protocols (e.g. every light-switch page),
    plus the all-protocols product-type page."""
    links = []
    if cat.get("family_title"):
        links.append(f'<a class="sub-link fam-all" href="{esc(family_slug(cat["family_title"]))}.html">Compare all '
                     f'{esc(family_display(cat["family_title"]).lower())} on one page <span class="arrow">&rarr;</span></a>')
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
  {render_quicknav(site["protocols"], compact=True, current=(proto["slug"], sub["slug"]))}
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
    {render_table(ranked, cat['avoid'], cat['table_columns'], cat.get('noun', 'product'))}
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
  {render_sibling_links(proto, cat)}
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
    return url, cat["data_captured"]


# --------------------------------------------------------------------------- seasonal pages
# Gift guides and the Black Friday price-to-beat page, generated from the ranked category
# pages so every pick stays in step with its page. Copy lives in data/seasonal.json.
SEASONAL = json.loads((DATA / "seasonal.json").read_text(encoding="utf-8")) if (DATA / "seasonal.json").exists() else {}

REVEAL_JS = ("<script>document.querySelectorAll('[data-show-from]').forEach(function(e){"
             "var p=e.getAttribute('data-show-from').split('-');"
             "if(new Date()>=new Date(+p[0],p[1]-1,+p[2]))e.hidden=false;});</script>")


def seasonal_pages():
    """[(slug, label, link_from)] of enabled seasonal pages."""
    out = [(g["slug"], g.get("label") or g["title"], g.get("link_from"))
           for g in SEASONAL.get("gifts", []) if g.get("enabled")]
    bf = SEASONAL.get("black_friday")
    if bf and bf.get("enabled"):
        out.append((bf["slug"], bf.get("label") or bf["title"], bf.get("link_from")))
    return out


def reveal_attr(link_from):
    """Hide a link until link_from (YYYY-MM-DD). The page stays live and in the sitemap;
    REVEAL_JS un-hides the link on the day, and builds after that date render it plainly."""
    if not link_from or datetime.date.today() >= datetime.date.fromisoformat(link_from):
        return ""
    return f' hidden data-show-from="{esc(link_from)}"'


def render_seasonal_strip(current=None):
    pages = [(s, t, lf) for s, t, lf in seasonal_pages() if s != current]
    if not pages:
        return ""
    links = "".join(f'<a class="sub-link" href="{esc(s)}.html"{reveal_attr(lf)}>{esc(t)} <span class="arrow">&rarr;</span></a>'
                    for s, t, lf in pages)
    head = "More holiday guides" if current else "Holiday gift guides"
    return f"""
  <section class="seasonal-strip" id="gift-guides">
    <h2>{head}</h2>
    <p class="group-sub">Our top-ranked smart home picks, sorted by budget.</p>
    <div class="sub-grid flat">{links}</div>
  </section>"""


def ranked_pages(site):
    """[(proto, sub, cat)] for every ready page, ranked, in site order."""
    out = []
    for proto in site["protocols"]:
        for sub in proto["subs"]:
            if sub.get("ready"):
                cat = load(f"pages/{sub['slug']}.json")
                rank_products(cat)
                out.append((proto, sub, cat))
    return out


def family_order(pages):
    order = []
    for _p, _s, cat in pages:
        if cat.get("family") not in order:
            order.append(cat.get("family"))
    return order


def render_pick_card(p, cat, sub, site, label=None, note=""):
    url = amazon_url(site, p["asin"])
    tag = f'<span class="badge {esc(label[1])}">{esc(label[0])}</span>' if label else ""
    return f"""
    <article class="card pick-card" id="{esc(sub['slug'])}">
      <div class="card-head">
        <div class="card-img"><img src="{esc(p['image'])}" alt="{esc(p['name'])}" loading="lazy"></div>
        <div class="card-title">
          <div class="badges">{tag}</div>
          <div class="brand">{esc(sub['title'])} &middot; {esc(p['brand'])}</div>
          <h3>{esc(p['brand'])} {esc(p['model'])}</h3>
          <div class="rate">{stars(p['rating'])} <b>{p['rating']}</b> <span class="muted">{p['reviews_count']:,} reviews &middot; score {p['score']}/100</span></div>
          <div class="works">Works with: {sys_icons(p['systems'], p.get('systems_label', 'Standalone'))}</div>
        </div>
        <div class="card-buy">
          <div class="price">{money(p['price'])}</div>
          <a class="btn" href="{url}" target="_blank" rel="sponsored nofollow noopener">Check today's price</a>
          <div class="tiny muted">{note}</div>
        </div>
      </div>
      <p class="verdict">{esc(p['verdict'])}</p>
      <p class="tiny"><a class="pick-more" href="{esc(sub['slug'])}.html#{esc(p['asin'])}">Ranked #{p['rank']} of {len(cat['products'])} on our {esc(sub['title'])} page &rarr;</a></p>
    </article>"""


def render_faq(items):
    return "".join(f"<details><summary>{esc(g['q'])}</summary><p>{esc(g['a'])}</p></details>" for g in items)


def write_hub(site, cfg, body, dates, extra=None, image=None):
    base = base_url(site)
    canonical = f"{base}/{cfg['slug']}.html" if base else ""
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
        for q in cfg.get("faq", [])]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": site["brand"], "item": f"{base}/"},
        {"@type": "ListItem", "position": 2, "name": cfg["title"], "item": canonical}]}
    updated = max(dates) if dates else site["updated"]
    sd = jsonld(*[x for x in (crumbs, extra, faq) if x])
    (OUT / f"{cfg['slug']}.html").write_text(
        page(site, f"{cfg['title']} | {site['brand']}", body, description=cfg["subtitle"],
             canonical=canonical, structured_data=sd, updated=updated,
             noindex=bool(cfg.get("noindex")), image=image), encoding="utf-8")
    return canonical, updated


def gift_pick(pages, family, lo, hi, min_reviews, min_rating=0, used=(), skip_pages=(), skip_asins=()):
    """Best-scoring product in [lo, hi] across every page in the family, skipping ASINs
    already picked for another family (kits show up on more than one page)."""
    pool = []
    for proto, sub, cat in pages:
        if cat.get("family") != family or sub["slug"] in skip_pages:
            continue
        for p in cat["products"]:
            if (lo <= p["price"] <= hi and p["reviews_count"] >= min_reviews and p["rating"] >= min_rating
                    and p["asin"] not in used and p["asin"] not in skip_asins and p["brand"].lower() not in ("generic", "unbranded")):
                pool.append((p["score"], p["reviews_count"], p, cat, sub))
    if not pool:
        return None
    pool.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return pool[0][2:]


def gift_picks(pages, cfg):
    lo, hi = cfg.get("min_price", 0), cfg["max_price"]
    out, used = [], set()
    for fam in family_order(pages):
        pick = gift_pick(pages, fam, lo, hi, cfg.get("min_reviews", 0), cfg.get("min_rating", 0), used,
                         set(SEASONAL.get("gift_skip_pages", [])), set(SEASONAL.get("gift_skip_asins", [])))
        if pick:
            used.add(pick[0]["asin"])
            out.append(pick)
    return out


def build_gift_page(site, cfg, pages):
    picks = gift_picks(pages, cfg)
    dates = [cat["data_captured"] for _p, cat, _s in picks]
    cards = "".join(
        f'<h2 class="pick-family">{esc(cat.get("family_title", ""))}</h2>'
        + render_pick_card(p, cat, sub, site, note=f"price on {esc(cat['data_captured'])}")
        for p, cat, sub in picks)
    span = (f"between {esc(min(dates))} and {esc(max(dates))}" if dates and min(dates) != max(dates)
            else f"on {esc(dates[0])}" if dates else "")
    body = f"""
  {render_quicknav(site["protocols"], compact=True)}
  <nav class="crumbs"><a href="./">Home</a> &rsaquo; {esc(cfg['label'])}</nav>
  <section class="lead">
    <h1>{esc(cfg['title'])}</h1>
    <p class="sub">{esc(cfg['subtitle'])}</p>
    <p class="intro">{esc(cfg['intro'])}</p>
    <p class="muted tiny">{len(picks)} gifts, one per device type. Prices were captured from Amazon {span} and change often, so check the live price before you buy.</p>
  </section>
  <section id="gifts">{cards}</section>
  <section class="guide" id="guide"><h2>Gift-buying questions</h2>{render_faq(cfg.get('faq', []))}</section>
  {render_seasonal_strip(cfg['slug'])}"""
    base = base_url(site)
    items = {"@context": "https://schema.org", "@type": "ItemList", "name": cfg["title"],
             "numberOfItems": len(picks), "itemListElement": [
                 {"@type": "ListItem", "position": i, "name": f"{p['brand']} {p['model']}",
                  "url": f"{base}/{sub['slug']}.html#{p['asin']}"} for i, (p, _c, sub) in enumerate(picks, 1)]}
    print(f"  {cfg['slug']}: {len(picks)} gifts")
    return write_hub(site, cfg, body, dates, items, picks[0][0]["image"] if picks else None)


def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d:%A, %B} {d.day}, {d.year}"


def page_overall_budget(cat):
    by = {p["asin"]: p for p in cat["products"]}
    ov = next((by[a["asin"]] for a in cat.get("awards", []) if a["kind"] == "overall" and a["asin"] in by), None)
    bu = next((by[a["asin"]] for a in cat.get("awards", []) if a["kind"] == "budget" and a["asin"] in by), None)
    ranked = sorted(cat["products"], key=lambda p: p["rank"])
    return ov or (ranked[0] if ranked else None), bu


def build_black_friday(site, cfg, pages):
    rows, dates, sections = [], [], []
    for fam in family_order(pages):
        cards, fam_title = [], ""
        for proto, sub, cat in pages:
            if cat.get("family") != fam:
                continue
            fam_title = cat.get("family_title", "")
            ov, bu = page_overall_budget(cat)
            if not ov:
                continue
            dates.append(cat["data_captured"])
            rows.append((sub, ov, bu))
            cards.append(render_pick_card(ov, cat, sub, site, ("Best Overall", "overall"),
                                          f"regular price on {esc(cat['data_captured'])}"))
        if cards:
            sections.append(f'<h2 class="pick-family">{esc(fam_title)}</h2>{"".join(cards)}')
    table = "".join(
        f'<tr><td><a href="#{esc(sub["slug"])}">{esc(sub["title"])}</a></td>'
        f'<td>{esc(ov["brand"])} {esc(ov["model"])}</td><td>{money(ov["price"])}</td>'
        f'<td>{(esc(bu["brand"]) + " " + esc(bu["model"])) if bu and bu is not ov else "&mdash;"}</td>'
        f'<td>{money(bu["price"]) if bu and bu is not ov else "&mdash;"}</td></tr>'
        for sub, ov, bu in rows)
    body = f"""
  {render_quicknav(site["protocols"], compact=True)}
  <nav class="crumbs"><a href="./">Home</a> &rsaquo; {esc(cfg['label'])}</nav>
  <section class="lead">
    <h1>{esc(cfg['title'])}</h1>
    <p class="sub">{esc(cfg['subtitle'])}</p>
    <p class="intro">{esc(cfg['intro'])}</p>
  </section>
  <section class="guide">
    <h2>Key dates</h2>
    <p><b>Black Friday:</b> {long_date(cfg['black_friday'])}. <b>Cyber Monday:</b> {long_date(cfg['cyber_monday'])}.
    Early deals usually start the week before. Every button below opens the live Amazon listing,
    so you see today's price next to the regular price we recorded.</p>
  </section>
  <section id="price-to-beat">
    <h2>Price-to-beat cheat sheet</h2>
    <p class="swipe-hint">Swipe the table sideways to see every column.</p>
    <div class="tablewrap"><table class="ptable"><thead><tr><th>Page</th><th>Best Overall</th><th>Regular</th>
      <th>Best Budget</th><th>Regular</th></tr></thead><tbody>{table}</tbody></table></div>
    <p class="tiny muted">"Regular" is the Amazon price when we last checked each page
    ({esc(min(dates))} to {esc(max(dates))}). If the Black Friday price is at or above it, it isn't a deal.</p>
  </section>
  <section id="picks">{"".join(sections)}</section>
  <section class="guide" id="guide"><h2>Black Friday smart home questions</h2>{render_faq(cfg.get('faq', []))}</section>
  {render_seasonal_strip(cfg['slug'])}"""
    print(f"  {cfg['slug']}: {len(rows)} pages (on-site links hidden until {cfg.get('link_from')})")
    return write_hub(site, cfg, body, dates)


def build_seasonal(site):
    """Build enabled seasonal pages; returns [(url, lastmod)] for the sitemap (noindex pages left out)."""
    pages = ranked_pages(site)
    urls = []
    for g in SEASONAL.get("gifts", []):
        if g.get("enabled"):
            u = build_gift_page(site, g, pages)
            if not g.get("noindex"):
                urls.append(u)
    bf = SEASONAL.get("black_friday")
    if bf and bf.get("enabled"):
        u = build_black_friday(site, bf, pages)
        if not bf.get("noindex"):
            urls.append(u)
    return urls


# --------------------------------------------------------------------------- product-type pages
# One page per device family (light switches, locks, ...) that puts every product from every
# protocol page into a single table, filterable by protocol and smart home system.

def family_display(title):
    """'Light switches' -> 'Smart Light Switches'; 'Smart plugs' -> 'Smart Plugs'."""
    words = title.split()
    small = {"and", "or", "of"}
    keep = {"CO"}
    out = [w if w in keep else (w.lower() if w.lower() in small and i else w[0].upper() + w[1:]) for i, w in enumerate(words)]
    t = " ".join(out)
    return t if t.lower().startswith("smart") else f"Smart {t}"


def family_slug(title):
    return re.sub(r"[^a-z0-9]+", "-", family_display(title).lower()).strip("-")


def family_index(site):
    """[(family, display_title, slug, [(proto, sub)])] in site order, ready pages only."""
    fams = {}
    order = []
    for proto in site["protocols"]:
        for sub in proto["subs"]:
            if sub.get("ready") and sub.get("family"):
                if sub["family"] not in fams:
                    fams[sub["family"]] = []
                    order.append(sub["family"])
                fams[sub["family"]].append((proto, sub))
    out = []
    for fam in order:
        title = load(f"pages/{fams[fam][0][1]['slug']}.json").get("family_title", fam)
        out.append((fam, family_display(title), family_slug(title), fams[fam]))
    return out


def render_proto_diff(protocols):
    cards = "".join(
        f'''<div class="diff-card">
      <div class="diff-head"><b>{esc(p["name"])}</b> <span class="tiny muted">{esc(p["facts"].get("band", ""))}</span></div>
      <div class="pc">
        <div class="pros"><h4>Pros</h4><ul>{"".join(f"<li>{esc(x)}</li>" for x in p["pros"])}</ul></div>
        <div class="cons"><h4>Cons</h4><ul>{"".join(f"<li>{esc(x)}</li>" for x in p["cons"])}</ul></div>
      </div>
      <p class="verdict"><b>Our take:</b> {esc(p["verdict"])}</p>
    </div>'''
        for p in protocols)
    return f"""
  <details class="proto-diff">
    <summary>How do these protocols differ? <span class="muted">Show the pros and cons</span></summary>
    {cards}
    <p class="tiny"><a href="./#compare">See the full protocol comparison on the home page &rarr;</a></p>
  </details>"""


FAMILY_JS = """(function(){
  var proto=document.getElementById('f-proto'), sys=document.getElementById('f-sys'), sort=document.getElementById('f-sort');
  var body=document.getElementById('fam-body'), count=document.getElementById('f-count');
  var rows=[].slice.call(body.querySelectorAll('tr'));
  function apply(){
    var p=proto.value, s=sys.value, shown=0;
    rows.forEach(function(r){
      var ok=(!p||(' '+r.dataset.protos+' ').indexOf(' '+p+' ')>=0)&&(!s||(' '+r.dataset.systems+' ').indexOf(' '+s+' ')>=0);
      r.hidden=!ok; if(ok&&!r.classList.contains('avoid-row')) shown++;
    });
    count.textContent=shown+' of '+rows.filter(function(r){return !r.classList.contains('avoid-row');}).length+' products';
  }
  function order(){
    var k=sort.value;
    var sorted=rows.slice().sort(function(a,b){
      if(a.classList.contains('avoid-row')!==b.classList.contains('avoid-row')) return a.classList.contains('avoid-row')?1:-1;
      var x=+a.dataset[k], y=+b.dataset[k];
      return k==='price'? x-y : y-x;
    });
    sorted.forEach(function(r){body.appendChild(r);});
  }
  proto.addEventListener('change',apply); sys.addEventListener('change',apply);
  sort.addEventListener('change',function(){order();apply();});
  var q=new URLSearchParams(location.search);
  if(q.get('protocol')) proto.value=q.get('protocol');
  if(q.get('system')) sys.value=q.get('system');
  apply();
})();"""


def build_family_page(site, fam, title, slug, members):
    protos_here = []
    for proto, _sub in members:
        if proto not in protos_here:
            protos_here.append(proto)
    items = {}
    avoids = []
    dates = []
    for proto, sub in members:
        cat = load(f"pages/{sub['slug']}.json")
        rank_products(cat)
        dates.append(cat["data_captured"])
        for p in cat["products"]:
            it = items.setdefault(p["asin"], {"p": p, "protos": [], "pages": []})
            if proto["slug"] not in [x["slug"] for x in it["protos"]]:
                it["protos"].append(proto)
            it["pages"].append((sub, p["rank"], len(cat["products"])))
        for a in cat.get("avoid", []):
            avoids.append((a, proto, sub))
    ranked = sorted(items.values(), key=lambda it: (-it["p"]["score"], -it["p"]["reviews_count"]))
    sys_order = [s for s in SYSTEM_NAMES]

    def row(p, protos, link, extra_cls="", note=""):
        proto_chips = " ".join(f'<span class="chip">{esc(x["name"])}</span>' for x in protos)
        return (f'<tr class="{extra_cls}" data-protos="{esc(" ".join(x["slug"] for x in protos))}" '
                f'data-systems="{esc(" ".join(p.get("systems", [])))}" data-score="{p.get("score", 0)}" '
                f'data-price="{p["price"]}" data-rating="{p["rating"]}" data-reviews="{p["reviews_count"]}">'
                f'<td><a href="{esc(link)}">{esc(p["brand"])} {esc(p["model"])}</a>{note}</td>'
                f'<td>{proto_chips}</td><td>{money(p["price"])}</td><td class="c">{p["rating"]}</td>'
                f'<td class="c">{p["reviews_count"]:,}</td>'
                f'<td>{sys_icons(p.get("systems", []), p.get("systems_label", "Standalone"))}</td>'
                f'<td class="c"><b>{p.get("score", "&mdash;") if not extra_cls else "AVOID"}</b></td>'
                f'<td><a class="btn btn-sm" href="{amazon_url(site, p["asin"])}" target="_blank" rel="sponsored nofollow noopener">Amazon</a></td></tr>')

    rows = []
    for it in ranked:
        sub, rank, n = it["pages"][0]
        rows.append(row(it["p"], it["protos"], f'{sub["slug"]}.html#{it["p"]["asin"]}'))
    for a, proto, sub in avoids:
        rows.append(row(a, [proto], f'{sub["slug"]}.html#avoid-{a["asin"]}', "avoid-row",
                        f'<div class="tiny avoid-note">{esc(a.get("flag", ""))}</div>'))
    proto_links = "".join(f'<a class="sub-link" href="{esc(sub["slug"])}.html">{esc(sub["title"])} <span class="arrow">&rarr;</span></a>'
                          for _proto, sub in members)
    proto_opts = "".join(f'<option value="{esc(p["slug"])}">{esc(p["name"])}</option>' for p in protos_here)
    sys_opts = "".join(f'<option value="{esc(s)}">{esc(SYSTEM_NAMES[s])}</option>' for s in sys_order)
    multi = len(protos_here) > 1
    h1 = f"{title} Compared Across Every Protocol" if multi else f"{title}: Every Pick We Rank"
    noun = title.lower().replace("smart ", "", 1)
    n_items = len(ranked)
    intro = (f"All {n_items} {noun} we rank, from {len(members)} review pages, in one table. "
             f"Filter by the smart home system you use or by protocol, then open a product to see its full review."
             if multi else
             f"All {n_items} {noun} we rank, in one table you can filter by smart home system. "
             f"Open a product to see its full review.")
    body = f"""
  {render_quicknav(site["protocols"], compact=True)}
  <nav class="crumbs"><a href="./">Home</a> &rsaquo; {esc(title)}</nav>
  <section class="lead">
    <h1>{esc(h1)}</h1>
    <p class="intro">{esc(intro)}</p>
  </section>
  <section class="fam-protos">
    <h2 class="h-small">{esc(title)} by protocol</h2>
    <div class="sub-grid flat">{proto_links}</div>
    {render_proto_diff(protos_here)}
  </section>
  <section id="all">
    <h2>All {esc(noun)}</h2>
    <div class="fam-filters">
      <label>Protocol <select id="f-proto"{'' if multi else ' disabled'}><option value="">All protocols</option>{proto_opts}</select></label>
      <label>Works with <select id="f-sys"><option value="">Any system</option>{sys_opts}</select></label>
      <label>Sort by <select id="f-sort"><option value="score">Score</option><option value="rating">Rating</option><option value="reviews">Reviews</option><option value="price">Price (low to high)</option></select></label>
      <span class="muted tiny" id="f-count"></span>
    </div>
    <p class="swipe-hint">Swipe the table sideways to see every column.</p>
    <div class="tablewrap"><table class="ptable fam-table"><thead><tr><th>Product</th><th>Protocol</th><th>Price</th><th>Rating</th>
      <th>Reviews</th><th>Works with</th><th>Score</th><th></th></tr></thead>
      <tbody id="fam-body">{"".join(rows)}</tbody></table></div>
    <p class="tiny muted legend">Scores come from each product's protocol page, where it was ranked against devices on the same protocol. Red rows are the picks we tell you to avoid. Prices captured from Amazon between {esc(min(dates))} and {esc(max(dates))}.</p>
  </section>
  <script>{FAMILY_JS}</script>"""
    base = base_url(site)
    url = f"{base}/{slug}.html" if base else ""
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": h1, "numberOfItems": len(ranked),
          "itemListElement": [{"@type": "ListItem", "position": i, "name": f'{it["p"]["brand"]} {it["p"]["model"]}',
                               "url": f'{base}/{it["pages"][0][0]["slug"]}.html#{it["p"]["asin"]}'} for i, it in enumerate(ranked, 1)]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": site["brand"], "item": f"{base}/"},
        {"@type": "ListItem", "position": 2, "name": title, "item": url}]}
    (OUT / f"{slug}.html").write_text(
        page(site, f"{h1} | {site['brand']}", body, description=intro, canonical=url,
             structured_data=jsonld(crumbs, il), updated=max(dates)), encoding="utf-8")
    return url, max(dates)


def build_family_pages(site):
    urls = []
    for fam, title, slug, members in family_index(site):
        urls.append(build_family_page(site, fam, title, slug, members))
    print(f"  {len(urls)} product-type pages")
    return urls


def build_sitemap(site, urls):
    base = base_url(site)
    if not base:
        return
    locs = "".join(f"<url><loc>{esc(u)}</loc><lastmod>{esc(d)}</lastmod></url>" for u, d in urls)
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
    urls = [(f"{base_url(site)}/", site["updated"])]
    for proto in site["protocols"]:
        for sub in proto["subs"]:
            if sub.get("ready"):
                urls.append(build_category(site, proto, sub))
    n_cat = len(urls) - 1
    fam = build_family_pages(site)
    seas = build_seasonal(site)
    urls += fam + seas
    build_sitemap(site, urls)
    print(f"{n_cat} category pages + {len(fam)} product-type pages + {len(seas)} seasonal pages -> {OUT}")


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
/* quick navigation */
.quicknav{margin:22px 0 6px;padding:18px 20px;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:var(--radius)}
.quicknav h2{margin:0 0 12px;font-size:1.25rem}
.quicknav-controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.quicknav select{appearance:none;-webkit-appearance:none;background-color:var(--card-2);color:var(--ink);border:1px solid var(--line);
  border-radius:9px;padding:10px 40px 10px 14px;font:inherit;font-size:.95rem;min-width:240px;cursor:pointer;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='none' stroke='%23d8b25a' stroke-width='1.6' d='M1 1.5l5 5 5-5'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 14px center}
.quicknav select:disabled,.quicknav .btn:disabled{opacity:.5;cursor:not-allowed}
.quicknav select:focus-visible,.quicknav .btn:focus-visible{outline:2px solid var(--gold);outline-offset:1px}
.quicknav option:disabled{color:#7d7896}
.quicknav .btn{border:0;cursor:pointer;font:inherit;font-weight:700;padding:10px 22px}
[hidden]{display:none!important}
.qn-modes{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin:0 0 12px;font-size:.95rem}
.qn-modes-label{color:var(--muted)}
.qn-modes label{display:inline-flex;align-items:center;gap:6px;cursor:pointer}
.qn-modes input{accent-color:var(--gold)}
.h-small{font-size:1.15rem;margin:22px 0 10px}
.chip{display:inline-block;padding:2px 9px;margin:2px 4px 2px 0;border:1px solid var(--line);border-radius:999px;font-size:.8rem;white-space:nowrap;background:var(--card-2)}
.btn.btn-sm{padding:6px 12px;font-size:.85rem;margin:0}
.ptable a.btn,.ptable a.btn:visited{color:#1d1405;text-decoration:none}
.fam-filters{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:8px 0 12px}
.fam-filters label{display:flex;flex-direction:column;gap:4px;font-size:.85rem;color:var(--muted)}
.fam-filters select{background:var(--card-2);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:8px 12px;font:inherit;min-width:170px}
.proto-diff{margin:16px 0 4px;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--purple);border-radius:var(--radius);padding:12px 16px}
.proto-diff summary{cursor:pointer;font-weight:700;color:var(--gold-ink)}
.proto-diff[open] summary{margin-bottom:8px}
.avoid-note{color:#f08a80;margin-top:2px}
.diff-card{border-top:1px solid var(--line);padding:12px 0}
.diff-card:first-of-type{border-top:0}
.diff-head{margin-bottom:6px}
.fam-all{border-color:var(--gold)}
.or-divider{text-align:center;margin:20px 0 6px;font-family:Cinzel,Georgia,serif;font-size:2.1rem;font-weight:700;line-height:1.15;letter-spacing:.01em}
@media (max-width:720px){.or-divider{font-size:1.6rem}}
.or-note{text-align:center;color:var(--muted);margin:0 auto 4px;max-width:640px}
.quicknav-bar{margin:4px 0 14px;padding:10px 12px;border-left-width:1px}
.quicknav-bar select{min-width:210px;padding:8px 36px 8px 12px;font-size:.9rem}
.quicknav-bar .btn{padding:8px 18px}
.back-home{display:inline-flex;align-items:center;background:var(--card-2);color:var(--ink);border:1px solid var(--line);
  border-radius:9px;padding:8px 14px;font-size:.9rem;font-weight:600;white-space:nowrap}
.back-home:hover{border-color:var(--gold);color:var(--gold-ink)}
.back-home:focus-visible{outline:2px solid var(--gold);outline-offset:1px}
@media (max-width:720px){
  .quicknav{padding:14px}
  .quicknav-bar{padding:10px}
  .quicknav-bar .quicknav-controls{grid-template-columns:1fr 1fr}
  .quicknav-bar #qn-protocol,.quicknav-bar #qn-review{grid-column:1/-1}
  .quicknav-bar .back-home{order:3;justify-content:center} .quicknav-bar #qn-go{order:4}
  .quicknav-controls{display:grid;grid-template-columns:1fr;gap:8px}
  .quicknav select{min-width:0;width:100%}
}
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
.sys-table{min-width:980px}
.sys-table td{white-space:normal;font-size:.86rem}
.sys-name{color:var(--gold-ink);font-weight:700;text-decoration:underline;text-decoration-color:rgba(216,178,90,.4);text-underline-offset:3px}
.sys-table .buy{min-width:170px}
.sys-table .buy a:not(.btn){color:var(--gold-ink)}
.btn.small{padding:6px 12px;font-size:.82rem;white-space:nowrap}
.btn.ghost-btn{background:var(--card-2);color:var(--ink);border:1px solid var(--line)}
.btn.ghost-btn:hover{border-color:var(--gold);filter:none}
.sys-table td:first-child{white-space:normal;width:16%;min-width:170px}
.sys-table td:nth-child(2),.sys-table td:nth-child(3){width:26%}
.sys-table td.facts{width:19%;min-width:170px}
.sys-table td.sys-cell{font-weight:400}
.sys-head{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.best-for{margin-top:8px;font-size:.8rem;color:var(--muted)}
.best-for span,.fact span{display:block;font-size:.68rem;text-transform:uppercase;letter-spacing:.04em;color:var(--purple-ink)}
.fact{margin:0 0 6px;font-size:.8rem}
.fact:last-child{margin:0}
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
.pick-family{font-size:1.2rem;margin:30px 0 10px;color:var(--gold-ink)}
.works{margin-top:6px;font-size:.85rem;color:var(--muted);display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.pick-more{color:var(--purple-ink)}
.seasonal-strip{margin-top:26px}
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
