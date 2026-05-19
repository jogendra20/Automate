import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ])
        page = await browser.new_page()
        await page.goto("https://www.gprec.ac.in", wait_until="domcontentloaded")
        await asyncio.sleep(30)
        screenshot = await page.screenshot()
        print(screenshot)
        await browser.close()

asyncio.run(main())