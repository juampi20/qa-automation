from .base_page import BasePage


class InventoryPage(BasePage):
    """Página de inventario / listado de productos."""

    CART_LINK = ".shopping_cart_link"
    CART_COUNTER = ".shopping_cart_badge"
    INVENTORY_CONTAINER = "#inventory_container"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ITEM_IMG = ".inventory_item_img"
    ADD_BUTTON = ".btn_inventory"
    REMOVE_BUTTON = ".btn_inventory"
    SORT_DROPDOWN = ".product_sort_container"
    SORT_OPTION_ZA = "za"
    SORT_OPTION_LOHI = "lohi"
    SORT_OPTION_HILO = "hilo"

    # ── Items fijos para acceso rápido ──────────────────────

    FIRST_ITEM_ADD_BUTTON = ".inventory_item:nth-child(1) .btn_inventory"
    SECOND_ITEM_ADD_BUTTON = ".inventory_item:nth-child(2) .btn_inventory"
    FIRST_ITEM_REMOVE_BUTTON = ".inventory_item:nth-child(1) .btn_inventory"
    SECOND_ITEM_REMOVE_BUTTON = ".inventory_item:nth-child(2) .btn_inventory"

    def navigate(self) -> None:
        """Navegar a la página de inventario."""
        self.page.goto("/inventory.html")

    def is_loaded(self) -> bool:
        """Verificar que la página de inventario se haya cargado."""
        return "/inventory.html" in self.page.url

    # ── Carrito ─────────────────────────────────────────

    def get_cart_item_count(self) -> int:
        """Obtener la cantidad de items en el carrito."""
        if self.is_visible_fast(self.CART_COUNTER):
            return int(self.get_text(self.CART_COUNTER))
        return 0

    def go_to_cart(self) -> None:
        """Ir a la página del carrito."""
        self.click(self.CART_LINK)

    # ── Agregar items ───────────────────────────────────

    def add_first_item_to_cart(self) -> None:
        """Agregar el primer producto al carrito."""
        self.click(self.FIRST_ITEM_ADD_BUTTON)

    def add_second_item_to_cart(self) -> None:
        """Agregar el segundo producto al carrito."""
        self.click(self.SECOND_ITEM_ADD_BUTTON)

    def add_item_to_cart_by_name(self, item_name: str) -> None:
        """Agregar un producto al carrito por su nombre."""
        item = self._locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        item.locator(self.ADD_BUTTON).click()

    # ── Remover items ───────────────────────────────────

    def remove_first_item_from_cart(self) -> None:
        """Remover el primer producto del carrito (desde inventario)."""
        self.click(self.FIRST_ITEM_REMOVE_BUTTON)

    def remove_second_item_from_cart(self) -> None:
        """Remover el segundo producto del carrito (desde inventario)."""
        self.click(self.SECOND_ITEM_REMOVE_BUTTON)

    def remove_item_from_cart_by_name(self, item_name: str) -> None:
        """Remover un producto del carrito por su nombre (desde inventario)."""
        item = self._locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        item.locator(self.REMOVE_BUTTON).click()

    def is_remove_button_visible(self, item_name: str) -> bool:
        """Verificar si el botón Remove está visible para un producto."""
        item = self._locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        return item.locator(self.REMOVE_BUTTON).is_visible(timeout=500)

    # ── Leer datos ──────────────────────────────────────

    def get_item_names(self) -> list[str]:
        """Obtener los nombres de todos los productos visibles."""
        return self.get_texts(self.ITEM_NAME)

    def get_item_count(self) -> int:
        """Cantidad de productos visibles en la página."""
        return self.count(self.INVENTORY_ITEM)

    def click_item_by_name(self, item_name: str) -> None:
        """Hacer clic en un producto para ver su detalle."""
        self._locator(self.ITEM_NAME).filter(has_text=item_name).click()

    # ── Sorting ─────────────────────────────────────────

    def sort_by(self, value: str) -> None:
        """Ordenar productos por valor del dropdown (az, za, lohi, hilo)."""
        self.page.select_option(self.SORT_DROPDOWN, value)
