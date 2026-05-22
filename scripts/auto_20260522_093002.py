import os
from playwright.sync_api import sync_playwright
import time

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    try:
        page.goto('https://news.ycombinator.com/', wait_until='domcontentloaded', timeout=45000)
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
        items = page.query_selector_all("tr.athing")
        for i, item in enumerate(items):
            if i >= 10:
                break
            try:
                link = item.query_selector("a")  # QuerySelectorAll doesn't support atribute selector in non-executable mode
                post_title = link.text_content()
                score = item.query_selector("span.score").text_content()
                print(f"{i+1}. {post_title} - {score}")
            except Exception as e:
                print(f"Error fetching post {i+1}: {e}")
    except Exception as e:
        print('screenshot saved')
        print(f"ERROR: {e}")
    finally:
        browser.close()