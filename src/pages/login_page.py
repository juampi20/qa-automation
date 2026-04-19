# https://www.saucedemo.com
from .base_page import BasePage

class LoginPage(BasePage):
    USERNAME_FIELD  = "#user-name"
    PASSWORD_FIELD = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message-container"

    def navigate(self):
        self.page.goto("https://www.saucedemo.com")

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME_FIELD, username)
        self.page.fill(self.PASSWORD_FIELD, password)
        self.page.click(self.LOGIN_BUTTON)

    def is_error_message_displayed(self):
        return self.page.locator(self.ERROR_MESSAGE).is_visible()
    