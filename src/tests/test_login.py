import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


class TestLogin:
    @pytest.mark.parametrize(
        ("username", "password", "expect_success", "case_id"),
        [
            pytest.param("standard_user", "secret_sauce", True, "valid", id="valid"),
            pytest.param(
                "standard_user", "wrong", False, "invalid_credentials", id="invalid_credentials"
            ),
            pytest.param("", "", False, "empty_fields", id="empty_fields"),
            pytest.param(
                "locked_out_user", "secret_sauce", False, "locked_out_user", id="locked_out_user"
            ),
        ],
    )
    def test_login(self, page, username, password, expect_success, case_id):
        login_page, inventory_page = LoginPage(page), InventoryPage(page)
        login_page.navigate()
        login_page.login(username, password)
        if expect_success:
            assert inventory_page.is_loaded()
        else:
            assert login_page.is_error_message_displayed()
