import pytest, time
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestInventory:
    
    def test_add_one_item_to_cart(self, driver):
        login_page, inventory_page = LoginPage(driver), InventoryPage(driver)

        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")

        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1, "El item no se agregó al carrito"

    def test_add_second_item_to_cart(self, driver):
        login_page, inventory_page = LoginPage(driver), InventoryPage(driver)
    
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")

        inventory_page.add_second_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1, "El item no se agregó al carrito"