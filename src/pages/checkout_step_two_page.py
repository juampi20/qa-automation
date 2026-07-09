from .base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    """Página de checkout — paso 2: resumen de la orden."""

    FINISH_BUTTON = "#finish"
    CANCEL_BUTTON = "#cancel"
    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_QUANTITY = ".cart_quantity"
    SUMMARY_SUBTOTAL = ".summary_subtotal_label"
    SUMMARY_TAX = ".summary_tax_label"
    SUMMARY_TOTAL = ".summary_total_label"
    PAYMENT_INFO = ".summary_value_label"
    SHIPPING_INFO = ".summary_value_label"

    def navigate(self) -> None:
        """Navegar al checkout paso 2."""
        self.page.goto("/checkout-step-two.html")

    def is_loaded(self) -> bool:
        """Verificar que estamos en el paso 2 de checkout."""
        return "checkout-step-two.html" in self.page.url

    def finish(self) -> None:
        """Finalizar la compra."""
        self.click(self.FINISH_BUTTON)

    def cancel(self) -> None:
        """Cancelar y volver al inventario."""
        self.click(self.CANCEL_BUTTON)

    def get_item_count(self) -> int:
        """Cantidad de productos en el resumen."""
        return self.count(self.CART_ITEM)

    def get_item_names(self) -> list[str]:
        """Nombres de los productos en el resumen."""
        return self.get_texts(self.ITEM_NAME)

    def get_item_prices(self) -> list[str]:
        """Precios de los productos en el resumen."""
        return self.get_texts(self.ITEM_PRICE)

    def get_subtotal(self) -> str:
        """Obtener el subtotal del resumen."""
        return self.get_text(self.SUMMARY_SUBTOTAL)

    def get_tax(self) -> str:
        """Obtener el impuesto del resumen."""
        return self.get_text(self.SUMMARY_TAX)

    def get_total(self) -> str:
        """Obtener el total del resumen."""
        return self.get_text(self.SUMMARY_TOTAL)
