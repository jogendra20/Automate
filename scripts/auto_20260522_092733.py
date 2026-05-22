from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    stealth_sync(page)
    try:
        page.goto('https://news.ycombinator.com/', wait_until='domcontentloaded', timeout=30000)
        time.sleep(8)
        titles = page.query_selector_all('tr.athing .titleline > a')
        scores = page.query_selector_all('span.score')
        
        for i, (title, score) in enumerate(zip(titles, scores)):
            if i >= 10:
                break
            post_title = title.inner_text().strip()
            points = score.inner_text().strip()
            print(f"{i+1}. {post_title} - {points}")
        
        page.screenshot(path='screenshot.png', full_page=False)
        print('screenshot saved')
    except Exception as e:
        page.screenshot(path='screenshot.png', full_page=False)
        print('screenshot saved')
        print(f'ERROR: {e}')
    finally:
        browser.close()