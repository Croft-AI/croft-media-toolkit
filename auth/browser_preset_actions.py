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


def reddit_login_preset_actions(page: Page, email: str, password: str) -> None:
    """reddit preset action"""
    page.get_by_placeholder("\n        Username\n      ").click()
    page.get_by_placeholder("\n        Username\n      ").fill(email)
    page.get_by_placeholder("\n        Username\n      ").press("Tab")
    page.get_by_placeholder("\n        Password\n      ").press("CapsLock")
    page.get_by_placeholder("\n        Password\n      ").fill(password)
    page.get_by_placeholder("\n        Password\n      ").press("Enter")
    # page.goto("https://www.reddit.com/")
    page.wait_for_load_state("networkidle")


def tiktok_preset_action(page: Page, email: str, password: str) -> None:
    """opens tiktok in home page to get cookie"""
    page.wait_for_load_state("networkidle")
    return None
