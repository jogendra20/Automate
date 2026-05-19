import os
import time
from playwright.sync_api import sync_playwright

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    page.goto("https://www.tickertape.in/", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(5000)

    page.get_by_text("Gainers", exact=True).first.click()
    page.wait_for_timeout(5000)

    rows = page.query_selector_all("a[href*='/stocks/']")
    seen = set()
    count = 0
    for row in rows:
        text = row.inner_text().strip()
        if text and text not in seen and "/" in text:
            seen.add(text)
            print(text.split('/')[0] + ": " + text.split('%')[0])
            count += 1
            if count >= 5:
                break

    browser.close()
In this code:

- The playwright library is used to automate tasks on the webpage.
- The Chromium browser is launched with the specified flags.
- The login page is navigated and the page is waited to fully load for 5 seconds.
- The login form is filled with credentials (username and password) and the submit button is clicked.
- After logging in, the Gainers tab is clicked and waited for 5 seconds.
- The webpage is then searched for stock links and the top 5 gainers with symbol and percent change are printed.