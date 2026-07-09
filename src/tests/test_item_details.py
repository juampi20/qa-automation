import pytest
from pages.item_details_page import ItemDetailsPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestItemDetails:
    """Tests de la página de detalle de producto."""

    @pytest.fixture(autouse=True)
    def _navigate_to_details(self, auth_page):
        """Fixture interno: navega al detalle de Sauce Labs Backpack."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.click_item_by_name("Sauce Labs Backpack")
        self.page = auth_page

    def test_item_details_loaded(self, auth_page):
        """La página de detalle se carga mostrando el nombre del producto."""
        details = ItemDetailsPage(auth_page)
        assert details.is_loaded()
        assert details.get_item_name() == "Sauce Labs Backpack"

    def test_item_details_show_price(self, auth_page):
        """El detalle muestra el precio del producto."""
        details = ItemDetailsPage(auth_page)
        price = details.get_item_price()
        assert "$" in price

    def test_add_to_cart_from_details(self, auth_page):
        """Agregar al carrito desde la página de detalle."""
        details = ItemDetailsPage(auth_page)
        details.add_to_cart()
        assert details.is_remove_button_visible()

    def test_remove_from_cart_from_details(self, auth_page):
        """Remover del carrito desde la página de detalle."""
        details = ItemDetailsPage(auth_page)
        details.add_to_cart()
        assert details.is_remove_button_visible()

        details.remove_from_cart()
        assert not details.is_remove_button_visible()

    def test_back_to_products_from_details(self, auth_page):
        """Volver al inventario desde el detalle."""
        details = ItemDetailsPage(auth_page)
        details.back_to_products()

        inventory_page = InventoryPage(auth_page)
        assert inventory_page.is_loaded()

    def test_go_to_cart_from_details(self, auth_page):
        """Ir al carrito desde el detalle."""
        details = ItemDetailsPage(auth_page)
        details.add_to_cart()
        details.go_to_cart()

        cart_page = CartPage(auth_page)
        assert cart_page.is_loaded()
        assert cart_page.get_item_count() == 1
