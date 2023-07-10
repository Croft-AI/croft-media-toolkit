"""runs toolkit"""
from auth.browser_login import access_login_page
from details.login_configs import twitter_details

if __name__ == "__main__":
    access_login_page("https://twitter.com/i/flow/login", twitter_details)
