import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


def money(text: str) -> float:
    return float(re.sub(r"[^0-9.]", "", text))


class InventoryPage(BasePage):
    path = "/inventory.html"
    ITEM = BasePage.dt("inventory-item")
    NAME = BasePage.dt("inventory-item-name")
    PRICE = BasePage.dt("inventory-item-price")
    IMAGE = (By.CSS_SELECTOR, "img.inventory_item_img")
    SORT = BasePage.dt("product-sort-container")
    BADGE = BasePage.dt("shopping-cart-badge")
    CART_LINK = BasePage.dt("shopping-cart-link")
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = BasePage.dt("logout-sidebar-link")
    RESET = BasePage.dt("reset-sidebar-link")

    def wait_until_loaded(self) -> None:
        self.wait_for_url_part("/inventory.html")
        self.find(self.ITEM)

    def count(self) -> int:
        return len(self.find_all(self.ITEM))

    def names(self) -> list[str]:
        return [e.text for e in self.find_all(self.NAME)]

    def prices(self) -> list[float]:
        return [money(e.text) for e in self.find_all(self.PRICE)]

    def image_sources(self) -> list[str]:
        return [e.get_attribute("src") for e in self.find_all(self.IMAGE)]

    def sort_by(self, value: str) -> None:
        Select(self.find(self.SORT)).select_by_value(value)

    def sort_value(self) -> str:
        return Select(self.find(self.SORT)).first_selected_option.get_attribute("value")

    def add(self, *slugs: str) -> None:
        for slug in slugs:
            self.click(self.dt(f"add-to-cart-{slug}"))

    def add_all(self) -> None:
        for button in self.find_all((By.CSS_SELECTOR, "button.btn_inventory")):
            button.click()

    def remove(self, slug: str) -> None:
        self.click(self.dt(f"remove-{slug}"))

    def has_button(self, locator_id: str) -> bool:
        return self.is_present(self.dt(locator_id))

    def badge_count(self) -> int:
        return int(self.text_of(self.BADGE)) if self.is_present(self.BADGE) else 0

    def has_badge(self, expected: int) -> bool:
        return self.becomes(self.badge_count, expected)

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def open_product(self, item_id: int) -> None:
        self.click(self.dt(f"item-{item_id}-title-link"))

    def open_menu(self) -> None:
        self.click(self.MENU)

    def logout(self) -> None:
        self.open_menu()
        self.click(self.LOGOUT)

    def reset_app_state(self) -> None:
        self.open_menu()
        self.click(self.RESET)
