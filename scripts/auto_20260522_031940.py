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
        page.goto('https://www.moneycontrol.com/news/business', wait_until='domcontentloaded', timeout=45000)
        time.sleep(15)
        content = page.content()
        print(content[:2000])
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path='screenshot.png', full_page=False)
        print('screenshot saved')
    finally:
        browser.close()