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
        try:
            page.get_by_text('Gainers', exact=True).first.click()
            time.sleep(4)
        except:
            pass
        rows = page.query_selector_all("a[href*='/stocks/']")
        gainers = []
        for row in rows:
            text = row.inner_text().strip()
            if text and len(text) > 2:
                spans = row.query_selector_all("span")
                if len(spans) >= 2:
                    stock_name = spans[0].inner_text().strip()
                    percent_change = spans[1].inner_text().strip()
                    gainers.append((stock_name, percent_change))
                if len(gainers) >= 5:
                    break
        for gainer in gainers:
            print(gainer[0], gainer[1])
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path='screenshot.png', full_page=False)
        print('screenshot saved')
    finally:
        browser.close()