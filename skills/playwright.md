# Playwright Automation Skills

## Browser Launch (Always use these exact flags)

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})

## Screenshot (Always save as screenshot.png)

page.goto("https://example.com", wait_until="networkidle", timeout=60000)
time.sleep(10)
page.screenshot(path="screenshot.png", full_page=False)
browser.close()

## Wait Strategies

page.wait_for_load_state("networkidle")
page.wait_for_selector("#main-content", timeout=30000)
time.sleep(5)

## Form Fill

page.fill('input[name="username"]', "value")
page.fill('input[name="password"]', "value")
page.click('button[type="submit"]')
page.wait_for_load_state("networkidle")
print(page.title())

## Scrape Table Data

rows = page.query_selector_all("table tbody tr")
for row in rows:
    cols = row.query_selector_all("td")
    data = [c.inner_text().strip() for c in cols]
    print(data)

## NSE India API (Never use Playwright on nseindia.com)

import requests
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "*/*",
    "Referer": "https://www.nseindia.com",
}
session.get("https://www.nseindia.com", headers=headers, timeout=10)
res = session.get(
    "https://www.nseindia.com/api/live-analysis-variations?index=gainers",
    headers=headers, timeout=10
)
data = res.json()
for item in data.get("data", []):
    # Correct field names from NSE API:
    # symbol, lastPrice, change, pChange, previousPrice, totalTradedVolume
    print(item.get("symbol"), item.get("lastPrice"), item.get("pChange"))

# If using pandas, convert pChange to float first:
# df["pChange"] = pd.to_numeric(df["pChange"], errors="coerce")

## Async Playwright

import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()
        await page.goto("https://example.com", wait_until="networkidle")
        await page.screenshot(path="screenshot.png")
        await browser.close()

asyncio.run(run())
