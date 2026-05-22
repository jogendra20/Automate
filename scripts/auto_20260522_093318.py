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
        page.goto('https://news.ycombinator.com', wait_until='domcontentloaded', timeout=45000)
        time.sleep(10)
        rows = page.query_selector_all('tr.athing')
        results = []
        for row in rows:
            title = row.query_selector('.titleline a')
            if title:
                score_tr = title.get_parent().query_selector('td .subtext')
                if score_tr:
                    score = score_tr.inner_text().split(' ')[1]
                    results.append((title.inner_text(), score))
                if len(results) >= 10:
                    break
        for idx, (title, score) in enumerate(results, 1):
            print(f"{idx}. {title} ({score})")
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    except Exception as e:
        print(f"ERROR: {e}")
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    finally:
        browser.close()