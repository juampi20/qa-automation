from .base_page import BasePage


class ItemDetailsPage(BasePage):
    """Página de detalles de un producto."""

    ADD_TO_CART_BUTTON = "#add-to-cart"
    REMOVE_BUTTON = "#remove"
    BACK_TO_PRODUCTS_BUTTON = "#back-to-products"
    CART_LINK = ".shopping_cart_link"
    ITEM_NAME = ".inventory_details_name"
    ITEM_DESC = ".inventory_details_desc"
    ITEM_PRICE = ".inventory_details_price"

    def is_loaded(self) -> bool:
        """Verificar que la página de detalles se haya cargado."""
        return "inventory-item.html" in self.page.url

    def add_to_cart(self) -> None:
        """Agregar el producto al carrito."""
        self.click(self.ADD_TO_CART_BUTTON)

    def remove_from_cart(self) -> None:
        """Remover el producto del carrito."""
        self.click(self.REMOVE_BUTTON)

    def back_to_products(self) -> None:
        """Volver a la página de inventario."""
        self.click(self.BACK_TO_PRODUCTS_BUTTON)

    def go_to_cart(self) -> None:
        """Ir al carrito."""
        self.click(self.CART_LINK)

    def get_item_name(self) -> str:
        """Obtener el nombre del producto."""
        return self.get_text(self.ITEM_NAME)

    def get_item_price(self) -> str:
        """Obtener el precio del producto."""
        return self.get_text(self.ITEM_PRICE)

    def is_remove_button_visible(self) -> bool:
        """Verificar si el botón Remove está visible (producto ya en carrito)."""
        return self.is_visible_fast(self.REMOVE_BUTTON)
