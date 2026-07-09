import allure

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@allure.feature("Cart")
class TestCart:
    @allure.story("Agregar items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_item_to_cart(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1

    @allure.story("Agregar items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_item_to_cart_by_name(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        assert inventory_page.get_cart_item_count() == 1

    @allure.story("Agregar items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_multiple_items_to_cart(self, auth_page):
        with allure.step("Agregar dos items al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_first_item_to_cart()
            inventory_page.add_second_item_to_cart()
            assert inventory_page.get_cart_item_count() == 2

    @allure.story("Remover items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_item_from_cart_in_inventory(self, auth_page):
        with allure.step("Agregar item al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_first_item_to_cart()
            assert inventory_page.get_cart_item_count() == 1

        with allure.step("Remover item del carrito"):
            inventory_page.remove_first_item()
            assert inventory_page.get_cart_item_count() == 0

    @allure.story("Visualización")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_displays_added_items(self, auth_page):
        with allure.step("Agregar items al carrito desde inventory"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
            inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
            inventory_page.go_to_cart()

        with allure.step("Verificar items en el carrito"):
            cart_page = CartPage(auth_page)
            assert cart_page.get_item_count() == 2
            names = cart_page.get_item_names()
            assert "Sauce Labs Backpack" in names
            assert "Sauce Labs Bike Light" in names

    @allure.story("Remover items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_item_from_cart_page(self, auth_page):
        with allure.step("Agregar items al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
            inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
            inventory_page.go_to_cart()

        with allure.step("Remover un item desde la página del carrito"):
            cart_page = CartPage(auth_page)
            assert cart_page.get_item_count() == 2

            cart_page.remove_item_by_name("Sauce Labs Backpack")
            assert cart_page.get_item_count() == 1
            names = cart_page.get_item_names()
            assert "Sauce Labs Backpack" not in names
            assert "Sauce Labs Bike Light" in names

    @allure.story("Remover items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_empty_after_removing_all_items(self, auth_page):
        with allure.step("Agregar items al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_first_item_to_cart()
            inventory_page.add_second_item_to_cart()
            inventory_page.go_to_cart()

        with allure.step("Remover todos los items del carrito"):
            cart_page = CartPage(auth_page)
            cart_page.remove_item_by_index(1)
            cart_page.remove_item_by_index(0)

            assert cart_page.is_empty()

    @allure.story("Navegación")
    @allure.severity(allure.severity_level.NORMAL)
    def test_continue_shopping_from_cart(self, auth_page):
        with allure.step("Agregar item y navegar al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_first_item_to_cart()
            inventory_page.go_to_cart()

        with allure.step("Click en Continue Shopping"):
            cart_page = CartPage(auth_page)
            cart_page.continue_shopping()

            assert inventory_page.is_loaded()

    @allure.story("Agregar items")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_same_item_twice_does_not_duplicate(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1

        assert inventory_page.is_remove_button_visible(inventory_page.get_item_names()[0])
