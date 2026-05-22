from playwright.sync_api import sync_playwright
import time, os

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    try:
        page.goto('https://www.tickertape.in/market-trends', wait_until='domcontentloaded', timeout=45000)
        time.sleep(10)
        try:
            page.get_by_text('Gainers', exact=True).first.click()
            time.sleep(4)
        except:
            pass
        rows = page.query_selector_all("a[href*='/stocks/']")
        seen = set()
        count = 0
        for row in rows:
            parent = row.query_selector('..')
            if parent:
                text = row.inner_text().strip()
                percent_change = parent.query_selector('.change-info')  # Adjusted selector for percent change
                if percent_change:
                    percent_change_text = percent_change.inner_text().strip()
                    if text and text not in seen and len(text) > 2:
                        seen.add(text)
                        print(f"{text}: {percent_change_text}")
                        count += 1
                        if count >= 10:
                            break
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    finally:
        browser.close()