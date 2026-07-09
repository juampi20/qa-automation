from pages.inventory_page import InventoryPage
from pages.item_details_page import ItemDetailsPage


class TestInventory:

    def test_inventory_is_loaded(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        assert inventory_page.is_loaded()

    def test_inventory_shows_items(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        assert inventory_page.get_item_count() > 0

    def test_remove_item_from_inventory(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1

        inventory_page.remove_first_item()
        assert inventory_page.get_cart_item_count() == 0

    def test_add_and_remove_multiple_from_inventory(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.add_first_item_to_cart()
        inventory_page.add_second_item_to_cart()
        assert inventory_page.get_cart_item_count() == 2

        inventory_page.remove_first_item()
        assert inventory_page.get_cart_item_count() == 1

        inventory_page.remove_second_item()
        assert inventory_page.get_cart_item_count() == 0

    def test_sort_by_name_z_to_a(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        names_before = inventory_page.get_item_names()

        inventory_page.sort_by("za")
        names_after = inventory_page.get_item_names()

        assert names_after == sorted(names_before, reverse=True)
        assert names_after != names_before

    def test_sort_by_price_low_to_high(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.sort_by("lohi")

        prices = inventory_page.get_texts(inventory_page.ITEM_PRICE)
        numeric_prices = [float(p.replace("$", "")) for p in prices]
        assert numeric_prices == sorted(numeric_prices)

    def test_sort_by_price_high_to_low(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.sort_by("hilo")

        prices = inventory_page.get_texts(inventory_page.ITEM_PRICE)
        numeric_prices = [float(p.replace("$", "")) for p in prices]
        assert numeric_prices == sorted(numeric_prices, reverse=True)

    def test_click_item_navigates_to_details(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        inventory_page.click_item_by_name("Sauce Labs Backpack")

        details = ItemDetailsPage(auth_page)
        assert details.is_loaded()
        assert details.get_item_name() == "Sauce Labs Backpack"

    def test_cart_badge_updates_after_add_and_remove(self, auth_page):
        inventory_page = InventoryPage(auth_page)
        assert inventory_page.get_cart_item_count() == 0

        inventory_page.add_first_item_to_cart()
        assert inventory_page.get_cart_item_count() == 1

        inventory_page.remove_first_item()
        assert inventory_page.get_cart_item_count() == 0
