from .base_page import BasePage


class CheckoutCompletePage(BasePage):

    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_HOME_BUTTON = "#back-to-products"
    PONY_IMAGE = ".pony_express"

    def navigate(self) -> None:
        self.goto("/checkout-complete.html")

    def is_loaded(self) -> bool:
        return "checkout-complete.html" in self.current_url

    def back_home(self) -> None:
        self.click(self.BACK_HOME_BUTTON)

    def get_header_text(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        return self.get_text(self.COMPLETE_TEXT)

    def is_pony_image_visible(self) -> bool:
        return self.is_visible(self.PONY_IMAGE)
