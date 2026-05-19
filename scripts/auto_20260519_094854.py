import os
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

def get_nse_headers():
    url = 'https://www.nseindia.com'
    headers = {
        'User-Agent': os.getenv('USER_AGENT'),
        'Accept': 'application/json, text/plain, */*',
        'Referer': url
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return headers, response.cookies

def get_nse_data(headers, cookies):
    url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers'
    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()
    return response.json()

def main():
    headers, cookies = get_nse_headers()
    nse_data = get_nse_data(headers, cookies)
    print("NSE Data:")
    import json
    print(json.dumps(nse_data, indent=4))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
        context = browser.new_context()
        page = context.new_page()
        
        url = 'https://shikamaru-ui.vercel.app/'
        page.goto(url)
        page.wait_for_timeout(5000)  # wait for 5 seconds
        context.screenshot(path='screenshot.png', full_page=True)  # send screenshot
        print("Screenshot sent")
        
        browser.close()

if __name__ == "__main__":
    import os
    os.getenv('USER_AGENT')
    main()

However, the above script will fail because the screenshot path is not a valid file path and the screenshot is not saved. Here's the corrected version of the script:

import os
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup

def get_nse_headers():
    url = 'https://www.nseindia.com'
    headers = {
        'User-Agent': os.getenv('USER_AGENT'),
        'Accept': 'application/json, text/plain, */*',
        'Referer': url
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return headers, response.cookies

def get_nse_data(headers, cookies):
    url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainer'
    response = requests.get(url, headers=headers, cookies=cookies)
    response.raise_for_status()
    return response.json()

def main():
    headers, cookies = get_nse_headers()
    nse_data = get_nse_data(headers, cookies)
    print("NSE Data:")
    import json
    print(json.dumps(nse_data, indent=4))

    user_agent = os.getenv('USER_AGENT')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        
        url = 'https://shikamaru-ui.vercel.app/'
        page.goto(url)
        page.wait_for_timeout(5000)  # wait for 5 seconds
        buffer = page.screenshot(full_page=True)  # take screenshot
        print(f"Screenshot taken (size: {buffer.size})")
        
        browser.close()

if __name__ == "__main__":
    os.getenv('USER_AGENT')
    main()