import os
import json
from playwright.sync_api import sync_playwright

def scrape_books():
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
        book_titles = [title.get_attribute("title") for title in titles]

        browser.close()

        print(book_titles)

        output = {"books": book_titles}
        with open("output.json", "w") as f:
            json.dump(output, f, indent=2)

if __name__ == "__main__":
    scrape_books()