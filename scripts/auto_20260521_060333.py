from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://www.gprec.ac.in", wait_until="networkidle", timeout=60000)
    time.sleep(3)
    page.screenshot(path="screenshot.png", full_page=False)
    print("screenshot saved")
    browser.close()