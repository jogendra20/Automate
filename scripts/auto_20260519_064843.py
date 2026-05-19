import os
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        page.goto("https://www.gprec.ac.in", wait_until="domcontentloaded")
        page.wait_for_timeout(30000)
        screenshot = page.screenshot()
        print(screenshot)
        browser.close()

if __name__ == "__main__":
    main()