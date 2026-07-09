from playwright.sync_api import Page, Locator, expect


class BasePage:
    # ── Sidebar (disponible en todas las páginas autenticadas) ────

    MENU_BUTTON = "#react-burger-menu-btn"
    MENU_CLOSE_BUTTON = "#react-burger-cross-btn"
    SIDEBAR_CONTAINER = ".bm-menu-wrap"
    SIDEBAR_ITEMS_CONTAINER = ".bm-item-list"
    ALL_ITEMS_LINK = "#inventory_sidebar_link"
    ABOUT_LINK = "#about_sidebar_link"
    LOGOUT_LINK = "#logout_sidebar_link"
    RESET_LINK = "#reset_sidebar_link"
    SIDEBAR_NAV_ITEMS = ".bm-item-list a"
    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.timeout = timeout

    # ── Sidebar (disponible en todas las páginas autenticadas) ──

    def open_menu(self) -> None:
        self.click(self.MENU_BUTTON)
        self._locator(self.RESET_LINK).wait_for(state="visible", timeout=5000)
        self._locator(self.SIDEBAR_CONTAINER).wait_for(
            state="attached", timeout=5000
        )
        # La transición CSS de SauceDemo tarda ~0.5s en mover el
        # sidebar a la posición visible. Playwright considera el
        # elemento "visible" incluso antes de que la transición
        # termine, así que esperamos a que el bounding box refleje
        # la posición real.
        self.page.wait_for_function(
            "() => document.querySelector('.bm-menu-wrap').getBoundingClientRect().x > -100",
            timeout=5000,
        )

    def close_menu(self) -> None:
        self.click(self.MENU_CLOSE_BUTTON)

    def close_menu_and_wait(self) -> None:
        """Cerrar y esperar que el sidebar desaparezca."""
        self.close_menu()
        self.page.wait_for_function(
            "() => document.querySelector('.bm-menu-wrap').getBoundingClientRect().x < -280",
            timeout=5000,
        )

    def is_menu_open(self) -> bool:
        """Verificar si el sidebar está abierto.

        SauceDemo esconde el sidebar con CSS translate3d. Cuando
        está cerrado, el bounding box tiene x ≈ -300; cuando está
        abierto, x ≈ 0. Usamos un threshold para evitar falsos
        negativos por sub-pixel rendering durante transiciones.
        """
        bbox = self._locator(self.SIDEBAR_CONTAINER).bounding_box()
        return bbox is not None and bbox["x"] > -100

    def is_menu_closed(self) -> bool:
        return not self.is_menu_open()

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

    # ── Navegación ──────────────────────────────────────────

    def navigate(self, url: str) -> None:
        """Navegar a una URL absoluta o relativa."""
        self.page.goto(url)

    # ── Locators ────────────────────────────────────────────

    def _locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    # ── Acciones ────────────────────────────────────────────

    def click(self, selector: str) -> None:
        """Hacer clic en un elemento."""
        self._locator(selector).click()

    def fill(self, selector: str, text: str) -> None:
        """Rellenar un campo de texto."""
        self._locator(selector).fill(text)

    def get_text(self, selector: str) -> str:
        """Obtener el texto visible de un elemento."""
        return self._locator(selector).inner_text()

    def get_texts(self, selector: str) -> list[str]:
        """Obtener los textos visibles de múltiples elementos."""
        return self._locator(selector).all_inner_texts()

    def is_visible(self, selector: str) -> bool:
        """Verificar si un elemento es visible."""
        return self._locator(selector).is_visible()

    def is_visible_fast(self, selector: str) -> bool:
        """Verificar visibilidad con timeout reducido (útil para asserts negativos)."""
        return self._locator(selector).is_visible(timeout=500)

    def wait_for(self, selector: str, state: str = "visible") -> None:
        """Esperar a que un elemento alcance un estado."""
        self._locator(selector).wait_for(state=state, timeout=self.timeout)

    def get_attribute(self, selector: str, attr: str) -> str | None:
        """Obtener un atributo de un elemento."""
        return self._locator(selector).get_attribute(attr)

    def count(self, selector: str) -> int:
        """Contar cuántos elementos coinciden con el selector."""
        return self._locator(selector).count()

    # ── Screenshots ─────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Tomar un screenshot de la página actual."""
        return self.page.screenshot(type="png")

    # ── Assertions ──────────────────────────────────────────

    def should_have_url(self, partial_url: str) -> None:
        """Assert de que la URL contiene un texto."""
        expect(self.page).to_have_url(partial_url)

    def should_be_visible(self, selector: str) -> None:
        """Assert de que un elemento es visible."""
        expect(self._locator(selector)).to_be_visible()

    def should_contain_text(self, selector: str, text: str) -> None:
        """Assert de que un elemento contiene un texto."""
        expect(self._locator(selector)).to_contain_text(text)
