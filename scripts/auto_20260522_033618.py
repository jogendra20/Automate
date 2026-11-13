# Required imports
from playwright.sync_api import sync_playwright
import time, os
from scrapling import Fetcher

# Get RUN_ID
run_id = os.environ.get('RUN_ID', '')

try:
    # Standard Browser Launch with Stealth
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
        )
        page = browser.new_page(viewport={'width':1280,'height':800})
        from playwright_stealth import stealth_sync
        stealth_sync(page)
        
        try:
            # Navigate to arxiv.org/list/cs.AI/recent
            page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=45000)
            time.sleep(6)

            # Extract top 10 paper titles
            rows = page.query_selector_all("dl > dt + dd")
            titles = []
            counter = 0
            for row in rows[:10]:
                title = row.query_selector("div.meta > div.list-title").inner_text()  
                title = title.replace('Title: ', '').strip()
                titles.append(title)
                counter += 1
                if counter >= 10:
                    break
            print("Titles:")
            for title in titles:
                print(title)

        except Exception as e:
            print(f'ERROR: {e}')

        finally:
            # Save a screenshot before closing the browser
            browser.close()

except Exception as e:
    print(f'ERROR: {e}')

    # Scrapling to retry the task
    fetcher = Fetcher(auto_match=False)
    page = fetcher.get('https://arxiv.org/list/cs.AI/recent')
    content = page.html
    import re
    rows = re.findall(r'<dd>.*?<div class="list-title">(.*?)</div>.*?</dd>', content, re.DOTALL)
    titles = [title.strip() for title in rows[:10]]
    print("Titles:")
    for title in titles:
        print(title)

    # Save a screenshot
    import tempfile
    with tempfile.NamedTemporaryFile() as fp:
        page.save(fp.name, full_page=True)
        print("screenshot saved")
# Historical note: this recipe was generated with a Scrapling fallback and
# screenshot support. Keep prose as comments so the file remains valid Python.
