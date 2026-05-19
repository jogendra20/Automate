import os
import requests
from playwright.sync_api import sync_playwright
from time import sleep

api_key = os.getenv('NSE_API_KEY')
url = f'https://api.nseindia.com/market_data/stocks/{api_key}'
response = requests.get(url)
cookies = dict(response.cookies)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, 
                                args=['--no-sandbox', '--disable-dev-shm-usage'])
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size(800, 600)
    page.goto('https://twitter.com/')

    sleep(30)

    page.screenshot(path='screenshot.png')

    browser.close()