import os
import requests
from bs4 import BeautifulSoup

def scrape_nse_top_gainers():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.nseindia.com/'
    }

    session = requests.Session()
    session.headers.update(headers)

    # Step 1: Get main page to set cookies
    main_url = 'https://www.nseindia.com'
    try:
        response = session.get(main_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching main page: {e}")
        return

    # Step 2: Get top gainers data from API
    api_url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers'
    try:
        response = session.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching gainers data: {e}")
        return

    if 'data' not in data or not data['data']:
        print("No gainers data found")
        return

    print("NSE Top Gainers:")
    print("{:<10} {:<20} {:<15} {:<15} {:<15}".format(
        "Symbol", "Series", "Prev Close", "Last Price", "Change (%)"))
    print("-" * 80)

    for item in data['data'][:10]:  # Top 10 gainers
        symbol = item.get('symbol', 'N/A')
        series = item.get('series', 'N/A')
        prev_close = item.get('previousClose', 'N/A')
        last_price = item.get('lastPrice', 'N/A')
        change = item.get('pChange', 'N/A')

        print("{:<10} {:<20} {:<15} {:<15} {:<15}".format(
            symbol, series, prev_close, last_price, change))

if __name__ == "__main__":
    scrape_nse_top_gainers()