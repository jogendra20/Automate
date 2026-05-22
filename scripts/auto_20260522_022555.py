from playwright.sync_api import sync_playwright
import time
import pandas as pd
import os

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    try:
        page.goto('https://www.tickertape.in/', wait_until='domcontentloaded', timeout=45000)
        time.sleep(10)
        try:
            page.get_by_text('Gainers', exact=True).first.click()
            time.sleep(4)
        except:
            pass
        
        rows = page.query_selector_all("a[href*='/stocks/']")
        data = []
        seen = set()
        for row in rows:
            text = row.inner_text().strip()
            if text and text not in seen:
                seen.add(text)
                parts = text.split('\n')
                if len(parts) >= 3:
                    name = parts[0].strip()
                    symbol = parts[1].strip()
                    percent_change = parts[2].strip()
                    data.append({"Name": name, "Symbol": symbol, "Percent Change": percent_change})
                if len(data) >= 10:
                    break
        
        df = pd.DataFrame(data)
        print(df)
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path='screenshot.png', full_page=False)
        print('screenshot saved')
    finally:
        browser.close()