from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page(ignore_https_errors=True)

        try:
            # 1. Navigate to the app
            page.goto("https://localhost:5173/")

            # 2. Set a dummy API key to enable the analyse button
            page.evaluate("() => localStorage.setItem('geminiApiKey', 'dummy-key')")
            page.reload()

            # 3. Click the "Analyse" button
            # First, wait for the button to be potentially enabled.
            # The button becomes enabled when isApiKeySet is true.
            # We manually set it above, so we wait for the button to not be disabled.
            analyse_button = page.get_by_role("button", name="Analyse")
            expect(analyse_button).to_be_enabled(timeout=10000)
            analyse_button.click()

            # 4. Wait for the analysis to complete and the bubble to appear
            # The bubble is a button with a specific icon.
            analysis_bubble = page.get_by_role("button", name="Open analysis")
            expect(analysis_bubble).to_be_visible(timeout=30000) # Wait up to 30s for analysis

            # 5. Click the bubble to open the analysis window
            analysis_bubble.click()

            # 6. Wait for the analysis window to be visible
            analysis_window = page.locator(".analysis-window")
            expect(analysis_window).to_be_visible()

            # 7. Take a screenshot
            page.screenshot(path="jules-scratch/verification/verification.png")

            print("Screenshot captured successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
