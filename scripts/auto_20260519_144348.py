from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://www.tickertape.in/", wait_until="networkidle", timeout=60000)
    time.sleep(5)
    
    try:
        page.get_by_text("Gainers", exact=True).first.click()
        time.sleep(5)
    except:
        pass

    rows = page.query_selector_all("a[href*='/stocks/']")
    seen = set()
    count = 0
    for row in rows:
        text = row.inner_text().strip()
        if text and text not in seen and "%" in text:
            seen.add(text)
            print(text)
            count += 1
            if count >= 5:
                break
    
    page.screenshot(path="screenshot.png", full_page=False)
    browser.close()