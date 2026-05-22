# Import required libraries
from playwright.sync_api import sync_playwright
import time, os

# Set environment variables
run_id = os.environ.get('RUN_ID', '')

# Launch the browser in headless mode
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
    )
    page = browser.new_page(viewport={'width':1280,'height':800})
    stealth_sync(page)
    try:
        # Navigate to the page and wait for content to load
        page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=45000)
        
        # Extract top 10 papers
        papers = page.query_selector_all("div#content dl article")
        for paper in papers[:10]:
            title = paper.query_selector("div.list-title.mathjax::text").inner_text().strip().replace("Title: ", "")
            print(f"Title: {title}")
            paper_url = paper.query_selector("div.meta div.list-title.mathjax a").attrib.get("href", "")
            paper_response = page.goto(paper_url, wait_until='domcontentloaded', timeout=45000)
            author_list = paper_response.query_selector("div.authorslist a").query_selector_all("a")
            authors = [author.inner_text().strip() for author in author_list]
            print(f"Authors: {authors}")
            print()
    except Exception as e:
        print(f'ERROR: {e}')
    finally:
        browser.close()
        # Save screenshot of the page
        page.screenshot(path='screenshot.png')
        print('screenshot saved')