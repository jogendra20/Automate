import os
import time
from playwright.sync_api import sync_playwright

def main():
    username = os.getenv("SHIKAMARU_USERNAME")
    password = os.getenv("SHIKAMARU_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, 
                                     args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://shikamaru-ui.vercel.app/")

        time.sleep(10)

        page.screenshot(path="screenshot.png")

        browser.close()

if __name__ == "__main__":
    main()