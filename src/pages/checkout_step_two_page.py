from .base_page import BasePage


class CheckoutStepTwoPage(BasePage):

    FINISH_BUTTON = "#finish"
    CANCEL_BUTTON = "#cancel"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_QUANTITY = ".cart_quantity"
    SUMMARY_SUBTOTAL = ".summary_subtotal_label"
    SUMMARY_TAX = ".summary_tax_label"
    SUMMARY_TOTAL = ".summary_total_label"

    def navigate(self) -> None:
        self.goto("/checkout-step-two.html")

    def is_loaded(self) -> bool:
        return "checkout-step-two.html" in self.current_url

    def finish(self) -> None:
        self.click(self.FINISH_BUTTON)

    def cancel(self) -> None:
        self.click(self.CANCEL_BUTTON)

    def get_item_count(self) -> int:
        return self.count(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        return self.get_texts(self.ITEM_NAME)

    def get_item_prices(self) -> list[str]:
        return self.get_texts(self.ITEM_PRICE)

    def get_subtotal(self) -> str:
        return self.get_text(self.SUMMARY_SUBTOTAL)

    def get_tax(self) -> str:
        return self.get_text(self.SUMMARY_TAX)

    def get_total(self) -> str:
        return self.get_text(self.SUMMARY_TOTAL)
