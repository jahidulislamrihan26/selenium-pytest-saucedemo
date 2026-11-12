"""Known defects of the standard user's journey. Same convention as test_personas.py: the test states the CORRECT behaviour and is
marked xfail(strict=True), so it stays green while the defect exists and turns red the day it is fixed."""
import pytest

from pages import flows
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

manual = pytest.mark.manual
known = pytest.mark.known_bug


@known
@manual("TC-038")
@pytest.mark.xfail(reason="BUG-001: an empty cart can be checked out")
def test_checkout_is_blocked_when_the_cart_is_empty(driver, base_url, inventory):
    inventory.open_cart()
    cart = CartPage(driver, base_url)
    cart.wait_until_loaded()
    cart.checkout()
    assert not cart.url_becomes("checkout-step-one"), "the checkout form opened with an empty cart"


@known
@manual("TC-042")
@pytest.mark.xfail(reason="BUG-002: any text is accepted as a postal code")
def test_postal_code_with_letters_is_rejected(driver, base_url, inventory):
    form = flows.to_checkout_form(driver, base_url, inventory, "sauce-labs-backpack")
    form.fill_info(postal="abc!@#")
    assert "Postal Code" in form.error_text()


@known
@manual("TC-043")
@pytest.mark.xfail(reason="BUG-002: whitespace-only values are accepted")
def test_whitespace_only_names_are_rejected(driver, base_url, inventory):
    form = flows.to_checkout_form(driver, base_url, inventory, "sauce-labs-backpack")
    form.fill_info(first=" ", last=" ", postal=" ")
    assert form.error_text()


@known
@manual("TC-044")
@pytest.mark.xfail(reason="BUG-002: no length limit on the first name")
def test_a_300_character_first_name_is_rejected(driver, base_url, inventory):
    form = flows.to_checkout_form(driver, base_url, inventory, "sauce-labs-backpack")
    form.fill_info(first="A" * 300)
    assert form.error_text()


@known
@manual("TC-034")
@pytest.mark.xfail(reason="BUG-003: Reset App State leaves the buttons on Remove")
def test_reset_app_state_restores_the_add_to_cart_buttons(inventory):
    inventory.add("sauce-labs-backpack")
    inventory.reset_app_state()
    assert inventory.has_badge(0)
    assert inventory.appears(inventory.dt("add-to-cart-sauce-labs-backpack")), "the button is still Remove"


@known
@manual("TC-080")
@pytest.mark.xfail(reason="BUG-017: the sort choice is lost after viewing a product")
def test_sort_choice_is_kept_after_viewing_a_product(inventory):
    inventory.sort_by("za")
    inventory.click(inventory.NAME)
    inventory.click(inventory.dt("back-to-products"))
    inventory.wait_until_loaded()
    assert inventory.sort_value() == "za"


@known
@manual("TC-073")
@pytest.mark.xfail(reason='BUG-014: "Thank you for your order!" is shown without an order')
def test_order_confirmation_cannot_be_opened_without_an_order(driver, base_url, inventory):
    driver.get(base_url + "/checkout-complete.html")
    page = CheckoutPage(driver, base_url)
    assert not page.appears(page.DONE), "the confirmation is shown without an order"


@known
@manual("TC-074")
@pytest.mark.xfail(reason="BUG-015: the overview opens with a $0.00 total and a working Finish button")
def test_checkout_overview_cannot_be_opened_with_an_empty_cart(driver, base_url, inventory):
    driver.get(base_url + "/checkout-step-two.html")
    page = CheckoutPage(driver, base_url)
    assert not page.appears(page.FINISH), "the overview opens with a working Finish button"


@known
@manual("TC-075")
@pytest.mark.xfail(reason="BUG-015: Back returns to the overview and Finish accepts a second, empty order")
def test_back_button_after_an_order_does_not_allow_finishing_it_again(driver, base_url, inventory):
    page = flows.place_order(driver, base_url, inventory, "sauce-labs-backpack")
    driver.back()
    assert not page.appears(page.FINISH), "Back returns to a working overview"


@known
@manual("TC-072")
@pytest.mark.xfail(reason="BUG-019: the product not-found message is worded for a telephone line")
def test_product_not_found_page_uses_plain_language(driver, base_url, inventory):
    driver.get(base_url + "/inventory-item.html?id=999")
    inventory.find(inventory.dt("inventory-item-name"))  # wait until the page is drawn
    assert "your call could not be completed" not in driver.page_source


@known
@manual("TC-072")
@pytest.mark.xfail(reason="BUG-019: unknown addresses show a blank page")
def test_unknown_address_shows_a_helpful_page(driver, base_url, inventory):
    driver.get(base_url + "/nonexistent-page.html")
    from selenium.webdriver.common.by import By
    assert driver.find_element(By.TAG_NAME, "body").text.strip() != ""
