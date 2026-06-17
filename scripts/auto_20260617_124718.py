from playwright.sync_api import sync_playwright
import time, os

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    try:
        page.goto("https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service='Academic Performance'", wait_until='domcontentloaded', timeout=30000)
        time.sleep(8)

        # Fill credentials
        ROLL_NO = "249xa33045"
        DOB = "20012007"
        page.locator("#ctl00_ContentPlaceHolder1_dfRollNo").fill(ROLL_NO)
        page.locator("#ctl00_ContentPlaceHolder1_dfDob").fill(DOB)

        # Click Get Details
        page.locator("#ctl00_ContentPlaceHolder1_ImageButton1").click()
        time.sleep(8)

        # Screenshot after submission
        page.screenshot(path="screenshot.png")
        print("screenshot saved")

        print(page.title())
        print(page.url)
    except Exception as e:
        page.screenshot(path="screenshot.png")
        print("screenshot saved")
        print(f"ERROR: {e}")
    finally:
        browser.close()