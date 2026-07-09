from .base_page import BasePage


class InventoryPage(BasePage):
    CART_LINK = ".shopping_cart_link"
    CART_COUNTER = ".shopping_cart_badge"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ADD_BUTTON = ".btn_inventory"
    SORT_DROPDOWN = ".product_sort_container"

    FIRST_ITEM_ADD_BUTTON = ".inventory_item:nth-child(1) .btn_inventory"
    SECOND_ITEM_ADD_BUTTON = ".inventory_item:nth-child(2) .btn_inventory"

    def navigate(self) -> None:
        self.goto("/inventory.html")

    def is_loaded(self) -> bool:
        return "/inventory.html" in self.current_url

    # ── Carrito ─────────────────────────────────────────────

    def get_cart_item_count(self) -> int:
        if self.is_visible_fast(self.CART_COUNTER):
            return int(self.get_text(self.CART_COUNTER))
        return 0

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    # ── Agregar items ───────────────────────────────────────

    def add_first_item_to_cart(self) -> None:
        self.click(self.FIRST_ITEM_ADD_BUTTON)

    def add_second_item_to_cart(self) -> None:
        self.click(self.SECOND_ITEM_ADD_BUTTON)

    def add_item_to_cart_by_name(self, item_name: str) -> None:
        item = self._locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        item.locator(self.ADD_BUTTON).click()

    # ── Remover items ───────────────────────────────────────

    def remove_first_item(self) -> None:
        self.click(self.FIRST_ITEM_ADD_BUTTON)

    def remove_second_item(self) -> None:
        self.click(self.SECOND_ITEM_ADD_BUTTON)

    def remove_item_by_name(self, item_name: str) -> None:
        item = self._locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        item.locator(self.ADD_BUTTON).click()

    def is_remove_button_visible(self, item_name: str) -> bool:
        item = self._locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        return item.locator(self.ADD_BUTTON).is_visible(timeout=500)

    # ── Leer datos ──────────────────────────────────────────

    def get_item_names(self) -> list[str]:
        return self.get_texts(self.ITEM_NAME)

    def get_item_count(self) -> int:
        return self.count(self.INVENTORY_ITEM)

    def click_item_by_name(self, item_name: str) -> None:
        self._locator(self.ITEM_NAME).filter(has_text=item_name).click()

    # ── Ordenamiento ────────────────────────────────────────

    def sort_by(self, value: str) -> None:
        self.select_option(self.SORT_DROPDOWN, value)
