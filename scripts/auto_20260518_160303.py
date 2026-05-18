import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nse_top_gainers():
    headers = {
        'User-Agent': os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.nseindia.com/'
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        # Get main page to set cookies
        main_url = 'https://www.nseindia.com'
        response = session.get(main_url, timeout=10)
        response.raise_for_status()

        # Get top gainers data from API
        api_url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers'
        api_response = session.get(api_url, timeout=10)
        api_response.raise_for_status()

        data = api_response.json()
        records = data.get('data', [])

        if not records:
            print("No data found for top gainers")
            return

        # Create DataFrame and print results
        df = pd.DataFrame(records)
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("No data available after processing")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    scrape_nse_top_gainers()