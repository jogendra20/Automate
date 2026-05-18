import os
from playwright.sync_api import sync_playwright

def scrape_nse_top_gainers():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        page = browser.new_page()
        page.goto('https://www.nseindia.com/market-data/top-gainers-losers')

        # Wait for the table to load
        page.wait_for_selector('table.dataTable')

        # Extract top gainers data
        gainers = []
        rows = page.query_selector_all('table.dataTable tbody tr')
        for row in rows[:10]:  # Top 10 gainers
            cells = row.query_selector_all('td')
            if len(cells) >= 5:
                symbol = cells[1].inner_text().strip()
                ltp = cells[2].inner_text().strip()
                chg = cells[3].inner_text().strip()
                chg_pct = cells[4].inner_text().strip()
                gainers.append({
                    'Symbol': symbol,
                    'LTP': ltp,
                    'Change': chg,
                    'Change%': chg_pct
                })

        browser.close()
        print(gainers)

if __name__ == '__main__':
    scrape_nse_top_gainers()