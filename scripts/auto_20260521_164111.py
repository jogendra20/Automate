from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    try:
        page.goto("http://www.gprec.ac.in", wait_until="domcontentloaded", timeout=30000)
        time.sleep(15)
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    except Exception as e:
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    finally:
        browser.close()