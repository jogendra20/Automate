from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service=%27Academic+Performance%27", wait_until="networkidle", timeout=30000)
    time.sleep(5)
    page.screenshot(path="screenshot.png", full_page=False)
    browser.close()