# Playwright Automation Skills

## Browser Launch (Always use these exact flags)

from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})

## Screenshot (Always save as screenshot.png)

page.goto("https://example.com", wait_until="networkidle", timeout=60000)
time.sleep(10)
page.screenshot(path="screenshot.png", full_page=False)
browser.close()

## Wait Strategies

page.wait_for_load_state("networkidle")
time.sleep(5)

## Extract text from any page (use this when selector is unknown)

page.goto("https://example.com", wait_until="networkidle", timeout=60000)
page.wait_for_timeout(5000)
content = page.inner_text("body")
print(content[:3000])

## Click tab by visible text

try:
    page.get_by_text("Gainers", exact=True).first.click()
    page.wait_for_timeout(2000)
except:
    pass

## Extract stock links (VERIFIED working on Tickertape)

rows = page.query_selector_all("a[href*='/stocks/']")
seen = set()
count = 0
for row in rows:
    text = row.inner_text().strip()
    if text and text not in seen and "%" in text:
        seen.add(text)
        print(text)
        count += 1
        if count >= 5:
            break

## Form Fill

page.fill('input[name="username"]', "value")
page.fill('input[name="password"]', "value")
page.click('button[type="submit"]')
page.wait_for_load_state("networkidle")
print(page.title())

## SITE RULES

Always use Playwright. Never use requests or urllib to fetch web pages.
Never use data-testid selectors unless you have verified they exist.
Never use div.classname selectors unless you have verified they exist.
For unknown pages, always use inner_text("body") first to see what is rendered.
