import os

import allure
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com"
STANDARD_USER = "standard_user"
STANDARD_PASSWORD = "secret_sauce"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or (
            item.funcargs.get("auth_page")
            if isinstance(item.funcargs.get("auth_page"), tuple)
            else item.funcargs.get("auth_page")
        )
        # auth_page returns (page, inventory_page) tuple or page directly
        if isinstance(page, tuple):
            page = page[0]
        if page and not page.is_closed():
            try:
                screenshot = page.screenshot(type="png")
                allure.attach(
                    screenshot,
                    name=f"screenshot_{report.nodeid}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass


HEADLESS = os.environ.get("HEADLESS", "").lower() in ("1", "true", "yes")
SLOW_MO = int(os.environ.get("SLOW_MO", "0"))


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    ctx = browser.new_context(viewport={"width": 1600, "height": 900})
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context):
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def auth_page(browser):
    """Login nuevo por test. SauceDemo es in-memory SPA — no comparte sesión."""
    context = browser.new_context(viewport={"width": 1600, "height": 900})
    page = context.new_page()
    page.goto(BASE_URL)
    page.fill("#user-name", STANDARD_USER)
    page.fill("#password", STANDARD_PASSWORD)
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    yield page
    context.close()
