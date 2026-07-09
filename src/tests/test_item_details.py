import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.item_details_page import ItemDetailsPage


@pytest.fixture(autouse=True)
def navigate_to_details(auth_page):
    InventoryPage(auth_page).click_item_by_name("Sauce Labs Backpack")


class TestItemDetails:
    def test_item_details_loaded(self, auth_page):
        details = ItemDetailsPage(auth_page)
        assert details.is_loaded()
        assert details.get_item_name() == "Sauce Labs Backpack"

    def test_item_details_show_price(self, auth_page):
        details = ItemDetailsPage(auth_page)
        assert "$" in details.get_item_price()

    def test_add_to_cart_from_details(self, auth_page):
        details = ItemDetailsPage(auth_page)
        details.add_to_cart()
        assert details.is_remove_button_visible()

    def test_remove_from_cart_from_details(self, auth_page):
        details = ItemDetailsPage(auth_page)
        details.add_to_cart()
        assert details.is_remove_button_visible()

        details.remove_from_cart()
        assert not details.is_remove_button_visible()

    def test_back_to_products_from_details(self, auth_page):
        ItemDetailsPage(auth_page).back_to_products()

        assert InventoryPage(auth_page).is_loaded()

    def test_go_to_cart_from_details(self, auth_page):
        details = ItemDetailsPage(auth_page)
        details.add_to_cart()
        details.go_to_cart()

        cart_page = CartPage(auth_page)
        assert cart_page.is_loaded()
        assert cart_page.get_item_count() == 1
