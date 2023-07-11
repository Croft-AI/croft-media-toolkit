"""opens browser instance in playwright to log in and access auth keys, cookies"""
from playwright.sync_api import sync_playwright
from auth.browser_login_typings import TwitterDetails
from auth.browser_network_scanner import scan_networking


def access_login_page(url: str, site_details: TwitterDetails) -> object:
    """opens up headless browser to url login"""
    with sync_playwright() as playwright:
        # opens up browser to page
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        scan_networking(page, site_details)
        page.goto(url)
        # logs into account
        if "preset_action" in site_details:
            site_details["preset_action"](
                page, site_details["email"], site_details["password"])
        else:
            page.locator(site_details["email_input_selector"]).fill(
                site_details["email"])
            page.locator(site_details["password_input_selector"]).fill(
                site_details["password"])
            page.press("body", "Enter")

        context.close()
        browser.close()


if __name__ == "__main__":
    pass
