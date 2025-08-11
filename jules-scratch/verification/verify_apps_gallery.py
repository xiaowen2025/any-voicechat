from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)  # Ignore SSL errors
    page = context.new_page()

    # Listen for console events
    page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))

    try:
        page.goto("https://localhost:5173", timeout=60000)
        page.wait_for_selector("h1:has-text('Apps Gallery')", timeout=10000)
        # Wait for the app cards to be loaded
        page.wait_for_selector(".v-card", timeout=15000)
        page.screenshot(path="jules-scratch/verification/verification.png")
    except Exception as e:
        print(f"Error during playwright script: {e}")
        # Taking a screenshot on failure to see the state
        page.screenshot(path="jules-scratch/verification/failure.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
