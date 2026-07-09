from .base_page import BasePage


class CheckoutCompletePage(BasePage):
    """Página de checkout — confirmación de compra exitosa."""

    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_HOME_BUTTON = "#back-to-products"
    PONY_IMAGE = ".pony_express"

    def navigate(self) -> None:
        """Navegar a la página de confirmación."""
        self.page.goto("/checkout-complete.html")

    def is_loaded(self) -> bool:
        """Verificar que estamos en la página de confirmación."""
        return "checkout-complete.html" in self.page.url

    def back_home(self) -> None:
        """Volver al inventario."""
        self.click(self.BACK_HOME_BUTTON)

    def get_header_text(self) -> str:
        """Obtener el mensaje de confirmación principal."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_complete_text(self) -> str:
        """Obtener el texto descriptivo de la confirmación."""
        return self.get_text(self.COMPLETE_TEXT)

    def is_pony_image_visible(self) -> bool:
        """Verificar si la imagen del pony (checkmark) está visible."""
        return self.is_visible(self.PONY_IMAGE)
