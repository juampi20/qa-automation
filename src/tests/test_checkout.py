import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage


@pytest.fixture(autouse=True)
def setup_cart(auth_page):
    inventory_page = InventoryPage(auth_page)
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
    inventory_page.go_to_cart()


@allure.feature("Checkout")
class TestCheckout:
    # ── Paso 1: Información del comprador ──────────────────

    @allure.story("Formulario de datos")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("{case_id}")
    @pytest.mark.parametrize(
        ("first_name", "last_name", "postal_code", "expect_error", "case_id"),
        [
            pytest.param("Jane", "Doe", "1000", False, "valid_data", id="valid_data"),
            pytest.param("", "Doe", "1000", True, "empty_first_name", id="empty_first_name"),
            pytest.param("Jane", "", "1000", True, "empty_last_name", id="empty_last_name"),
            pytest.param("Jane", "Doe", "", True, "empty_postal_code", id="empty_postal_code"),
            pytest.param(None, None, None, True, "all_empty", id="all_empty"),
        ],
    )
    def test_step_one_form_validation(
        self, auth_page, first_name, last_name, postal_code, expect_error, case_id
    ):
        with allure.step("Ir al checkout"):
            CartPage(auth_page).checkout()

        with allure.step(f"Completar formulario: {first_name} / {last_name} / {postal_code}"):
            step_one = CheckoutStepOnePage(auth_page)
            if first_name is not None:
                step_one.fill_details(first_name, last_name, postal_code)

            step_one.continue_checkout()

        with allure.step("Verificar resultado del formulario"):
            if expect_error:
                assert step_one.is_error_displayed()
            else:
                step_two = CheckoutStepTwoPage(auth_page)
                assert step_two.is_loaded()

    @allure.story("Cancelación")
    @allure.severity(allure.severity_level.NORMAL)
    def test_step_one_cancel_returns_to_cart(self, auth_page):
        with allure.step("Ir al checkout"):
            CartPage(auth_page).checkout()

        with allure.step("Cancelar en paso 1"):
            step_one = CheckoutStepOnePage(auth_page)
            step_one.cancel()

        with allure.step("Verificar retorno al carrito"):
            assert CartPage(auth_page).is_loaded()

    # ── Paso 2: Resumen ────────────────────────────────────

    @allure.story("Resumen")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_step_two_item_summary(self, auth_page):
        with allure.step("Completar paso 1 y continuar"):
            CartPage(auth_page).checkout()
            step_one = CheckoutStepOnePage(auth_page)
            step_one.fill_details("Jane", "Doe", "1000")
            step_one.continue_checkout()

        with allure.step("Verificar resumen de items"):
            step_two = CheckoutStepTwoPage(auth_page)
            assert step_two.get_item_count() == 2
            names = step_two.get_item_names()
            assert "Sauce Labs Backpack" in names
            assert "Sauce Labs Bike Light" in names

    @allure.story("Cancelación")
    @allure.severity(allure.severity_level.NORMAL)
    def test_step_two_cancel_returns_to_inventory(self, auth_page):
        with allure.step("Completar paso 1"):
            CartPage(auth_page).checkout()
            step_one = CheckoutStepOnePage(auth_page)
            step_one.fill_details("Jane", "Doe", "1000")
            step_one.continue_checkout()

        with allure.step("Cancelar en paso 2"):
            step_two = CheckoutStepTwoPage(auth_page)
            step_two.cancel()

        with allure.step("Verificar retorno al inventory"):
            assert InventoryPage(auth_page).is_loaded()

    @allure.story("Resumen")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_step_two_total_breakdown(self, auth_page):
        with allure.step("Completar paso 1"):
            CartPage(auth_page).checkout()
            step_one = CheckoutStepOnePage(auth_page)
            step_one.fill_details("Jane", "Doe", "1000")
            step_one.continue_checkout()

        with allure.step("Verificar breakdown de totales"):
            step_two = CheckoutStepTwoPage(auth_page)
            assert "Item total" in step_two.get_subtotal()
            assert "Tax" in step_two.get_tax()
            assert "Total" in step_two.get_total()

    # ── Flujo completo ─────────────────────────────────────

    @allure.story("Flujo completo")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_checkout_flow(self, auth_page):
        with allure.step("Checkout paso 1 — completar datos"):
            CartPage(auth_page).checkout()
            step_one = CheckoutStepOnePage(auth_page)
            step_one.fill_details("Jane", "Doe", "1000")
            step_one.continue_checkout()

        with allure.step("Checkout paso 2 — finalizar"):
            step_two = CheckoutStepTwoPage(auth_page)
            step_two.finish()

        with allure.step("Verificar orden completada"):
            complete = CheckoutCompletePage(auth_page)
            assert complete.is_loaded()
            assert "Thank you" in complete.get_header_text()
            assert complete.get_complete_text() != ""

    @allure.story("Flujo completo")
    @allure.severity(allure.severity_level.NORMAL)
    def test_back_home_after_checkout(self, auth_page):
        with allure.step("Completar checkout"):
            CartPage(auth_page).checkout()
            step_one = CheckoutStepOnePage(auth_page)
            step_one.fill_details("Jane", "Doe", "1000")
            step_one.continue_checkout()

            step_two = CheckoutStepTwoPage(auth_page)
            step_two.finish()

        with allure.step("Volver al inicio"):
            complete = CheckoutCompletePage(auth_page)
            complete.back_home()

        with allure.step("Verificar retorno al inventory"):
            assert InventoryPage(auth_page).is_loaded()
