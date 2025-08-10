from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)  # Ignore HTTPS errors for localhost
    page = context.new_page()

    try:
        page.goto("https://localhost:5173/")

        # Click on the avatar to open the editor
        page.locator(".v-avatar").click()

        # Wait for the dialog to appear
        page.wait_for_selector(".v-dialog")

        # Take a screenshot of the dialog
        page.locator(".v-dialog").screenshot(path="jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
