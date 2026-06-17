from playwright.sync_api import sync_playwright
import os
import time

ROLL_NO = "249xa33045"
DOB = "20012007"  # Example: 25032005

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    try:
        page.goto(
            "https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service='Academic Performance'",
            wait_until="domcontentloaded",
            timeout=30000
        )
        time.sleep(8)
        page.fill("#ctl00_ContentPlaceHolder1_dfRollNo", ROLL_NO)
        page.fill("#ctl00_ContentPlaceHolder1_dfDob", DOB)
        page.click("#ctl00_ContentPlaceHolder1_ImageButton1")
        time.sleep(8)
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
        print(page.title())
        print(page.url)
    except Exception as e:
        print(f"ERROR: {e}")
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
    finally:
        browser.close()