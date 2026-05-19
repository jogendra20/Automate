from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = browser.new_page()
    page.goto("https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service=%27Academic%20Performance%27", timeout=60000)
    page.wait_for_load_state("networkidle")
    time.sleep(5)
    print(page.inner_text())
    page.screenshot(path="screenshot.png")
    browser.close()