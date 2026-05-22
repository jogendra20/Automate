import os
import pandas as pd

run_id = os.environ.get('RUN_ID', '')

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
    )
    page = browser.new_page(viewport={'width':1280,'height':800})
    stealth_sync(page)
    try:
        page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=45000)
        rows = page.query_selector_all("dl > dd")
        titles = []
        for row in rows:
            title = row.inner_text()
            if 'Title: ' in title:
                title = title.replace('Title: ', '').strip()
            titles.append(title)
            if len(titles) >= 10:
                break

        print("Titles:")
        for title in titles:
            print(title)

        df = pd.DataFrame({'Titles': titles})
        print(df.head())
        df.to_csv('titles.csv', index=False)
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    finally:
        browser.close()