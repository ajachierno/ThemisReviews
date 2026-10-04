"""ThemisReviews static site generator.

Reads data/site.json and writes the static site into docs/ for GitHub Pages.
Zero dependencies. Run:  python build.py
"""
import html
import json
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
         structured_data=""):
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
  <p class="muted">{home_link}Last updated on {esc(site['updated'])}. Not affiliated with Amazon,
  the Z-Wave Alliance, the Connectivity Standards Alliance, the Thread Group, Lutron, or any manufacturer.</p>
</footer>
<a href="#" class="to-top" aria-label="Back to top">&uarr;</a>
<script>(function(){{var b=document.querySelector('.to-top');
window.addEventListener('scroll',function(){{b.classList.toggle('show',window.scrollY>600);}},{{passive:true}});}})();</script>
</body>
</html>"""


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
  <nav class="jump" aria-label="Jump to a protocol">
    <a href="#compare" class="jump-all">At a glance</a>{links}
  </nav>"""


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
    <h1>Pick the right smart home protocol first</h1>
    <p class="sub">{esc(site['description'])}</p>
  </section>
  {render_jump(protos)}
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


def main():
    site = load("site.json")
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "styles.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    if site.get("custom_domain"):
        (OUT / "CNAME").write_text(site["custom_domain"] + "\n", encoding="utf-8")
    build_home(site)
    print(f"Built home page with {len(site['protocols'])} protocols -> {OUT}")


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
a.sub-link:hover{border-color:var(--gold);color:var(--gold-ink)}
.sub-link.soon{color:var(--muted)}
.soon-tag{flex:none;font-size:.68rem;text-transform:uppercase;letter-spacing:.04em;
  border:1px solid var(--line);border-radius:20px;padding:1px 8px}
/* footer */
footer{max-width:var(--max);margin:0 auto;padding:24px 20px 50px;border-top:1px solid var(--line)}
.disclosure{font-size:.85rem;color:var(--muted);max-width:80ch}
footer .muted{font-size:.85rem}
footer a{color:var(--gold-ink)}
.to-top{display:none}
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
