import os
from playwright.sync_api import sync_playwright

url = os.getenv('URL', 'https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service=%27Academic%20Performance%27')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(url, wait_until="networkidle", timeout=60000)
    time.sleep(5)
    page.screenshot(path="screenshot.png", full_page=False)
    browser.close()