"""Site audit: loads every page in docs/ at desktop and phone sizes from a local server and
reports JS errors, failed requests, horizontal overflow, broken images, and broken links."""
import asyncio, json, os, re, sys
from pathlib import Path
from playwright.async_api import async_playwright

DOCS = Path(__file__).resolve().parent.parent / "docs"
BASE = "http://127.0.0.1:8765/"
VIEWS = {"desktop": dict(viewport={"width": 1366, "height": 900}),
         "phone": dict(viewport={"width": 412, "height": 915}, is_mobile=True, has_touch=True, device_scale_factor=2.6)}

CHECK_JS = r"""() => {
  const out = {};
  const W = document.documentElement.clientWidth;
  out.scrollW = document.documentElement.scrollWidth; out.W = W;
  // elements sticking out past the right edge (ignore things inside horizontal scrollers)
  const wide = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.right <= W + 1) continue;
    let p = el.parentElement, scroller = false;
    while (p && p !== document.body) { const s = getComputedStyle(p); if (/(auto|scroll|hidden)/.test(s.overflowX)) { scroller = true; break; } p = p.parentElement; }
    if (!scroller) wide.push(el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').join('.') : '') + ' r=' + Math.round(r.right));
  }
  out.wide = wide.slice(0, 6);
  out.badImgs = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map(i => i.getAttribute('src')).slice(0, 5);
  out.noAlt = [...document.images].filter(i => !i.hasAttribute('alt')).length;
  out.links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
  out.ids = [...document.querySelectorAll('[id]')].map(e => e.id);
  out.title = document.title; out.h1 = document.querySelectorAll('h1').length;
  out.desc = (document.querySelector('meta[name=description]') || {}).content || '';
  out.canon = (document.querySelector('link[rel=canonical]') || {}).href || '';
  // visible text overlapping: tiny font check
  out.tiny = [...document.querySelectorAll('p,li,td,a,span')].filter(e => e.offsetParent && parseFloat(getComputedStyle(e).fontSize) < 11 && e.textContent.trim()).length;
  return out;
}"""


async def check(ctx, name, view, results):
    page = await ctx.new_page()
    errs, fails = [], []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: m.type == "error" and errs.append(m.text[:200]))
    page.on("requestfailed", lambda r: fails.append(r.url[:150] + " " + (r.failure or "")))
    page.on("response", lambda r: r.status >= 400 and fails.append(f"{r.status} {r.url[:150]}"))
    try:
        await page.goto(BASE + name, wait_until="load", timeout=60000)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(600)
        info = await page.evaluate(CHECK_JS)
    except Exception as e:
        info = {"fatal": str(e)[:200]}
    info["errs"], info["fails"] = errs, [f for f in fails if "googleapis" not in f and "gstatic" not in f]
    results[(name, view)] = info
    await page.close()


async def main():
    pages = sorted(p.name for p in DOCS.glob("*.html"))
    results = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, channel="chrome")
        for view, opts in VIEWS.items():
            ctx = await b.new_context(**opts)
            await ctx.route(re.compile(r"fonts\.(googleapis|gstatic)\.com"), lambda r: r.abort())
            sem = asyncio.Semaphore(6)
            async def run(n):
                async with sem:
                    await check(ctx, n, view, results)
            await asyncio.gather(*(run(n) for n in pages))
            await ctx.close()
        await b.close()
    # link check (static, from desktop pass)
    files = set(pages)
    ids = {n: set(results[(n, "desktop")].get("ids", [])) for n in pages}
    problems = []
    for (n, view), r in sorted(results.items()):
        tag = f"{n} [{view}]"
        if r.get("fatal"): problems.append(f"{tag} FATAL {r['fatal']}")
        for e in r.get("errs", []):
            if "ERR_FAILED" in e: continue
            problems.append(f"{tag} JS {e}")
        for f in r.get("fails", []): problems.append(f"{tag} REQ {f}")
        if r.get("scrollW", 0) > r.get("W", 0) + 1: problems.append(f"{tag} OVERFLOW {r['scrollW']}>{r['W']} {r.get('wide')}")
        for i in r.get("badImgs", []): problems.append(f"{tag} IMG {i}")
        if r.get("noAlt"): problems.append(f"{tag} {r['noAlt']} img without alt")
        if view == "desktop":
            if r.get("h1") != 1: problems.append(f"{tag} h1 count {r.get('h1')}")
            if not r.get("desc"): problems.append(f"{tag} no meta description")
            for h in set(r.get("links", [])):
                if h.startswith(("http", "mailto:", "javascript:")): continue
                path, _, frag = h.partition("#")
                raw = path.split("?")[0]
                path = raw[2:] if raw.startswith("./") else raw.lstrip("/")
                if raw in ("./", "/", "."): path = "index.html"
                elif path == "": path = n
                if path.endswith("/"): path += "index.html"
                if path not in files and not (DOCS / path).exists(): problems.append(f"{tag} LINK {h}"); continue
                if frag and path in ids and frag not in ids[path]: problems.append(f"{tag} ANCHOR {h}")
    print(f"{len(pages)} pages x {len(VIEWS)} views")
    print("\n".join(problems) or "no problems")
    json.dump({f"{k[0]}|{k[1]}": v for k, v in results.items()}, open(Path(__file__).parent / "audit-out.json", "w"), indent=1)

asyncio.run(main())
