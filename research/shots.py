import asyncio, re
from playwright.async_api import async_playwright
PAGES = ["index.html", "wifi-pet-cameras.html", "smart-blinds-and-shades.html", "smart-home-gifts-under-50.html", "black-friday-smart-home-deals.html", "wifi-mesh-routers.html"]
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, channel="chrome")
        for view, opts, h in [("phone", dict(viewport={"width": 412, "height": 915}, is_mobile=True, has_touch=True, device_scale_factor=1), 915),
                              ("desk", dict(viewport={"width": 1366, "height": 900}), 900)]:
            ctx = await b.new_context(**opts)
            await ctx.route(re.compile(r"fonts\.(googleapis|gstatic)\.com"), lambda r: r.abort())
            pg = await ctx.new_page()
            for u in PAGES:
                await pg.goto("http://127.0.0.1:8765/" + u, wait_until="load")
                await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await pg.wait_for_timeout(500)
                H = await pg.evaluate("document.body.scrollHeight")
                n = min(4, -(-H // h))
                for i in range(n):
                    await pg.evaluate(f"window.scrollTo(0,{i*h})"); await pg.wait_for_timeout(150)
                    await pg.screenshot(path=f"shots/{view}-{u[:-5]}-{i}.png")
                print(view, u, H, n)
            await ctx.close()
        await b.close()
asyncio.run(m())
