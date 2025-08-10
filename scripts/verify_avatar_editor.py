from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    page.goto("https://localhost:5173/")

    # Wait for the avatar to be visible and then click it
    avatar = page.locator(".v-avatar")
    expect(avatar).to_be_visible()
    avatar.click()

    # Wait for the dialog to be visible
    dialog = page.locator(".v-dialog")
    expect(dialog).to_be_visible(timeout=10000)

    # Take a screenshot of the editor
    page.screenshot(path="jules-scratch/verification/avatar_editor.png")

    # Click the AI Generate button
    page.get_by_role("button", name="AI Generate").click()

    # Wait for the loading indicator to disappear
    expect(page.locator(".v-progress-circular")).not_to_be_visible(timeout=60000)

    # Take a screenshot of the generated image
    page.screenshot(path="jules-scratch/verification/generated_avatar.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
