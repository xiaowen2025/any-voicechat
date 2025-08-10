from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://localhost:5176/")

    # Click the settings button
    settings_button = page.get_by_role("button", name="Show Settings JSON")
    settings_button.click()

    # Wait for the dialog to be visible
    dialog = page.get_by_role("dialog")
    expect(dialog).to_be_visible()

    # Take a screenshot
    page.screenshot(path="jules-scratch/verification/verification.png")

    browser.close()
