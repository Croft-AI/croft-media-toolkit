"""type casting for browser login script"""
from playwright.sync_api import Page
from typing import TypedDict, Callable, NotRequired


class UserCredentials(TypedDict):
    """user credentials"""
    email: str
    password: str
    preset_action: NotRequired[Callable[[Page, str, str], None]]


class TwitterDetails(UserCredentials):
    """twitter login input selector details"""
    email_input_selector: str
    password_input_selector: str
