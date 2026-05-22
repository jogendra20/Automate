import os
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import re
import random
import string

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
    )
    page = browser.new_page(viewport={'width':1280,'height':800})
    stealth_sync(page)

    try:
        page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=30000)
        time.sleep(4)
        rows = page.query_selector_all("dl > dd")
        titles = []
        for row in rows[:10]:
            title = row.query_selector("div.meta > div.list-title").inner_text()
            if "Title: " in title:
                title = title.replace('Title: ', '').strip()
            titles.append(title)
        print("Titles:")
        for title in titles:
            print(title)

        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    except Exception as e:
        print(f'ERROR: {e}')
    finally:
        browser.close()