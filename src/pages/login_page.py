from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME_FIELD = "#user-name"
    PASSWORD_FIELD = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message-container"

    def navigate(self) -> None:
        self.goto("https://www.saucedemo.com")

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_FIELD, username)
        self.fill(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)

    def is_error_message_displayed(self) -> bool:
        return self.is_visible_fast(self.ERROR_MESSAGE)
