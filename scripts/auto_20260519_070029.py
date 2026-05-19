import os
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto("https://www.gprec.ac.in", wait_until="domcontentloaded")
        page.wait_for_timeout(30000)
        page.click("text=Student-Services")
        page.screenshot(path="screenshot.png", full_page=True)
        browser.close()

if __name__ == "__main__":
    main()