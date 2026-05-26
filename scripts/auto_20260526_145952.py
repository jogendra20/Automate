from playwright.sync_api import sync_playwright
import os, time, requests

run_id = os.environ.get('RUN_ID', '')

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
        )
        page = browser.new_page(viewport={'width':1280,'height':800})
        
        page.goto('https://it.com', wait_until='domcontentloaded', timeout=45000)
        time.sleep(15) # wait for domcontentloaded on it.com or similar sites
        
        # scrape the page
        content = page.inner_text('body')
        print(content[:3000])
        
        page.screenshot(path="screenshot.png", full_page=False)
        print('screenshot saved')
        
except Exception as e:
    print(f'ERROR: {e}')
    
finally:
    browser.close()