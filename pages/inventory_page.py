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
    SORT = BasePage.dt("product-sort-container")
    BADGE = BasePage.dt("shopping-cart-badge")
    CART_LINK = BasePage.dt("shopping-cart-link")
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = BasePage.dt("logout-sidebar-link")

    def wait_until_loaded(self) -> None:
        self.wait_for_url_part("/inventory.html")
        self.find(self.ITEM)

    def count(self) -> int:
        return len(self.find_all(self.ITEM))

    def names(self) -> list[str]:
        return [e.text for e in self.find_all(self.NAME)]

    def prices(self) -> list[float]:
        return [money(e.text) for e in self.find_all(self.PRICE)]

    def sort_by(self, value: str) -> None:
        Select(self.find(self.SORT)).select_by_value(value)

    def add(self, *slugs: str) -> None:
        for slug in slugs:
            self.click(self.dt(f"add-to-cart-{slug}"))

    def remove(self, slug: str) -> None:
        self.click(self.dt(f"remove-{slug}"))

    def badge_count(self) -> int:
        return int(self.text_of(self.BADGE)) if self.is_present(self.BADGE) else 0

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def open_product(self, item_id: int) -> None:
        self.click(self.dt(f"item-{item_id}-title-link"))

    def logout(self) -> None:
        self.click(self.MENU)
        self.click(self.LOGOUT)
