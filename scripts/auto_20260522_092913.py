from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth_sync
import os
import time
from bs4 import BeautifulSoup, SoupStrainer

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    stealth_sync(page)
    try:
        page.goto('https://news.ycombinator.com/', wait_until='domcontentloaded', timeout=45000)
        time.sleep(8)
        content = page.inner_html()
        soup = BeautifulSoup(content, 'html.parser', parse_only=SoupStrainer('tr'))
        titles = soup.select('.athing > .titleline > a')
        scores = soup.select('.score')
        for i, (title, score) in enumerate(zip(titles, scores)):
            if i >= 10:
                break
            post_title = title.text.strip()
            points = score.text.strip()
            print(f"{i+1}. {post_title} - {points}")
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
    except TimeoutError:
        print("Timeout error: unable to scrape page")
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
    except Exception as e:
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
        print(f"ERROR: {e}")
    finally:
        browser.close()