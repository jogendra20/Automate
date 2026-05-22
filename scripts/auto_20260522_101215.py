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
        page.goto('https://news.ycombinator.com', wait_until='domcontentloaded', timeout=30000)
        time.sleep(6)
        titles = page.query_selector_all('tr.athing')
        scores = page.query_selector_all('span.score')
        
        for i, (title_row, score_span) in enumerate(zip(titles[:10], scores[:10])):
            title_el = title_row.query_selector('span.titleline a')
            title = title_el.inner_text().strip() if title_el else 'N/A'
            points = score_span.inner_text().strip() if score_span else '0 points'
            print(f"{i+1}. {title}")
            print(f"   {points}")
            print()
    except Exception as e:
        page.screenshot(path='screenshot.png')
        print("screenshot saved")
        print(f"ERROR: {e}")
    finally:
        browser.close()