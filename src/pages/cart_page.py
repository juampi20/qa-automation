from .base_page import BasePage


class CartPage(BasePage):
    """Página del carrito de compras."""

    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_QUANTITY = ".cart_quantity"
    REMOVE_BUTTON = ".cart_button"

    def navigate(self) -> None:
        """Navegar a la página del carrito."""
        self.page.goto("/cart.html")

    def is_loaded(self) -> bool:
        """Verificar que la página del carrito se haya cargado."""
        return "/cart.html" in self.page.url

    def checkout(self) -> None:
        """Proceder al checkout."""
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """Volver al inventario."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def get_item_count(self) -> int:
        """Cantidad de productos distintos en el carrito."""
        return self.count(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        """Nombres de los productos en el carrito."""
        return self.get_texts(self.ITEM_NAME)

    def get_item_prices(self) -> list[str]:
        """Precios de los productos en el carrito."""
        return self.get_texts(self.ITEM_PRICE)

    def remove_item_by_index(self, index: int = 0) -> None:
        """Remover un producto del carrito por su índice (0-based)."""
        self._locator(self.REMOVE_BUTTON).nth(index).click()

    def remove_item_by_name(self, item_name: str) -> None:
        """Remover un producto del carrito por su nombre."""
        item = self._locator(self.CART_ITEM).filter(has_text=item_name)
        item.locator(self.REMOVE_BUTTON).click()

    def is_empty(self) -> bool:
        """Verificar si el carrito está vacío."""
        return not self.is_visible_fast(self.CART_ITEM)
