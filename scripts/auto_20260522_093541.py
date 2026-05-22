from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time, os

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    stealth_sync(page)
    try:
        page.goto('https://news.ycombinator.com', wait_until='domcontentloaded', timeout=30000)
        time.sleep(8)
        
        rows = page.query_selector_all('tr.athing')
        result = []
        for row in rows:
            title = row.query_selector('a.titlelink')
            score = row.evaluate('sibling => sibling && sibling.nextElementSibling && sibling.nextElementSibling.querySelector(".score") ? sibling.nextElementSibling.querySelector(".score").innerText.trim() : "No points"', row)
            if title and len(result) < 10:
                result.append(f"{len(result)+1}. {title.inner_text().strip()} ({score})")
        
        for item in result:
            print(item)
        
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
    
    except Exception as e:
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
        print(f'ERROR: {e}')
    finally:
        browser.close()