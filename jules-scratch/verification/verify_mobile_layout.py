from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    page.goto("https://localhost:5174")

    # Desktop view
    page.set_viewport_size({"width": 1280, "height": 720})
    page.screenshot(path="jules-scratch/verification/desktop_view.png")

    # Mobile view
    page.set_viewport_size({"width": 375, "height": 667})
    page.screenshot(path="jules-scratch/verification/mobile_view.png")

    # Mobile view with sidebar
    page.get_by_role("button", name="Open navigation drawer").click()
    page.screenshot(path="jules-scratch/verification/mobile_view_sidebar.png")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
