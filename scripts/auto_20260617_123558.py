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
        page.goto('https://example.com', wait_until='domcontentloaded', timeout=30000)
        time.sleep(8)
        all_selectors = page.evaluate("""() => {
            let elements = document.querySelectorAll('*');
            let selectors = Array.from(elements).map(el => {
                let tag = el.tagName.toLowerCase();
                let id = el.id ? `#${el.id}` : '';
                let classes = (el.className && el.className.length > 0) 
                    ? `.${el.className.trim().split(/\\s+/).join('.')}` : '';
                return `${tag}${id}${classes}`;
            });
            return Array.from(new Set(selectors));
        }""")
        for selector in all_selectors[:100]:  # Limit to first 100 selectors for brevity
            print(selector)
        time.sleep(2)
    except Exception as e:
        print(f'ERROR: {e}')
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
    finally:
        browser.close()