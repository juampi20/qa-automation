import os
import re

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
    if report.when == "call":
        item.rep_call = report
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


def _save_trace(context, node):
    """Guarda el trace de Playwright solo si el test falló."""
    rep_call = getattr(node, "rep_call", None)
    if rep_call and rep_call.failed:
        trace_dir = "traces"
        os.makedirs(trace_dir, exist_ok=True)
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", node.name)
        context.tracing.stop(path=os.path.join(trace_dir, f"{safe_name}.zip"))
    else:
        context.tracing.stop()  # descartar


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
def context(browser, request):
    ctx = browser.new_context(viewport={"width": 1600, "height": 900})
    ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    _save_trace(ctx, request.node)
    ctx.close()


@pytest.fixture(scope="function")
def page(context):
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def auth_page(browser, request):
    """Login nuevo por test. SauceDemo es in-memory SPA — no comparte sesión."""
    context = browser.new_context(viewport={"width": 1600, "height": 900})
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.goto(BASE_URL)
    page.fill("#user-name", STANDARD_USER)
    page.fill("#password", STANDARD_PASSWORD)
    page.click("#login-button")
    page.wait_for_url("**/inventory.html")
    yield page
    _save_trace(context, request.node)
    context.close()
