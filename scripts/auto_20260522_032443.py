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
        time.sleep(5)

        rows = page.query_selector_all('tr.athing')
        count = 0
        for row in rows:
            title_element = row.query_selector('.titleline > a')
            points_element = row.evaluate_handle(
                '''row => {
                    const nextRow = row.nextElementSibling;
                    if (nextRow && nextRow.classList.contains('spacer')) {
                        return null;
                    }
                    return nextRow?.querySelector('.score');
                }''', row)
            
            if title_element:
                title = title_element.inner_text().strip()
                points = points_element.inner_text().strip() if points_element else '0 points'
                print(f"{title} - {points}")
                count += 1
                if count >= 5:
                    break
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path='screenshot.png')
        print('screenshot saved')
    finally:
        browser.close()