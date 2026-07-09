import pytest, time
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestLogin:
    
    def test_login_valid(self, page):
        login_page, inventory_page = LoginPage(page), InventoryPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        assert inventory_page.is_loaded() == True, "Inicio de sesion fallido"

    def test_login_invalid_credentials(self, page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce123")
        assert login_page.is_error_message_displayed() == True, "Mensaje de error no mostrado"

    def test_login_empty_fields(self, page):
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("", "")
        assert login_page.is_error_message_displayed() == True, "Mensaje de error no mostrado"