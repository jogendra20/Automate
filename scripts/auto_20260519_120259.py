from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://www.tickertape.in/", wait_until="networkidle", timeout=60000)
    time.sleep(10)

    # Find the Today's stocks Gainers section
    section = page.query_selector("//section[@data-testid='gainers']")
    if section:
        # Get all gainers
        gainers = section.query_selector_all("//ul[@class='list list--inline list--inline-2']/li")
        gainers = [gainer for gainer in gainers[:5]]  # top 5 gainers
        # Extract symbol and percentage
        for gainer in gainers:
            symbol = gainer.query_selector(".list__item > a").text_content().strip()
            percentage = gainer.query_selector(".percentage > span").text_content().strip().replace('%', '')
            print(f"Symbol: {symbol}, Percentage: {percentage}")
    else:
        print("Gainers section not found")

    browser.close()