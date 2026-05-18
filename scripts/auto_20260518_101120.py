import json
import os
from playwright.sync_api import sync_playwright

def scrape_books():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        page = browser.new_page()
        page.goto('https://books.toscrape.com')

        titles = []
        book_elements = page.query_selector_all('article.product_pod h3 a')
        for i, book in enumerate(book_elements[:5]):
            title = book.get_attribute('title')
            titles.append(title)

        browser.close()

        print(json.dumps(titles, indent=2))

        output_file = os.getenv('OUTPUT_FILE', 'output.json')
        with open(output_file, 'w') as f:
            json.dump(titles, f, indent=2)

if __name__ == '__main__':
    scrape_books()