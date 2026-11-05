from .base_page import BasePage
from .inventory_page import money


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"
    FIRST = BasePage.dt("firstName")
    LAST = BasePage.dt("lastName")
    ZIP = BasePage.dt("postalCode")
    CONTINUE = BasePage.dt("continue")
    CANCEL = BasePage.dt("cancel")
    FINISH = BasePage.dt("finish")
    ERROR = BasePage.dt("error")
    DONE = BasePage.dt("complete-header")

    def fill_info(self, first: str = "Ada", last: str = "Lovelace", postal: str = "12345") -> None:
        for locator, value in ((self.FIRST, first), (self.LAST, last), (self.ZIP, postal)):
            if value:
                self.type_into(locator, value)
        self.click(self.CONTINUE)

    def error_text(self) -> str:
        return self.text_of(self.ERROR)

    def amounts(self) -> tuple[float, float, float]:
        """Items subtotal, tax and total as shown on the order summary."""
        return tuple(money(self.text_of(self.dt(k))) for k in ("subtotal-label", "tax-label", "total-label"))  # type: ignore[return-value]

    def finish(self) -> None:
        self.click(self.FINISH)

    def confirmation(self) -> str:
        return self.text_of(self.DONE)

    def cancel(self) -> None:
        self.click(self.CANCEL)
