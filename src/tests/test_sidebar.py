import allure
import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@allure.feature("Sidebar")
class TestSidebar:
    LINKS = frozenset(["All Items", "About", "Logout", "Reset App State"])

    @allure.story("Apertura y cierre")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sidebar_closed_by_default(self, auth_page):
        assert not InventoryPage(auth_page).is_menu_open()

    @allure.story("Apertura y cierre")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sidebar_opens_and_closes(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.open_menu()
        assert inventory_page.is_menu_open()

        inventory_page.close_menu()
        assert not inventory_page.is_menu_open()

    @allure.story("Enlaces")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sidebar_contains_expected_links(self, auth_page):
        with allure.step("Abrir menú lateral"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.open_menu()

        with allure.step("Verificar links del sidebar"):
            links = set(inventory_page.get_sidebar_links())
            assert links == self.LINKS

    @allure.story("Enlaces")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sidebar_all_items_navigates_to_inventory(self, auth_page):
        with allure.step("Agregar item e ir al carrito"):
            inventory_page = InventoryPage(auth_page)
            inventory_page.add_first_item_to_cart()
            inventory_page.go_to_cart()

        with allure.step("Verificar que estamos en el carrito"):
            cart_page = CartPage(auth_page)
            assert cart_page.is_loaded()

        with allure.step("Abrir sidebar y click en All Items"):
            cart_page.open_menu()
            cart_page.click_sidebar_all_items()

        with allure.step("Verificar retorno al inventory"):
            assert inventory_page.is_loaded()

    @allure.story("Navegación")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("{link_type}")
    @pytest.mark.parametrize(
        "link_type",
        [
            pytest.param("about", id="about"),
            pytest.param("logout", id="logout"),
            pytest.param("reset", id="reset_app_state"),
        ],
    )
    def test_sidebar_link_navigation(self, auth_page, link_type):
        inventory_page = InventoryPage(auth_page)

        if link_type == "about":
            with allure.step("Click en About — navegar a saucelabs"):
                inventory_page.open_menu()
                inventory_page.click_sidebar_about()
                inventory_page.page.wait_for_url("**/saucelabs.com/**", timeout=15000)
                assert "saucelabs" in inventory_page.page.url

        elif link_type == "logout":
            with allure.step("Click en Logout"):
                inventory_page.open_menu()
                inventory_page.click_sidebar_logout()
                auth_page.wait_for_url("https://www.saucedemo.com/", timeout=5000)
                assert auth_page.url.rstrip("/") == "https://www.saucedemo.com"
                assert auth_page.locator("#user-name").is_visible()

        elif link_type == "reset":
            with allure.step("Agregar items al carrito"):
                inventory_page.add_first_item_to_cart()
                inventory_page.add_second_item_to_cart()
                assert inventory_page.get_cart_item_count() == 2

            with allure.step("Reset App State desde sidebar"):
                inventory_page.open_menu()
                inventory_page.click_sidebar_reset()
                inventory_page.close_menu()
                assert inventory_page.get_cart_item_count() == 0
