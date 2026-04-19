import pytest
import allure
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright():
    # Configuración de Playwright
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="function")
def browser(playwright):
    # Lanzar el navegador
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def context(browser):
    # Configuración del contexto
    context = browser.new_context(viewport={"width": 1600, "height": 900})
    yield context
    context.close()

@pytest.fixture(scope="function")
def driver(context):
    # Configuración de la página
    page = context.new_page()
    yield page
    page.close()