"""opens browser instance in playwright to log in and access auth keys, cookies"""
from auth.browser_login_typings import TwitterDetails
from playwright.sync_api import sync_playwright


def access_login_page(url: str, site_details: TwitterDetails) -> object:
    """opens up headless browser to url login"""
    with sync_playwright() as playwright:
        # opens up browser to page
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()
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


if __name__ == "__main__":
    pass
