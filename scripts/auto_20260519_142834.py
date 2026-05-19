from playwright.sync_api import sync_playwright
import time
import os

os.environ['PLAYWRIGHT_EXECUTABLE_PATH'] = '/usr/bin/playwright'

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    page.goto("https://www.tickertape.in/", wait_until="networkidle", timeout=60000)
    time.sleep(10)

    page.get_by_text("Gainers", exact=True).first.click()
    page.wait_for_load_state("networkidle")

    rows = page.query_selector_all("a[href*='/stocks/']")
    seen = set()
    count = 0
    for row in rows:
        try:
            text = row.inner_text().strip()
            if text and text not in seen:
                seen.add(text)
                parts = text.split('(')
                symbol = parts[0]
                percent = parts[1].split('%')[0]
                print(f"{symbol} : {percent}")
                count += 1
                if count >= 5:
                    break
        except Exception as e:
            pass
    browser.close()