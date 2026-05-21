from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    try:
        page.goto("https://www.gprec.ac.in", wait_until="domcontentloaded", timeout=30000)
        time.sleep(15)
        page.screenshot(path="screenshot.png", full_page=False)
        print("screenshot saved")
    except:
        page.screenshot(path="screenshot.png", full_page=False)
        print("screenshot saved")
    browser.close()