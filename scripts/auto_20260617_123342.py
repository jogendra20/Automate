from playwright.sync_api import sync_playwright
import os

USERNAME = "249xa33045"  # Roll Number
PASSWORD = "20012007"    # DOB in DD/MM/YYYY format

run_id = os.environ.get('RUN_ID', '')

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    try:
        page.goto("https://examcell.gprec.ac.in/StudentDetails/StudentDetailsLogin.aspx?service=%27Academic%20Performance%27", wait_until="domcontentloaded", timeout=30000)
        page.fill('input[name="txtRollNo"]', USERNAME)
        page.fill('input[name="txtDOB"]', PASSWORD)
        page.click('input[value="Get Details"]')
        page.wait_for_load_state("domcontentloaded")
        time.sleep(8)  # Additional wait for dynamic content
        print(page.title())
        page.screenshot(path="screenshot.png", full_page=True)
        print("screenshot saved")
    except Exception as e:
        print(f"ERROR: {e}")
        page.screenshot(path="screenshot.png", full_page=True)
        print("screenshot saved")
    finally:
        browser.close()