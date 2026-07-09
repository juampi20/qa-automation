from .base_page import BasePage


class CheckoutStepOnePage(BasePage):
    FIRST_NAME_FIELD = "#first-name"
    LAST_NAME_FIELD = "#last-name"
    POSTAL_CODE_FIELD = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    CANCEL_BUTTON = "#cancel"
    ERROR_MESSAGE = ".error-message-container"

    def navigate(self) -> None:
        self.goto("/checkout-step-one.html")

    def is_loaded(self) -> bool:
        return "checkout-step-one.html" in self.current_url

    def fill_details(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.FIRST_NAME_FIELD, first_name)
        self.fill(self.LAST_NAME_FIELD, last_name)
        self.fill(self.POSTAL_CODE_FIELD, postal_code)

    def continue_checkout(self) -> None:
        self.click(self.CONTINUE_BUTTON)

    def cancel(self) -> None:
        self.click(self.CANCEL_BUTTON)

    def is_error_displayed(self) -> bool:
        return self.is_visible_fast(self.ERROR_MESSAGE)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
