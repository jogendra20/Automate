import time
from playwright.sync_api import sync_playwright
import pandas as pd
import os

url = os.getenv('URL') or 'https://www.tickertape.in/'
username = os.getenv('USERNAME') or 'your_username'
password = os.getenv('PASSWORD') or 'your_password'

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(url, wait_until="networkidle", timeout=60000)
    time.sleep(5)
    page.screenshot(path="screenshot.png", full_page=False)

    try:
        page.get_by_text("Log in", exact=True).first.click()
        time.sleep(0.5)
    except:
        page.get_by_text("Login", exact=True).first.click()
        time.sleep(0.5)

    page.fill('#email', username)
    page.fill('#password', password)
    page.click('#login-form-submit')
    page.wait_for_load_state("networkidle")
    print(page.title())

    page.goto(url, wait_until="networkidle", timeout=60000)
    time.sleep(10)

    page.goto(url, wait_until="networkidle", timeout=60000)
    try:
        page.get_by_text("Gainers", exact=True).first.click()
        page.wait_for_timeout(2000)
    except:
        pass

    rows = page.query_selector_all("a[href*='/stocks/']")
    seen = set()
    gainers_df = pd.DataFrame(columns=['Symbol', 'Percent Change'])
    count = 0
    for row in rows:
        text = row.inner_text().strip()
        if text and text not in seen and "%" in text:
            seen.add(text)
            symbol, percent_change = text.split(' ')
            gainers_df.loc[count, 'Symbol'] = symbol
            try:
                gainers_df.loc[count, 'Percent Change'] = float(percent_change.replace('%', ''))
            except ValueError:
                percent_change = percent_change.strip('()')
                try:
                    gainers_df.loc[count, 'Percent Change'] = float(percent_change.replace('%', ''))
                except ValueError:
                    gainer_text = row.get_attribute('innerHTML')
                    gainer_text = gainer_text.replace('<span>', '').replace('</span>', '').replace('<strong>', '').replace('</strong>', '')
                    gainer_text = gainer_text.split('<br/>')
                    percent_change = [x for x in gainer_text if ':' in x][1]
                    percent_change = percent_change.strip().replace(':', '')
                    gainer_text = [x for x in gainer_text if 'Change' in x][0]
                    symbol = [x for x in gainer_text.replace('Change', '').split('<span>') if x][0].strip()
                    gainer_text = [x for x in gainer_text.replace('Change', '').split('<span>') if x][0].strip()
                    try:
                        gainers_df.loc[count, 'Percent Change'] = float(percent_change.replace('%', '')) / 100
                    except:
                        continue
            gainer_text = row.get_attribute('innerHTML')
            gainer_text = gainer_text.replace('<span>', '').replace('</span>', '').replace('<strong>', '').replace('</strong>', '')
            gainer_text = gainer_text.split('<br/>')
            gainer_text = [x for x in gainer_text if ':' in x][0]
            try:
                gainers_df.loc[count, 'Symbol'] = gainer_text.split(':')[1].strip()
            except:
                continue
            print(symbol, gainers_df.loc[count, 'Percent Change'].round(2))
            gainers_df.to_csv('gainers.csv', index=False)
            count += 1
            if count >= 5:
                break
    browser.close()