from playwright.sync_api import sync_playwright
import time, os

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
    )
    page = browser.new_page(viewport={'width':1280,'height':800})
    try:
        page.goto('https://news.ycombinator.com', wait_until='domcontentloaded', timeout=30000)
        time.sleep(8)
        rows = page.query_selector_all("tr.athing")
        titles = []
        
        for row in rows:
            rank = row.query_selector(".rank").inner_text().strip() if row.query_selector(".rank") else ''
            title = row.query_selector(".titleline").inner_text().strip() if row.query_selector(".titleline") else ''
            score_span = row.next_sibling.query_selector(".score") if row.next_sibling else None
            score = score_span.inner_text().strip() if score_span else '0 points'
            if rank and title:
                titles.append(f"{rank} {title} - {score}")
            if len(titles) >= 10:
                break

        for title in titles:
            print(title)

        page.screenshot(path='screenshot.png')
        print('screenshot saved')
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path='screenshot.png')
        print('screenshot saved')
    finally:
        browser.close()