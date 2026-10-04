"""Live Amazon research helper (real Chrome, warmed on the homepage).

  python amz.py search out.json "query one" ["query two" ...]     (2 pages each)
  python amz.py products out.json ASIN [ASIN ...]
"""
import asyncio, json, sys
from playwright.async_api import async_playwright

SEARCH_JS = r"""() => [...document.querySelectorAll('div[data-component-type="s-search-result"]')].map(d => {
  const t = d.querySelector('h2');
  const sp = !!d.querySelector('.puis-sponsored-label-text, .s-sponsored-label-text') || /Sponsored/.test(d.innerText.slice(0,200));
  const price = d.querySelector('.a-price:not(.a-text-price) .a-offscreen');
  const rat = d.querySelector('i[class*="a-star"] span.a-icon-alt, span.a-icon-alt');
  const rev = d.querySelector('a[href*="customerReviews"]');
  const img = d.querySelector('img.s-image');
  const bought = [...d.querySelectorAll('span')].map(s=>s.textContent).find(x=>/bought in past month/.test(x));
  return {asin: d.dataset.asin, sponsored: sp, title: t ? t.textContent.trim() : '',
    price: price ? price.textContent : null, rating: rat ? rat.textContent : null,
    reviews: rev ? (rev.getAttribute('aria-label') || rev.textContent.trim()) : null,
    image: img ? img.src : null, bought: bought || null};
})"""

PRODUCT_JS = r"""() => {
  const q = s => document.querySelector(s); const tx = s => { const e = q(s); return e ? e.textContent.trim() : null; };
  const img = q('#landingImage');
  const rows = {};
  document.querySelectorAll('#productOverview_feature_div tr, #productDetails_techSpec_section_1 tr, #productDetails_detailBullets_sections1 tr, #technicalSpecifications_section_1 tr').forEach(r => {
    const k = r.querySelector('th, td'); const v = r.querySelector('td:last-child');
    if (k && v && k !== v) rows[k.textContent.trim()] = v.textContent.trim().replace(/\s+/g,' ');
  });
  document.querySelectorAll('#detailBullets_feature_div li').forEach(li => {
    const s = li.querySelectorAll('span span'); if (s.length >= 2) rows[s[0].textContent.replace(/[:‏‎]/g,'').trim()] = s[1].textContent.trim();
  });
  return {
    title: tx('#productTitle'), byline: tx('#bylineInfo'),
    price: tx('#corePrice_feature_div .a-price .a-offscreen') || tx('#corePriceDisplay_desktop_feature_div .a-price .a-offscreen') || tx('.a-price .a-offscreen'),
    rating: q('#acrPopover') ? q('#acrPopover').getAttribute('title') : null,
    reviews: tx('#acrCustomerReviewText'), bought: tx('#social-proofing-faceout-title-tk_bought'),
    availability: tx('#availability'), seller: tx('#merchantInfoFeature_feature_div .offer-display-feature-text-message') || tx('#sellerProfileTriggerId'),
    image: img ? (img.getAttribute('data-old-hires') || img.src) : null,
    bullets: [...document.querySelectorAll('#feature-bullets li span.a-list-item')].map(s => s.textContent.trim()).filter(Boolean),
    specs: rows,
  };
}"""

async def run(mode, out, items):
    import os
    res = {} if mode == "products" else []
    if mode == "products" and os.path.exists(out):
        res = json.load(open(out, encoding="utf-8"))
        items = [i for i in items if i not in res or not res[i].get("title")]
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=False, channel="chrome",
                                    args=["--disable-blink-features=AutomationControlled", "--disable-background-timer-throttling", "--disable-renderer-backgrounding", "--disable-backgrounding-occluded-windows"])
        ctx = await b.new_context(locale="en-US", viewport={"width": 1366, "height": 900})
        ctx.set_default_timeout(45000)
        warm = await ctx.new_page()
        await warm.goto("https://www.amazon.com/", wait_until="domcontentloaded"); await warm.wait_for_timeout(2500)
        if mode == "search":
            for it in items:
                for n in (1, 2):
                    await warm.goto(f"https://www.amazon.com/s?k={it.replace(' ', '+')}&page={n}", wait_until="domcontentloaded")
                    await warm.wait_for_timeout(2500)
                    rows = await warm.evaluate(SEARCH_JS)
                    for i, r in enumerate(rows): r.update(query=it, page=n, pos=i)
                    res += rows
        else:
            import random
            pg = await ctx.new_page()
            await pg.route("**/*.{png,jpg,jpeg,gif,webp,woff,woff2,mp4}", lambda r: r.abort())
            fails = 0
            for it in items:
                for attempt in (1, 2):
                    try:
                        await pg.goto(f"https://www.amazon.com/dp/{it}", wait_until="commit")
                        await pg.wait_for_selector("#productTitle", timeout=20000)
                        await pg.wait_for_timeout(1200)
                        d = await pg.evaluate(PRODUCT_JS); break
                    except Exception as e:
                        d = {"title": None, "error": (await pg.title()) + " | " + str(e)[:120]}
                        print(f"{it}: attempt {attempt} failed ({d['error'][:60]}), backing off", file=sys.stderr, flush=True)
                        await pg.wait_for_timeout(45000)
                        await pg.goto("https://www.amazon.com/", wait_until="commit"); await pg.wait_for_timeout(4000)
                d["asin"] = it; res[it] = d
                fails = fails + 1 if not d.get("title") else 0
                json.dump(res, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
                print(f"{it}: {(d.get('title') or 'NO TITLE')[:70]} | {d.get('price')} | {d.get('rating')} | {d.get('reviews')}", file=sys.stderr, flush=True)
                if fails >= 4:
                    print("STOPPING: 4 failures in a row", file=sys.stderr, flush=True); break
                await pg.wait_for_timeout(random.randint(3000, 6000))
        await b.close()
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

asyncio.run(run(sys.argv[1], sys.argv[2], sys.argv[3:]))
