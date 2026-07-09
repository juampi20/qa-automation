import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCart:
    """Tests del carrito de compras."""

    def test_add_one_item_to_cart(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1

    def test_add_item_to_cart_by_name(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        assert inventory_page.get_cart_item_count() == 1

    def test_add_multiple_items_to_cart(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.add_second_item_to_cart()
        assert inventory_page.get_cart_item_count() == 2

    def test_remove_item_from_cart_in_inventory(self, auth_page):
        """Agregar y remover un item desde la página de inventario."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1

        inventory_page.remove_first_item_from_cart()
        assert inventory_page.get_cart_item_count() == 0

    def test_cart_displays_added_items(self, auth_page):
        """Verificar que los items agregados aparecen en el carrito."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        inventory_page.go_to_cart()

        cart_page = CartPage(auth_page)
        assert cart_page.get_item_count() == 2
        names = cart_page.get_item_names()
        assert "Sauce Labs Backpack" in names
        assert "Sauce Labs Bike Light" in names

    def test_remove_item_from_cart_page(self, auth_page):
        """Agregar items y remover uno desde la página del carrito."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        inventory_page.go_to_cart()

        cart_page = CartPage(auth_page)
        assert cart_page.get_item_count() == 2

        cart_page.remove_item_by_name("Sauce Labs Backpack")
        assert cart_page.get_item_count() == 1
        names = cart_page.get_item_names()
        assert "Sauce Labs Backpack" not in names
        assert "Sauce Labs Bike Light" in names

    def test_cart_empty_after_removing_all_items(self, auth_page):
        """Verificar que el carrito queda vacío al remover todos los items."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.add_second_item_to_cart()
        inventory_page.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.remove_item_by_index(1)
        cart_page.remove_item_by_index(0)

        assert cart_page.is_empty()

    def test_continue_shopping_from_cart(self, auth_page):
        """El botón 'Continue Shopping' vuelve al inventario."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.go_to_cart()

        cart_page = CartPage(auth_page)
        cart_page.continue_shopping()

        assert inventory_page.is_loaded()

    def test_add_same_item_twice_does_not_duplicate(self, auth_page):
        """Agregar el mismo item dos veces no debería duplicar el contador."""
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1

        # El botón cambia a REMOVE, no debería poder agregar de nuevo
        assert inventory_page.is_remove_button_visible(
            inventory_page.get_item_names()[0]
        )
