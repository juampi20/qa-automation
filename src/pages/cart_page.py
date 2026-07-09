from .base_page import BasePage


class CartPage(BasePage):

    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_QUANTITY = ".cart_quantity"
    REMOVE_BUTTON = ".cart_button"

    def navigate(self) -> None:
        self.goto("/cart.html")

    def is_loaded(self) -> bool:
        return "/cart.html" in self.current_url

    def checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def get_item_count(self) -> int:
        return self.count(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        return self.get_texts(self.ITEM_NAME)

    def get_item_prices(self) -> list[str]:
        return self.get_texts(self.ITEM_PRICE)

    def remove_item_by_index(self, index: int = 0) -> None:
        self._locator(self.REMOVE_BUTTON).nth(index).click()

    def remove_item_by_name(self, item_name: str) -> None:
        item = self._locator(self.CART_ITEM).filter(has_text=item_name)
        item.locator(self.REMOVE_BUTTON).click()

    def is_empty(self) -> bool:
        return not self.is_visible_fast(self.CART_ITEM)
