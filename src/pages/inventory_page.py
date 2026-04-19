from .base_page import BasePage

class InventoryPage(BasePage):
    MENU_BUTTON = "#react-burger-menu-btn"
    FIRST_ITEM_ADD_BUTTON = ".inventory_item:nth-child(1) .btn_inventory"
    SECOND_ITEM_ADD_BUTTON = ".inventory_item:nth-child(2) .btn_inventory"
    CART_COUNTER = ".shopping_cart_badge"

    def open_menu(self) -> None:
        self.page.click(self.MENU_BUTTON)

    def is_loaded(self) -> bool:
        # Verificar "/inventory.html" en la url
        return "/inventory.html" in self.page.url
    
    def get_cart_item_count(self) -> int:
        # Obtener el número de items en el carrito
        if self.page.locator(self.CART_COUNTER).is_visible():
            return int(self.page.inner_text(self.CART_COUNTER))
        return 0
    
    def add_first_item_to_cart(self) -> None:
        # Agregar el primer item al carrito
        self.page.click(self.FIRST_ITEM_ADD_BUTTON)

    def add_second_item_to_cart(self) -> None:
        # Agregar el segundo item al carrito
        self.page.click(self.SECOND_ITEM_ADD_BUTTON)