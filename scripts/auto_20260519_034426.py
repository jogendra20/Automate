import asyncio
from playwright.async_api import async_playwright

async def scrape_books_toscrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()

        await page.goto("https://books.toscrape.com/", wait_until="domcontentloaded")

        titles = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('h3 a')).map(a => a.title);
        }''')

        await browser.close()

        for title in titles:
            print(title)

asyncio.run(scrape_books_toscrape())