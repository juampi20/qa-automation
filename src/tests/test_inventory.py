import allure
import pytest

from pages.inventory_page import InventoryPage
from pages.item_details_page import ItemDetailsPage


@allure.feature("Inventory")
class TestInventory:
    @allure.story("Carga y visualización")
    @allure.severity(allure.severity_level.NORMAL)
    def test_inventory_is_loaded(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        assert inventory_page.is_loaded()

    @allure.story("Carga y visualización")
    @allure.severity(allure.severity_level.NORMAL)
    def test_inventory_shows_items(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        assert inventory_page.get_item_count() > 0

    @allure.story("Gestión del carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_item_from_inventory(self, auth_page):
        with allure.step("Agregar primer item al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_first_item_to_cart()
            assert inventory_page.get_cart_item_count() == 1

        with allure.step("Remover el item del carrito"):
            inventory_page.remove_first_item()
            assert inventory_page.get_cart_item_count() == 0

    @allure.story("Gestión del carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_and_remove_multiple_from_inventory(self, auth_page):
        with allure.step("Agregar dos items al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_first_item_to_cart()
            inventory_page.add_second_item_to_cart()
            assert inventory_page.get_cart_item_count() == 2

        with allure.step("Remover el primer item"):
            inventory_page.remove_first_item()
            assert inventory_page.get_cart_item_count() == 1

        with allure.step("Remover el segundo item"):
            inventory_page.remove_second_item()
            assert inventory_page.get_cart_item_count() == 0

    @allure.story("Ordenamiento")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("{sort_value}")
    @pytest.mark.parametrize(
        ("sort_value", "assert_type"),
        [
            pytest.param("za", "name", id="name_z_to_a"),
            pytest.param("lohi", "price", id="price_low_to_high"),
            pytest.param("hilo", "price", id="price_high_to_low"),
        ],
    )
    def test_sort_inventory(self, auth_page, sort_value, assert_type):
        inventory_page = InventoryPage(auth_page)
        if assert_type == "name":
            names_before = inventory_page.get_item_names()
            inventory_page.sort_by(sort_value)
            names_after = inventory_page.get_item_names()
            is_reverse = sort_value == "za"
            assert names_after == sorted(names_before, reverse=is_reverse)
        else:
            inventory_page.sort_by(sort_value)
            prices = inventory_page.get_texts(inventory_page.ITEM_PRICE)
            numeric_prices = [float(p.replace("$", "")) for p in prices]
            is_hilo = sort_value == "hilo"
            assert numeric_prices == sorted(numeric_prices, reverse=is_hilo)

    @allure.story("Navegación a detalles")
    @allure.severity(allure.severity_level.NORMAL)
    def test_click_item_navigates_to_details(self, auth_page):
        with allure.step("Click en Sauce Labs Backpack"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.click_item_by_name("Sauce Labs Backpack")

        with allure.step("Verificar que estamos en la página de detalles"):
            details = ItemDetailsPage(auth_page)
            assert details.is_loaded()
            assert details.get_item_name() == "Sauce Labs Backpack"

    @allure.story("Gestión del carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_badge_updates_after_add_and_remove(self, auth_page):
        with allure.step("Verificar que el carrito está vacío"):
            inventory_page = InventoryPage(auth_page)
            assert inventory_page.get_cart_item_count() == 0

        with allure.step("Agregar item al carrito"):
            inventory_page.add_first_item_to_cart()
            assert inventory_page.get_cart_item_count() == 1

        with allure.step("Remover item del carrito"):
            inventory_page.remove_first_item()
            assert inventory_page.get_cart_item_count() == 0
