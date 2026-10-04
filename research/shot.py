import asyncio, pathlib, sys
from playwright.async_api import async_playwright
async def main(slug):
    url = pathlib.Path(f"docs/{slug}.html").resolve().as_uri()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 2400})
        await pg.goto(url); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=f"shot-{slug}.png")
        m = await b.new_page(viewport={"width": 390, "height": 844})
        await m.goto(url); await m.wait_for_timeout(1500)
        print("mobile overflow:", await m.evaluate("document.documentElement.scrollWidth"))
        await m.locator("#ranked").scroll_into_view_if_needed()
        await m.screenshot(path=f"shot-{slug}-m.png")
        await b.close()
asyncio.run(main(sys.argv[1]))
