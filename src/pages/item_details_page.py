from .base_page import BasePage


class ItemDetailsPage(BasePage):

    ADD_TO_CART_BUTTON = "#add-to-cart"
    REMOVE_BUTTON = "#remove"
    BACK_TO_PRODUCTS_BUTTON = "#back-to-products"
    CART_LINK = ".shopping_cart_link"
    ITEM_NAME = ".inventory_details_name"
    ITEM_DESC = ".inventory_details_desc"
    ITEM_PRICE = ".inventory_details_price"

    def is_loaded(self) -> bool:
        return "inventory-item.html" in self.current_url

    def add_to_cart(self) -> None:
        self.click(self.ADD_TO_CART_BUTTON)

    def remove_from_cart(self) -> None:
        self.click(self.REMOVE_BUTTON)

    def back_to_products(self) -> None:
        self.click(self.BACK_TO_PRODUCTS_BUTTON)

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    def get_item_name(self) -> str:
        return self.get_text(self.ITEM_NAME)

    def get_item_price(self) -> str:
        return self.get_text(self.ITEM_PRICE)

    def is_remove_button_visible(self) -> bool:
        return self.is_visible_fast(self.REMOVE_BUTTON)
