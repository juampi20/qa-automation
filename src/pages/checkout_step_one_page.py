from .base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Página de checkout — paso 1: información del comprador."""

    FIRST_NAME_FIELD = "#first-name"
    LAST_NAME_FIELD = "#last-name"
    POSTAL_CODE_FIELD = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    CANCEL_BUTTON = "#cancel"
    ERROR_MESSAGE = ".error-message-container"

    def navigate(self) -> None:
        """Navegar al checkout paso 1."""
        self.page.goto("/checkout-step-one.html")

    def is_loaded(self) -> bool:
        """Verificar que estamos en el paso 1 de checkout."""
        return "checkout-step-one.html" in self.page.url

    def fill_details(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Completar el formulario con los datos del comprador."""
        self.fill(self.FIRST_NAME_FIELD, first_name)
        self.fill(self.LAST_NAME_FIELD, last_name)
        self.fill(self.POSTAL_CODE_FIELD, postal_code)

    def continue_checkout(self) -> None:
        """Continuar al paso 2."""
        self.click(self.CONTINUE_BUTTON)

    def cancel(self) -> None:
        """Cancelar y volver al carrito."""
        self.click(self.CANCEL_BUTTON)

    def is_error_displayed(self) -> bool:
        """Verificar si hay un mensaje de error (campos obligatorios)."""
        return self.is_visible_fast(self.ERROR_MESSAGE)

    def get_error_message(self) -> str:
        """Obtener el texto del mensaje de error."""
        return self.get_text(self.ERROR_MESSAGE)
