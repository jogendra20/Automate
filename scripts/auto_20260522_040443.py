from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time, os

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    stealth_sync(page=browser.new_page(viewport={'width': 1280, 'height': 800}))
    
    try:
        page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=45000)
        time.sleep(10)
        papers = page.query_selector_all("div#content dl dt + dd")
        count = 0
        for paper in papers[:10]:
            title = paper.query_selector("div.meta div.list-title.mathjax").text_content().strip().replace("Title: ", "")
            authors = paper.query_selector("div.meta div.list-authors").text_content().strip().replace("Authors:", "").strip()
            count += 1
            print(f"{count}. Title: {title}")
            print(f"   Authors: {authors}")
        page.screenshot(path="screenshot.png", full_page=False)
        print('screenshot saved')
    except Exception as e:
        page.screenshot(path="screenshot.png")
        print(f'ERROR: {e}')
        print('screenshot saved')
    finally:
        browser.close()