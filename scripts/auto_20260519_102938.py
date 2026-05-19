import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://gprec.ac.in"
session = requests.Session()
session.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    },
    timeout=10
)

res = session.get(url + "/faculty", headers=session.headers, timeout=10)
soup = BeautifulSoup(res.text, 'lxml')
data = [item.split('<h4>')[-1].replace('</h4>', '').strip() for item in soup.find_all('p') if '<h4>' in str(item)]

faculty_names = []
departments = []
for item in data:
    name, department = item.split('<br>')
    faculty_names.append(name.strip())
    departments.append(department.strip())

df = pd.DataFrame({
    'Faculty Name': faculty_names,
    'Department': departments
})
df.to_csv('faculty_data.csv', index=False)

print(df)

import os
import playwright.sync_api as sync_playwright

faculty_url = "https://gprec.ac.in/faculty"
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(faculty_url, wait_until="networkidle", timeout=60000)

    data = page.query_selector_all("p")
    faculty_names = []
    departments = []
    for item in data:
        text = item.inner_text().strip()
        if '<h4>' in text:
            name, department = text.split('<h4>')
            faculty_names.append(name.strip())
            departments.append(department.strip())

    df = pd.DataFrame({
        'Faculty Name': faculty_names,
        'Department': departments
    })
    df.to_csv('faculty_data.csv', index=False)

    page.screenshot(path="screenshot.png")
    browser.close()