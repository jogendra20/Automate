from playwright.sync_api import sync_playwright

def scrape_books_toscrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page()

        page.goto("https://books.toscrape.com/", timeout=10000)
        titles = page.query_selector_all("h3 a")

        results = [title.inner_text() for title in titles]

        browser.close()

        for title in results:
            print(title)

scrape_books_toscrape()