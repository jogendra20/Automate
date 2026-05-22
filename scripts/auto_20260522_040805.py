import os
import time
from scrapling import Fetcher
import playwright
from playwright.sync_api import sync_playwright

try:
    playwright.__version__
except AttributeError:
    playwright = playwright.__spec__.parent

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
    )
    page = browser.new_page(viewport={'width':1280,'height':800})
    try:
        # Navigate to the page and wait for content to load
        page.goto('https://arxiv.org/list/cs.AI/recent', wait_until='domcontentloaded', timeout=45000)
        
        # Save screenshot of the page
        page.screenshot(path='screenshot.png')
        print('screenshot saved')
        
        # Use Scrapling instead of Playwright
        fetcher = Fetcher(auto_match=False)
        page = fetcher.get('https://arxiv.org/list/cs.AI/recent', stealthy_headers=True)
        
        # Extract top 10 papers
        papers = page.css('div#content dl dd div.list-title a')
        for paper in papers[:10]:
            title = paper.text.strip()
            print(f"Title: {title}")
            paper_url = paper.attrib.get('href', '')
            print(f"Link: {paper_url}")
            print()
    except Exception as e:
        print('ERROR: ' + str(e))
    finally:
        browser.close()