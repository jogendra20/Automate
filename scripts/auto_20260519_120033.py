from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://www.tickertape.in/", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(5000)
    content = page.inner_text("body")
    print(content)
    browser.close()