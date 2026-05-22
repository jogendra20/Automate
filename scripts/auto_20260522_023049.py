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
        page.goto('https://www.tickertape.in/market-movers', wait_until='domcontentloaded', timeout=45000)
        time.sleep(10)

        gainers_section = page.query_selector('//h2[text()="Top Gainers"]/ancestor::section')
        rows = gainers_section.query_selector_all("a[href*='/stocks/']")
        
        seen = set()
        count = 0
        for row in rows:
            text = row.inner_text().strip()
            sub_text = row.query_selector("span:nth-child(2)").inner_text().strip()  # Extracting percent change
            if text and text not in seen and len(text) > 2:
                seen.add(text)
                print(f"{text}: {sub_text}")
                count += 1
                if count >= 10:
                    break
    except Exception as e:
        page.screenshot(path='screenshot.png', full_page=False)
        print('screenshot saved')
        print(f'ERROR: {e}')
    finally:
        browser.close()