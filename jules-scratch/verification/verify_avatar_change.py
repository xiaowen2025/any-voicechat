from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    try:
        page.goto("https://localhost:5173")

        # Click the apps button to open the gallery
        apps_button = page.get_by_role("button", name="apps")
        expect(apps_button).to_be_visible()
        apps_button.click()

        # Click the "Interview Simulator" app
        interview_simulator_card = page.get_by_text("Interview Simulator")
        expect(interview_simulator_card).to_be_visible()
        interview_simulator_card.click()

        # Wait for the avatar to change
        avatar = page.locator(".v-avatar img")
        expect(avatar).to_have_attribute("src", "/assets/avatar_interview_simulator.png")

        # Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
