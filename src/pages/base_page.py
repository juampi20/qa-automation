from playwright.sync_api import Locator, Page, expect


class BasePage:
    MENU_BUTTON = "#react-burger-menu-btn"
    MENU_CLOSE_BUTTON = "#react-burger-cross-btn"
    SIDEBAR_CONTAINER = ".bm-menu-wrap"
    ALL_ITEMS_LINK = "#inventory_sidebar_link"
    ABOUT_LINK = "#about_sidebar_link"
    LOGOUT_LINK = "#logout_sidebar_link"
    RESET_LINK = "#reset_sidebar_link"
    SIDEBAR_NAV_ITEMS = ".bm-item-list a"

    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.timeout = timeout

    # ── Navegación ──────────────────────────────────────────

    def goto(self, url: str) -> None:
        self.page.goto(url)

    @property
    def current_url(self) -> str:
        return self.page.url

    # ── Localizadores ───────────────────────────────────────

    def _locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    # ── Acciones ────────────────────────────────────────────

    def click(self, selector: str) -> None:
        self._locator(selector).click()

    def fill(self, selector: str, text: str) -> None:
        self._locator(selector).fill(text)

    def select_option(self, selector: str, value: str) -> None:
        self._locator(selector).select_option(value)

    # ── Lectura ─────────────────────────────────────────────

    def get_text(self, selector: str) -> str:
        return self._locator(selector).inner_text()

    def get_texts(self, selector: str) -> list[str]:
        return self._locator(selector).all_inner_texts()

    def is_visible(self, selector: str) -> bool:
        return self._locator(selector).is_visible()

    def is_visible_fast(self, selector: str) -> bool:
        return self._locator(selector).is_visible(timeout=500)

    def get_attribute(self, selector: str, attr: str) -> str | None:
        return self._locator(selector).get_attribute(attr)

    def count(self, selector: str) -> int:
        return self._locator(selector).count()

    # ── Esperas ─────────────────────────────────────────────

    def wait_for(self, selector: str, state: str = "visible") -> None:
        self._locator(selector).wait_for(state=state, timeout=self.timeout)

    def wait_for_url(self, url: str, timeout: int | None = None) -> None:
        self.page.wait_for_url(url, timeout=timeout or self.timeout)

    def wait_for_function(self, expression: str, timeout: int | None = None) -> None:
        self.page.wait_for_function(expression, timeout=timeout or self.timeout)

    # ── Capturas ────────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        _ = name  # Avoid unused parameter warning
        return self.page.screenshot(type="png")

    # ── Aserciones ──────────────────────────────────────────

    def should_have_url(self, partial_url: str) -> None:
        expect(self.page).to_have_url(partial_url)

    def should_be_visible(self, selector: str) -> None:
        expect(self._locator(selector)).to_be_visible()

    def should_contain_text(self, selector: str, text: str) -> None:
        expect(self._locator(selector)).to_contain_text(text)

    # ── Menú lateral ────────────────────────────────────────

    def open_menu(self) -> None:
        self.click(self.MENU_BUTTON)
        self.wait_for(self.RESET_LINK)
        self.wait_for_function(
            "() => document.querySelector('.bm-menu-wrap').getBoundingClientRect().x > -100"
        )

    def close_menu(self) -> None:
        self.click(self.MENU_CLOSE_BUTTON)
        self.wait_for_function(
            "() => document.querySelector('.bm-menu-wrap').getBoundingClientRect().x < -280"
        )

    def is_menu_open(self) -> bool:
        bbox = self._locator(self.SIDEBAR_CONTAINER).bounding_box()
        return bbox is not None and bbox["x"] > -100

    def get_sidebar_links(self) -> list[str]:
        return self.get_texts(self.SIDEBAR_NAV_ITEMS)

    def click_sidebar_all_items(self) -> None:
        self.click(self.ALL_ITEMS_LINK)

    def click_sidebar_about(self) -> None:
        self.click(self.ABOUT_LINK)

    def click_sidebar_logout(self) -> None:
        self.click(self.LOGOUT_LINK)

    def click_sidebar_reset(self) -> None:
        self.click(self.RESET_LINK)
