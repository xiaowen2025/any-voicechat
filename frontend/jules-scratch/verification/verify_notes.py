from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    try:
        page.goto("https://localhost:5173/")

        # Click the "Start Interview" button
        page.get_by_role("button", name="Start Interview").click()

        # Wait for the conversation to start and for some notes to be generated
        page.wait_for_timeout(5000)

        # Take a screenshot of the notes window
        notes_window = page.locator('.notes-window')
        notes_window.screenshot(path="frontend/jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
