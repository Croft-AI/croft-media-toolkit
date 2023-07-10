"""type casting for browser login script"""
from typing import TypedDict, Callable, NotRequired, List
from playwright.sync_api import Page


class UserCredentials(TypedDict):
    """user credentials"""
    name: str
    email: str
    password: str
    preset_action: NotRequired[Callable[[Page, str, str], None]]
    collect_headers: List[str]


class TwitterDetails(UserCredentials):
    """twitter login input selector details"""
    email_input_selector: str
    password_input_selector: str
