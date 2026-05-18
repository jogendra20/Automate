import os
from playwright.sync_api import sync_playwright

def scrape_book_titles():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        page = browser.new_page()
        page.goto("https://books.toscrape.com")

        titles = page.locator(".product_pod h3 a").all()[:5]
        for title in titles:
            print(title.get_attribute("title"))

        browser.close()

if __name__ == "__main__":
    scrape_book_titles()