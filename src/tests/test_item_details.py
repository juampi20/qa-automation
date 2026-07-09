import allure
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.item_details_page import ItemDetailsPage


@pytest.fixture(autouse=True)
def navigate_to_details(auth_page):
    InventoryPage(auth_page).click_item_by_name("Sauce Labs Backpack")


@allure.feature("Item Details")
class TestItemDetails:
    @allure.story("Visualización")
    @allure.severity(allure.severity_level.NORMAL)
    def test_item_details_loaded(self, auth_page):
        details = ItemDetailsPage(auth_page)
        assert details.is_loaded()
        assert details.get_item_name() == "Sauce Labs Backpack"

    @allure.story("Visualización")
    @allure.severity(allure.severity_level.NORMAL)
    def test_item_details_show_price(self, auth_page):
        details = ItemDetailsPage(auth_page)
        assert "$" in details.get_item_price()

    @allure.story("Gestión del carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_to_cart_from_details(self, auth_page):
        with allure.step("Agregar item al carrito desde detalles"):
            details = ItemDetailsPage(auth_page)
            details.add_to_cart()
            assert details.is_remove_button_visible()

    @allure.story("Gestión del carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_from_cart_from_details(self, auth_page):
        with allure.step("Agregar item al carrito"):
            details = ItemDetailsPage(auth_page)
            details.add_to_cart()
            assert details.is_remove_button_visible()

        with allure.step("Remover item del carrito"):
            details.remove_from_cart()
            assert not details.is_remove_button_visible()

    @allure.story("Navegación")
    @allure.severity(allure.severity_level.NORMAL)
    def test_back_to_products_from_details(self, auth_page):
        with allure.step("Volver a productos desde detalles"):
            ItemDetailsPage(auth_page).back_to_products()

        with allure.step("Verificar retorno al inventory"):
            assert InventoryPage(auth_page).is_loaded()

    @allure.story("Navegación")
    @allure.severity(allure.severity_level.NORMAL)
    def test_go_to_cart_from_details(self, auth_page):
        with allure.step("Agregar item desde detalles"):
            details = ItemDetailsPage(auth_page)
            details.add_to_cart()

        with allure.step("Navegar al carrito"):
            details.go_to_cart()

        with allure.step("Verificar item en el carrito"):
            cart_page = CartPage(auth_page)
            assert cart_page.is_loaded()
            assert cart_page.get_item_count() == 1
