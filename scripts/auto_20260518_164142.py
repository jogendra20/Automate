from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page()
        page.goto("https://www.google.com")
        page.fill("textarea[name='q']", "bitcoin price")
        page.keyboard.press("Enter")
        page.wait_for_selector("#search")
        results = page.inner_text("#search")
        print(results)
        browser.close()

if __name__ == "__main__":
    main()