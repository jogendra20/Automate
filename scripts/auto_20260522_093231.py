from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time, os

run_id = os.getenv('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    stealth_sync(page)
    try:
        page.goto('https://news.ycombinator.com', wait_until='domcontentloaded', timeout=30000)
        time.sleep(6)
        rows = page.query_selector_all('tr.athing')
        results = []
        for row in rows:
            title = row.query_selector('.titleline a')
            score_element = row.evaluate_handle('node => node.nextElementSibling.querySelector(".subtext .score")')
            score = score_element.evaluate('node => node.innerText', force_expr=True) if score_element else '0 points'
            if title:
                results.append((title.inner_text(), score))
            if len(results) >= 10:
                break
        for idx, (title, score) in enumerate(results, 1):
            print(f"{idx}. {title} ({score})")
    except Exception as e:
        print(f"ERROR: {e}")
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    finally:
        browser.close()