from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestSidebar:

    LINKS = {"All Items", "About", "Logout", "Reset App State"}

    def test_sidebar_closed_by_default(self, auth_page):
        assert not InventoryPage(auth_page).is_menu_open()

    def test_sidebar_opens_and_closes(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.open_menu()
        assert inventory_page.is_menu_open()

        inventory_page.close_menu()
        assert not inventory_page.is_menu_open()

    def test_sidebar_contains_expected_links(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.open_menu()

        links = set(inventory_page.get_sidebar_links())
        assert links == self.LINKS

    def test_sidebar_all_items_navigates_to_inventory(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.go_to_cart()

        cart_page = CartPage(auth_page)
        assert cart_page.is_loaded()

        cart_page.open_menu()
        cart_page.click_sidebar_all_items()

        assert inventory_page.is_loaded()

    def test_sidebar_about_navigates_to_saucelabs(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.open_menu()
        inventory_page.click_sidebar_about()

        inventory_page.page.wait_for_url("**/saucelabs.com/**", timeout=15000)
        assert "saucelabs" in inventory_page.page.url

    def test_sidebar_logout_returns_to_login(self, auth_page):
        InventoryPage(auth_page).open_menu()
        InventoryPage(auth_page).click_sidebar_logout()

        auth_page.wait_for_url("https://www.saucedemo.com/", timeout=5000)
        assert auth_page.url.rstrip("/") == "https://www.saucedemo.com"
        assert auth_page.locator("#user-name").is_visible()

    def test_sidebar_reset_app_state_clears_cart(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.add_second_item_to_cart()
        assert inventory_page.get_cart_item_count() == 2

        inventory_page.open_menu()
        inventory_page.click_sidebar_reset()
        inventory_page.close_menu()

        assert inventory_page.get_cart_item_count() == 0
