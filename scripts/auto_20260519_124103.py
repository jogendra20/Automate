from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service=%27Academic%20Performance%27", wait_until="networkidle", timeout=60000)
    time.sleep(5)
    page.fill('input[placeholder="Username"]', "249xa33045")
    page.fill('input[id="txtPassword"]', "2478888")
    page.click('input[id="btnLogin"]')
    page.wait_for_load_state("networkidle")
    page.screenshot(path="screenshot.png")
    print("Screenshot taken successfully")
    browser.close()