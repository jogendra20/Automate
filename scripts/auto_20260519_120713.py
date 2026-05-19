import os
import time
from playwright.sync_api import sync_playwright

# Set API timeout
TIMEOUT = int(os.getenv("TIMEOUT", 60000))

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://www.tickertape.in/", wait_until="networkidle", timeout=TIMEOUT)

    # Click on Gainers tab
    page.wait_for_selector("[data-testid='gainers-tab']").click()

    # Wait for page to load and wait for selector
    page.wait_for_load_state("networkidle")
    page.wait_for_selector("[data-testid='gainers']", timeout=15000)
    
    # Find all gainers
    rows = page.query_selector_all("[data-testid='gainer-row']")
    
    for row in rows[:5]:
        symbol = row.query_selector("[data-testid='gainer-symbol']").inner_text()
        change_percent = row.query_selector("[data-testid='gainer-percentage']").inner_text()
        print(symbol, change_percent)

    page.screenshot(path="screenshot.png")
    browser.close()