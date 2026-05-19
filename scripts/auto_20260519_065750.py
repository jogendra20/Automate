import os
import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()
        page.goto("https://www.gprec.ac.in", timeout=30000)
        time.sleep(30)
        page.click("text=Student-Services")
        screenshot = page.screenshot()
        print("Screenshot captured")
        browser.close()

if __name__ == "__main__":
    main()