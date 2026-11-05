import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def cart(driver, base_url, inventory) -> CartPage:
    """A cart holding the backpack ($29.99) and the bike light ($9.99), opened."""
    inventory.add("sauce-labs-backpack", "sauce-labs-bike-light")
    inventory.open_cart()
    page = CartPage(driver, base_url)
    page.wait_until_loaded()
    return page


@pytest.fixture
def checkout(driver, base_url, cart) -> CheckoutPage:
    cart.checkout()
    page = CheckoutPage(driver, base_url)
    page.wait_for_url_part("checkout-step-one")
    return page


def test_cart_shows_the_products_with_their_prices(cart):
    assert cart.count() == 2
    assert "Sauce Labs Backpack" in cart.item_text()
    assert "$29.99" in cart.item_text()


def test_removing_a_product_leaves_one(cart):
    cart.remove("sauce-labs-backpack")
    assert cart.count() == 1


def test_continue_shopping_returns_to_the_list(cart):
    cart.continue_shopping()
    cart.wait_for_url_part("/inventory.html")


@pytest.mark.smoke
def test_complete_order_reaches_the_confirmation_page(checkout):
    checkout.fill_info()
    checkout.finish()
    assert checkout.confirmation() == "Thank you for your order!"


def test_order_summary_adds_up(checkout):
    checkout.fill_info()
    subtotal, tax, total = checkout.amounts()
    assert subtotal == pytest.approx(29.99 + 9.99)
    assert subtotal + tax == pytest.approx(total, abs=0.005)


@pytest.mark.parametrize(
    "fields, message",
    [
        ({"first": ""}, "First Name is required"),
        ({"last": ""}, "Last Name is required"),
        ({"postal": ""}, "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_each_missing_field_is_reported(checkout, fields, message):
    checkout.fill_info(**fields)
    assert message in checkout.error_text()


def test_cancel_goes_back_to_the_cart_with_the_products(driver, base_url, checkout):
    checkout.cancel()
    page = CartPage(driver, base_url)
    page.wait_until_loaded()
    assert page.count() == 2
