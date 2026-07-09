import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.checkout_complete_page import CheckoutCompletePage


class TestCheckout:
    """Tests del flujo completo de checkout."""

    @pytest.fixture(autouse=True)
    def setup_cart(self, auth_page):
        """Fixture interno: agrega items al carrito antes de cada test."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        inventory_page.go_to_cart()
        self.page = auth_page

    # ── Step 1: Información del comprador ──────────────────

    def test_checkout_step_one_continue_with_valid_data(self, auth_page):
        """Completar formulario con datos válidos y continuar."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        assert step_one.is_loaded()

        step_one.fill_details("Jane", "Doe", "1000")
        step_one.continue_checkout()

        step_two = CheckoutStepTwoPage(auth_page)
        assert step_two.is_loaded()

    def test_checkout_step_one_empty_first_name(self, auth_page):
        """Error al dejar el nombre vacío."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("", "Doe", "1000")
        step_one.continue_checkout()

        assert step_one.is_error_displayed()
        assert "First Name" in step_one.get_error_message()

    def test_checkout_step_one_empty_last_name(self, auth_page):
        """Error al dejar el apellido vacío."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("Jane", "", "1000")
        step_one.continue_checkout()

        assert step_one.is_error_displayed()
        assert "Last Name" in step_one.get_error_message()

    def test_checkout_step_one_empty_postal_code(self, auth_page):
        """Error al dejar el código postal vacío."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("Jane", "Doe", "")
        step_one.continue_checkout()

        assert step_one.is_error_displayed()

    def test_checkout_step_one_all_empty_fields(self, auth_page):
        """Error al dejar todos los campos vacíos."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.continue_checkout()

        assert step_one.is_error_displayed()

    def test_checkout_step_one_cancel_returns_to_cart(self, auth_page):
        """Cancelar en step 1 vuelve al carrito."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.cancel()

        assert cart_page.is_loaded()

    # ── Step 2: Resumen ────────────────────────────────────

    def test_checkout_step_two_item_summary(self, auth_page):
        """El resumen muestra los items agregados."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("Jane", "Doe", "1000")
        step_one.continue_checkout()

        step_two = CheckoutStepTwoPage(auth_page)
        assert step_two.get_item_count() == 2
        names = step_two.get_item_names()
        assert "Sauce Labs Backpack" in names
        assert "Sauce Labs Bike Light" in names

    def test_checkout_step_two_cancel_returns_to_inventory(self, auth_page):
        """Cancelar en step 2 vuelve al inventario."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("Jane", "Doe", "1000")
        step_one.continue_checkout()

        step_two = CheckoutStepTwoPage(auth_page)
        step_two.cancel()

        # Cancel en step 2 redirige a inventory
        inventory_page = InventoryPage(auth_page)
        assert inventory_page.is_loaded()

    def test_checkout_step_two_total_breakdown(self, auth_page):
        """El resumen muestra subtotal, tax y total."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("Jane", "Doe", "1000")
        step_one.continue_checkout()

        step_two = CheckoutStepTwoPage(auth_page)
        assert "Total" in step_two.get_total()
        assert "Item total" in step_two.get_subtotal()
        assert "Tax" in step_two.get_tax()

    # ── Flujo completo (happy path) ────────────────────────

    def test_complete_checkout_flow(self, auth_page):
        """Flujo completo: carrito → checkout → confirmación."""
        # Step 1
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("Jane", "Doe", "1000")
        step_one.continue_checkout()

        # Step 2
        step_two = CheckoutStepTwoPage(auth_page)
        step_two.finish()

        # Confirmación
        complete = CheckoutCompletePage(auth_page)
        assert complete.is_loaded()
        assert "Thank you" in complete.get_header_text()
        assert complete.get_complete_text() != ""

    def test_back_home_after_checkout(self, auth_page):
        """'Back Home' en la confirmación vuelve al inventario."""
        cart_page = CartPage(auth_page)
        cart_page.checkout()

        step_one = CheckoutStepOnePage(auth_page)
        step_one.fill_details("Jane", "Doe", "1000")
        step_one.continue_checkout()

        step_two = CheckoutStepTwoPage(auth_page)
        step_two.finish()

        complete = CheckoutCompletePage(auth_page)
        complete.back_home()

        inventory_page = InventoryPage(auth_page)
        assert inventory_page.is_loaded()
