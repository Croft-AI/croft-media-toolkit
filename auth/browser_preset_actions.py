""""""
from playwright.sync_api import Page
from auth.browser_login_typings import TwitterDetails
from auth.browser_network_scanner import scan_networking


def twitter_login_preset_actions(page: Page, email: str, password: str) -> None:
    """twitter preset actions"""
    page.wait_for_load_state("networkidle")
    page.locator("label div").nth(3).click()
    page.get_by_label("Phone, email address, or username").fill(
        email)
    page.get_by_label("Phone, email address, or username").press("Enter")
    page.wait_for_load_state("load")
    page.get_by_role(
        "textbox", name="Password Reveal password").fill(password)

    page.get_by_test_id("LoginForm_Login_Button").click()

    page.wait_for_load_state("networkidle")

    # page.wait_for_load_state("networkidle")
