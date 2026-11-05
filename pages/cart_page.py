from .base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"
    ITEM = BasePage.dt("inventory-item")
    CHECKOUT = BasePage.dt("checkout")
    CONTINUE = BasePage.dt("continue-shopping")

    LIST = BasePage.dt("cart-list")

    def wait_until_loaded(self) -> None:
        # The address changes before the page is drawn, so wait for the cart's own list as well.
        self.wait_for_url_part("/cart.html")
        self.find(self.LIST)

    def count(self) -> int:
        return len(self.find_all(self.ITEM))

    def has_count(self, expected: int) -> bool:
        return self.becomes(self.count, expected)

    def item_text(self) -> str:
        return " ".join(e.text for e in self.find_all(self.ITEM))

    def remove(self, slug: str) -> None:
        self.click(self.dt(f"remove-{slug}"))

    def checkout(self) -> None:
        self.click(self.CHECKOUT)

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE)
