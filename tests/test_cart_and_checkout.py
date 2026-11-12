import pytest

from pages import flows
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

manual = pytest.mark.manual
CATALOG = [
    ("sauce-labs-backpack", 29.99), ("sauce-labs-bike-light", 9.99), ("sauce-labs-bolt-t-shirt", 15.99),
    ("sauce-labs-fleece-jacket", 49.99), ("sauce-labs-onesie", 7.99), ("test.allthethings()-t-shirt-(red)", 15.99),
]


@pytest.fixture
def cart(driver, base_url, inventory) -> CartPage:
    """A cart holding the backpack ($29.99) and the bike light ($9.99), opened."""
    inventory.add("sauce-labs-backpack", "sauce-labs-bike-light")
    inventory.open_cart()
    page = CartPage(driver, base_url)
    page.wait_until_loaded()
    return page


@pytest.fixture
def checkout(driver, base_url, inventory) -> CheckoutPage:
    return flows.to_checkout_form(driver, base_url, inventory, "sauce-labs-backpack", "sauce-labs-bike-light")


@manual("TC-032")
def test_cart_shows_the_products_with_their_prices(cart):
    assert cart.has_count(2), f"cart shows {cart.count()} rows"
    assert "Sauce Labs Backpack" in cart.item_text()
    assert "$29.99" in cart.item_text()


@manual("TC-031")
def test_removing_a_product_leaves_one(cart):
    cart.remove("sauce-labs-backpack")
    assert cart.has_count(1), f"cart shows {cart.count()} rows"


def test_continue_shopping_returns_to_the_list(cart):
    cart.continue_shopping()
    cart.wait_for_url_part("/inventory.html")


@pytest.mark.smoke
@manual("TC-051")
def test_complete_order_reaches_the_confirmation_page(checkout):
    checkout.fill_info()
    checkout.finish()
    assert checkout.confirmation() == "Thank you for your order!"


@manual("TC-048")
@manual("TC-049")
@manual("TC-050")
def test_order_summary_adds_up_with_figures_worked_out_in_the_test(driver, base_url, inventory):
    chosen = CATALOG[:3]
    page = flows.to_overview(driver, base_url, inventory, *[slug for slug, _ in chosen])
    subtotal = round(sum(price for _, price in chosen), 2)
    tax = round(subtotal * 0.08, 2)
    assert page.amounts() == (pytest.approx(subtotal), pytest.approx(tax), pytest.approx(round(subtotal + tax, 2)))


@manual("TC-077")
def test_totals_are_correct_when_all_six_products_are_bought(driver, base_url, inventory):
    page = flows.to_overview(driver, base_url, inventory, *[slug for slug, _ in CATALOG])
    assert page.amounts() == (pytest.approx(129.94), pytest.approx(10.4), pytest.approx(140.34))


@pytest.mark.parametrize(
    "fields, message",
    [
        pytest.param({"first": ""}, "First Name is required", marks=manual("TC-039"), id="no-first-name"),
        pytest.param({"last": ""}, "Last Name is required", marks=manual("TC-040"), id="no-last-name"),
        pytest.param({"postal": ""}, "Postal Code is required", marks=manual("TC-041"), id="no-postal-code"),
    ],
)
def test_each_missing_field_is_reported(checkout, fields, message):
    checkout.fill_info(**fields)
    assert message in checkout.error_text()


@manual("TC-045")
def test_cancel_goes_back_to_the_cart_with_the_products(driver, base_url, checkout):
    checkout.cancel()
    page = CartPage(driver, base_url)
    page.wait_until_loaded()
    assert page.has_count(2), f"cart shows {page.count()} rows"


@manual("TC-052")
def test_cart_is_empty_after_a_completed_order(driver, base_url, inventory):
    flows.place_order(driver, base_url, inventory, "sauce-labs-bike-light")
    assert inventory.has_badge(0)


@manual("TC-053")
def test_back_home_returns_to_the_product_list(driver, base_url, inventory):
    page = flows.place_order(driver, base_url, inventory, "sauce-labs-bike-light")
    page.click(page.dt("back-to-products"))
    inventory.wait_until_loaded()
