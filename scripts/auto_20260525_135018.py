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
        page.goto('https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service=%27Academic%20Performance%27', wait_until='domcontentloaded', timeout=45000)
        time.sleep(8)
        page.screenshot(path='screenshot.png', full_page=False)
        print('screenshot saved')
    except Exception as e:
        print(f'ERROR: {e}')
    finally:
        browser.close()