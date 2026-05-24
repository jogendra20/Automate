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
        page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=30000)
        time.sleep(8)
        titles = page.query_selector_all('dt')
        descriptions = page.query_selector_all('dd')
        for i in range(min(2, len(titles))):
            title = descriptions[i].query_selector('div.list-title').inner_text().replace('Title:', '').strip()
            print(f"{i+1}. {title}")
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    except Exception as e:
        print(f"ERROR: {e}")
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    finally:
        browser.close()