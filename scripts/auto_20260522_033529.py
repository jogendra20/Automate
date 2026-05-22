# Required imports
from playwright.sync_api import sync_playwright
import time, os

# Get RUN_ID
run_id = os.environ.get('RUN_ID', '')

# Standard Browser Launch with Stealth
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
    )
    page = browser.new_page(viewport={'width':1280,'height':800})
    stealth_sync(page)

    try:
        # Navigate to arxiv.org/list/cs.AI/recent
        page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=45000)
        time.sleep(6)

        # Extract top 10 paper titles and authors
        rows = page.query_selector_all("dl > dt + dd")
        titles = []
        authors = []
        counter = 0
        for row in rows[:10]:
            title = row.query_selector("div.meta > div.list-title").inner_text()  # Corrected the CSS selector
            title = title.replace('Title: ', '').strip()
            authors_list = row.query_selector("div.meta > div.list-authors a").inner_text().split(', ')  # Modified the CSS selector
            authors.append([a.strip() for a in authors_list])  # Fixed author names
            titles.append(title)
            counter += 1
            if counter >= 10:
                break
        print("Titles and Authors:")
        for title, author in zip(titles, authors):
            print(f"{title} ({', '.join(author)})")

    except Exception as e:
        print(f'ERROR: {e}')

    finally:
        # Save a screenshot before closing the browser
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
        browser.close()