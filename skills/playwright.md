# Playwright Skill - GitHub Actions Ubuntu

## RULES (never break these)
- Never set PLAYWRIGHT_EXECUTABLE_PATH
- Never use wait_until=networkidle on Indian sites - use domcontentloaded + time.sleep(8)
- Always read: run_id = os.environ.get('RUN_ID', '')
- Always wrap entire script in try/except and print errors
- Screenshots always saved as screenshot.png
- Never use data-testid or .classname selectors without verifying

## Standard Browser Launch

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
        pass  # your code here
    except Exception as e:
        print(f'ERROR: {e}')
    finally:
        browser.close()

## Screenshot a page

page.goto('https://example.com', wait_until='domcontentloaded', timeout=45000)
time.sleep(8)
page.screenshot(path='screenshot.png', full_page=False)
print('screenshot saved')

## Scrape unknown page

page.goto('https://example.com', wait_until='domcontentloaded', timeout=45000)
time.sleep(6)
content = page.inner_text('body')
print(content[:3000])

## Tickertape top gainers (VERIFIED working)

page.goto('https://www.tickertape.in/', wait_until='domcontentloaded', timeout=45000)
time.sleep(10)
try:
    page.get_by_text('Gainers', exact=True).first.click()
    time.sleep(4)
except:
    pass
rows = page.query_selector_all("a[href*='/stocks/']")
seen = set()
count = 0
for row in rows:
    text = row.inner_text().strip()
    if text and text not in seen and len(text) > 2:
        seen.add(text)
        print(text)
        count += 1
        if count >= 10:
            break

## Fill and submit form

page.goto('https://example.com/login', wait_until='domcontentloaded', timeout=45000)
time.sleep(4)
page.fill('input[name="username"]', 'value')
page.fill('input[name="password"]', 'value')
page.click('button[type="submit"]')
time.sleep(4)
print(page.title())

## SITE RULES
- nseindia.com: DO NOT USE - blocks all scrapers
- Use tickertape.in or api.tickertape.in for NSE data
- For Indian govt sites: domcontentloaded + time.sleep(15)
- moneycontrol.com: use inner_text('body'), selectors change frequently
