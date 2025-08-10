from playwright.sync_api import sync_playwright, expect
import re

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    try:
        page.goto("https://localhost:5173/")

        # Click the settings button
        settings_button = page.locator('button:has(i.mdi-cog)')
        expect(settings_button).to_be_visible()
        settings_button.click()

        # Wait for the settings dialog to appear
        settings_dialog = page.locator('div.v-dialog')
        expect(settings_dialog).to_be_visible()

        # Find the textarea and check its content
        settings_textarea = settings_dialog.locator('textarea.v-field__input:not(.v-textarea__sizer)')
        expect(settings_textarea).to_have_value(re.compile(r'.*"app_name": "Language Pal".*'))

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
