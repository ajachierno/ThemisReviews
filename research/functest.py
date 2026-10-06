"""Click-through tests of the site's interactive bits at phone and desktop sizes."""
import asyncio, re
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8765/"
VIEWS = {"desktop": dict(viewport={"width": 1366, "height": 900}),
         "phone": dict(viewport={"width": 412, "height": 915}, is_mobile=True, has_touch=True, device_scale_factor=2.6)}
results = []


def ok(cond, msg):
    results.append(("PASS" if cond else "FAIL") + " " + msg)


async def visible_rows(page, sel="table.ptable tbody tr"):
    return await page.eval_on_selector_all(sel, "rs => rs.filter(r => r.offsetParent !== null).length")


async def run(view, opts, b):
    ctx = await b.new_context(**opts)
    await ctx.route(re.compile(r"fonts\.(googleapis|gstatic)\.com"), lambda r: r.abort())
    pg = await ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    v = f"[{view}]"

    # Home quick nav, protocol mode
    await pg.goto(BASE + "index.html")
    await pg.select_option("#qn-protocol", "z-wave")
    ok(await pg.is_enabled("#qn-review"), f"{v} home: picking a protocol enables the review select")
    opts_ = await pg.eval_on_selector_all("#qn-review option", "os => os.map(o => o.value).filter(Boolean)")
    ok(len(opts_) > 5, f"{v} home: Z-Wave review list has {len(opts_)} options")
    await pg.select_option("#qn-review", opts_[0])
    if await pg.is_enabled("#qn-go"):
        await pg.click("#qn-go")
    await pg.wait_for_load_state("load")
    ok(opts_[0].split("/")[-1].replace(".html", "") in pg.url, f"{v} home: Go lands on {pg.url.split('/')[-1]}")

    # Home quick nav, product type mode
    await pg.goto(BASE + "index.html")
    await pg.click("input[name=qn-mode][value=type]")
    ok(await pg.is_visible("#qn-type"), f"{v} home: product-type select visible after toggle")
    ok(not await pg.is_visible("#qn-protocol"), f"{v} home: protocol select hidden in product-type mode")
    tv = await pg.eval_on_selector_all("#qn-type option", "os => os.map(o => o.value).filter(Boolean)")
    ok(len(tv) >= 40, f"{v} home: {len(tv)} product types listed")
    await pg.select_option("#qn-type", tv[0])
    if await pg.is_enabled("#qn-type-go"):
        await pg.click("#qn-type-go")
    await pg.wait_for_load_state("load")
    ok(pg.url.endswith(".html") and "index" not in pg.url, f"{v} home: type Go lands on {pg.url.split('/')[-1]}")

    # Home: Black Friday link stays hidden before Nov 15, gift guides visible
    await pg.goto(BASE + "index.html")
    bf = await pg.eval_on_selector_all("a[href*=black-friday]", "as => as.filter(a => a.offsetParent !== null).length")
    ok(bf == 0, f"{v} home: Black Friday link hidden ({bf} visible)")
    ok(await pg.is_visible("#gift-guides"), f"{v} home: gift guides section visible")

    # Protocol page: works-with filter
    await pg.goto(BASE + "z-wave-switches.html")
    total = await visible_rows(pg)
    sysv = await pg.eval_on_selector_all("#t-sys option", "os => os.map(o => o.value).filter(Boolean)")
    await pg.select_option("#t-sys", sysv[-1])
    after = await visible_rows(pg)
    ok(0 < after <= total, f"{v} z-wave-switches: system filter {sysv[-1]} shows {after}/{total} rows")
    await pg.select_option("#t-sys", "")
    ok(await visible_rows(pg) == total, f"{v} z-wave-switches: clearing filter restores {total} rows")
    await pg.goto(BASE + "z-wave-switches.html?system=hubitat")
    ok(await pg.eval_on_selector("#t-sys", "s => s.value") == "hubitat", f"{v} z-wave-switches: ?system= preselects")

    # Product-type page: multi-select protocol + system + sort
    await pg.goto(BASE + "smart-light-switches.html")
    total = await visible_rows(pg)
    await pg.click("#f-proto-dd > summary")
    await pg.check("input[name=f-proto][value=z-wave]")
    z = await visible_rows(pg)
    await pg.check("input[name=f-proto][value=zigbee]")
    zz = await visible_rows(pg)
    ok(0 < z < zz < total, f"{v} smart-light-switches: protocol multi-select z-wave {z}, +zigbee {zz}, all {total}")
    label = await pg.inner_text("#f-proto-dd > summary")
    ok("2" in label, f"{v} smart-light-switches: dropdown label reads '{label.strip()}'")
    await pg.mouse.click(5, 5)
    ok(not await pg.eval_on_selector("#f-proto-dd", "d => d.open"), f"{v} smart-light-switches: dropdown closes on outside tap")
    await pg.click("#f-proto-dd > summary")
    await pg.click("#f-proto-clear")
    ok(await visible_rows(pg) == total, f"{v} smart-light-switches: Clear all restores rows")
    await pg.mouse.click(5, 5)
    sysv = await pg.eval_on_selector_all("#f-sys option", "os => os.map(o => o.value).filter(Boolean)")
    await pg.select_option("#f-sys", "apple-home" if "apple-home" in sysv else sysv[0])
    ok(0 < await visible_rows(pg) < total, f"{v} smart-light-switches: system filter narrows rows")
    await pg.select_option("#f-sys", "")
    sorts = await pg.eval_on_selector_all("#f-sort option", "os => os.map(o => o.value)")
    for s in sorts:
        await pg.select_option("#f-sort", s)
        vals = await pg.eval_on_selector_all("table.ptable tbody tr", "rs => rs.filter(r => r.offsetParent).map(r => r.dataset)")
        ok(len(vals) == total, f"{v} smart-light-switches: sort '{s}' keeps {len(vals)} rows")
    if "price" in " ".join(sorts):
        s = [x for x in sorts if "price" in x][0]
        await pg.select_option("#f-sort", s)
        prices = await pg.eval_on_selector_all("table.ptable tbody tr", "rs => rs.filter(r => r.offsetParent && r.dataset.price && !r.classList.contains('avoid-row')).map(r => +r.dataset.price)")
        ok(prices == sorted(prices) or prices == sorted(prices, reverse=True), f"{v} smart-light-switches: price sort ordered ({prices[:4]}...)")
    await pg.goto(BASE + "smart-light-switches.html?protocol=matter,thread")
    chk = await pg.eval_on_selector_all("input[name=f-proto]:checked", "is => is.map(i => i.value)")
    ok(sorted(chk) == ["matter", "thread"], f"{v} smart-light-switches: ?protocol= preselects {chk}")
    # protocol differences explainer collapsed by default, opens on click
    ok(not await pg.eval_on_selector("details.proto-diff", "d => d.open"), f"{v} smart-light-switches: protocol differences collapsed")
    await pg.click("details.proto-diff > summary")
    ok(await pg.eval_on_selector("details.proto-diff", "d => d.open"), f"{v} smart-light-switches: protocol differences opens")

    # Category page anchors / jump nav / buyer's guide accordions
    await pg.goto(BASE + "wifi-pet-cameras.html")
    for a in ["#picks", "#compare", "#ranked", "#avoid", "#guide"]:
        ok(await pg.locator(a).count() == 1, f"{v} wifi-pet-cameras: jump target {a} exists")
    await pg.click("#guide details >> nth=0")
    ok(await pg.eval_on_selector("#guide details", "d => d.open"), f"{v} wifi-pet-cameras: buyer's guide opens")
    links = await pg.eval_on_selector_all("a[href*='amazon.com']", "as => as.map(a => [a.href, a.rel, a.target])")
    bad = [l for l in links if "tag=themisreviews-20" not in l[0] or "sponsored" not in l[1]]
    ok(not bad, f"{v} wifi-pet-cameras: {len(links)} Amazon links tagged + rel=sponsored ({len(bad)} bad)")

    # Gift + Black Friday pages render picks
    for gp in ["smart-home-gifts-under-50.html", "smart-home-gifts-under-100.html", "black-friday-smart-home-deals.html"]:
        await pg.goto(BASE + gp)
        n = await pg.eval_on_selector_all("a[href*='amazon.com']", "as => as.length")
        ok(n >= 10, f"{v} {gp}: {n} Amazon links")
    # Header search
    await pg.goto(BASE + "wifi-bulbs.html")
    await pg.fill("#ss-q", "zen77"); await pg.wait_for_timeout(400)
    names = await pg.eval_on_selector_all("#ss-list .ss-item .ss-n", "ns => ns.map(n => n.textContent)")
    ok(any("ZEN77" in n for n in names), f"{v} search: 'zen77' finds the Zooz ZEN77 ({names[:2]})")
    await pg.fill("#ss-q", "zwave dimmer"); await pg.wait_for_timeout(400)
    first = await pg.eval_on_selector("#ss-list .ss-item", "a => a.getAttribute('href')")
    ok(first == "z-wave-dimmers.html", f"{v} search: 'zwave dimmer' puts the Z-Wave dimmers page first ({first})")
    await pg.press("#ss-q", "Enter"); await pg.wait_for_load_state("load"); await pg.wait_for_timeout(500)
    n = await pg.eval_on_selector_all("#sr-list .ss-item", "as => as.length")
    ok("search.html?q=" in pg.url and n > 5, f"{v} search: Enter opens the results page with {n} results")
    await pg.fill("#ss-q", "xqzzy"); await pg.wait_for_timeout(400)
    ok(await pg.locator("#ss-list .ss-none").count() == 1, f"{v} search: nonsense query says no matches")
    await pg.press("#ss-q", "Escape")
    ok(await pg.eval_on_selector("#ss-list", "p => p.hidden"), f"{v} search: Escape closes the dropdown")
    # "Must work without" filter + home picker
    await pg.goto(BASE + "wifi-doorbells.html")
    tot = await visible_rows(pg, "#compare tbody tr")
    await pg.check("input[name=t-wo][value=sub]")
    aft = await visible_rows(pg, "#compare tbody tr")
    ok(0 < aft < tot, f"{v} wifi-doorbells: no-subscription filter {tot} -> {aft} rows")
    await pg.goto(BASE + "smart-light-switches.html?without=neutral")
    ok(await pg.is_checked("input[name=f-wo][value=neutral]"), f"{v} smart-light-switches: ?without= preselects")
    await pg.goto(BASE + "index.html")
    ok(await pg.is_disabled("#pk-go"), f"{v} picker: button waits for a device type")
    await pg.select_option("#pk-sys", "apple-home"); await pg.select_option("#pk-fam", "smart-light-switches")
    await pg.check("input[name=pk-wo][value=neutral]"); await pg.click("#pk-go"); await pg.wait_for_timeout(800)
    cards = await pg.eval_on_selector_all("#pk-out .pk-card", "cs => cs.length")
    href = await pg.eval_on_selector("#pk-out a.btn", "a => a.getAttribute('href')")
    ok(cards == 3 and href == "smart-light-switches.html?system=apple-home&without=neutral", f"{v} picker: {cards} picks, link {href}")
    await pg.select_option("#pk-fam", "smart-plugs")
    ok(await pg.is_disabled("input[name=pk-wo][value=neutral]"), f"{v} picker: neutral option disabled for plug-in devices")
    ok(not errs, f"{v} no page errors during click-through {errs[:2]}")
    await ctx.close()


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, channel="chrome")
        for view, opts in VIEWS.items():
            try:
                await run(view, opts, b)
            except Exception as e:
                results.append(f"FAIL [{view}] crashed: {str(e)[:300]}")
        await b.close()
    print("\n".join(results))
    print(sum(r.startswith("FAIL") for r in results), "failures")

asyncio.run(main())
