# Playwright Skill - GitHub Actions Ubuntu

## RULES (never break these)
- Never set PLAYWRIGHT_EXECUTABLE_PATH
- Never use wait_until=networkidle on Indian sites - use domcontentloaded + time.sleep(8)
- Always read: run_id = os.environ.get('RUN_ID', '')
- Always wrap entire script in try/except and print errors
- Screenshots always saved as screenshot.png
- Never use data-testid or .classname selectors without verifying

## Standard Browser Launch (with stealth — always use this)

from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time, os

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']
    )
    page = browser.new_page(viewport={'width':1280,'height':800})
    stealth_sync(page)
    try:
        pass  # your code here
    except Exception as e:
        print(f'ERROR: {e}')
    finally:
        browser.close()

## Old Standard Browser Launch (no stealth - do not use)

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

page.goto('https://www.tickertape.in/market-movers', wait_until='domcontentloaded', timeout=45000)
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


## Scrapling (use for static HTML sites — faster and stealthier than Playwright)

from scrapling import Fetcher
import os

run_id = os.environ.get('RUN_ID', '')
fetcher = Fetcher(auto_match=False)

## Scrapling basic fetch

page = fetcher.get('https://example.com', stealthy_headers=True)
print(page.status)
print(page.html[:2000])

## Scrapling extract text by CSS selector

page = fetcher.get('https://example.com', stealthy_headers=True)
items = page.css('div.stock-name')
for item in items:
    print(item.text)

## Scrapling extract table rows

page = fetcher.get('https://example.com', stealthy_headers=True)
rows = page.css('table tr')
for row in rows[:20]:
    cols = row.css('td')
    print([c.text for c in cols])

## Scrapling extract all links

page = fetcher.get('https://example.com', stealthy_headers=True)
links = page.css('a')
for link in links[:20]:
    print(link.attrib.get('href',''), link.text)

## DECISION RULE
- Use Scrapling when: site is news, blog, govt, static data, no JS required
- Use Playwright+stealth when: site is React/Vue/Next.js (Tickertape, Groww, Zerodha)
- When unsure: try Scrapling first, fall back to Playwright if output is empty
