import os
from playwright.sync_api import sync_playwright

API_KEY = os.getenv("PLAYWRIGHT_API_KEY")
if not API_KEY:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        page.goto("https://www.tickertape.in/")
        page.wait_for_timeout(5000)
        table = page.query_selector("div.top-gainers-table")
        rows = table.query_selector_all("tr")
        gainers = []
        for row in rows[1:]:
            cols = row.query_selector_all("td")
            gainers.append((cols[0].inner_text(), cols[1].inner_text()))
        print(gainers[:5])
        browser.close()
else:
    print("PLAYWRIGHT_API_KEY is required")