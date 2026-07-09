import os

import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com"
STANDARD_USER = "standard_user"
STANDARD_PASSWORD = "secret_sauce"

HEADLESS = os.environ.get("HEADLESS", "").lower() in ("1", "true", "yes")
SLOW_MO = int(os.environ.get("SLOW_MO", "0"))


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    """Navegador Chromium — UNO solo para toda la sesión.

    Cada test crea su propio context + page, pero el navegador
    arranca UNA vez. Ahorra ~1s por test comparado con function-scope.
    """
    browser = playwright.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Contexto limpio para tests de login (sin autenticar)."""
    ctx = browser.new_context(viewport={"width": 1600, "height": 900})
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context):
    """Página sin autenticar. Para tests de login."""
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def auth_page(browser):
    """Página autenticada — login fresco por test.

    SauceDemo es una SPA client-side sin persistencia de sesión.
    No hay forma de compartir auth entre pages o contexts.
    La optimización real: browser session-scoped (launch una vez).
    """
    context = browser.new_context(viewport={"width": 1600, "height": 900})
    page = context.new_page()
    page.goto(BASE_URL)
    page.fill("#user-name", STANDARD_USER)
    page.fill("#password", STANDARD_PASSWORD)
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    yield page
    context.close()
