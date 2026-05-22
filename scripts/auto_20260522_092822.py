# import required libraries. No extra unused imports
from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth as stealth_sync
import os

# extract RUN ID from environment before running
run_id = os.environ.get('RUN_ID', '')

# always use --no-sandbox and --disable-dev-shm-usage for this runner
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    stealth_sync(page)
    try:
        # perform a domcontentloaded goto
        page.goto('https://news.ycombinator.com/')
        # capture a page after it has loaded
        time.sleep(8)
        # select all table rows with class 'athing', each contains a 'titleline' with an anchor tag
        titles = page.query_selector_all('tr.athing .titleline > a')
        # select all score spans
        scores = page.query_selector_all('span.score')
        # iterate over pairs of title and score
        for i, (title, score) in enumerate(zip(titles, scores)):
            # break after 10 cycles for brevity
            if i >= 10:
                break
            # inner text of title anchor tag
            post_title = title.inner_text().strip()
            # inner text of score tag
            points = score.inner_text().strip()
            # print the extracted fields
            print(f"{i+1}. {post_title} - {points}")
        
        # capture a full page screenshot
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
    except TimeoutError:
        print("Timeout error: unable to scrape page")
        # still capture a screenshot for diagnostics
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
    except Exception as e:
        # capture a screenshot for diagnostics
        page.screenshot(path='screenshot.png', full_page=True)
        print('screenshot saved')
        # print the actual error
        print(f'ERROR: {e}')
    finally:
        # ensure browser is closed before exiting
        browser.close()