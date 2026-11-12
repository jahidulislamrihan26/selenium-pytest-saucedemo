"""Whole journeys, for tests that are about something else than the journey itself. They assume the user is logged in."""
from .cart_page import CartPage
from .checkout_page import CheckoutPage
from .inventory_page import InventoryPage


def to_checkout_form(driver, base_url, inventory: InventoryPage, *slugs: str) -> CheckoutPage:
    inventory.add(*slugs)
    inventory.open_cart()
    cart = CartPage(driver, base_url)
    cart.wait_until_loaded()
    cart.checkout()
    form = CheckoutPage(driver, base_url)
    form.wait_for_url_part("checkout-step-one")
    return form


def to_overview(driver, base_url, inventory: InventoryPage, *slugs: str) -> CheckoutPage:
    form = to_checkout_form(driver, base_url, inventory, *slugs)
    form.fill_info()
    form.wait_for_url_part("checkout-step-two")
    return form


def place_order(driver, base_url, inventory: InventoryPage, *slugs: str) -> CheckoutPage:
    page = to_overview(driver, base_url, inventory, *slugs)
    page.finish()
    page.confirmation()  # waits until the confirmation is on screen
    return page
