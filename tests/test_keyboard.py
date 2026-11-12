"""Keyboard use (manual-testing charter 6). An automated accessibility scan cannot see most of this, which is why it is tested directly.
Selenium can press Tab and read which element has focus, so it covers the two defects the Cypress project cannot reach (BUG-016,
BUG-020). Known defects are written as the correct behaviour and marked xfail(strict=True)."""
import time

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages import flows
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

manual = pytest.mark.manual
known = pytest.mark.known_bug
pytestmark = [pytest.mark.a11y, pytest.mark.keyboard]


def focused_key(driver) -> str:
    """The data-test attribute (or id) of the element that has keyboard focus."""
    return driver.execute_script("const e = document.activeElement; return (e && (e.getAttribute('data-test') || e.id)) || (e ? e.tagName : '')")


def press(driver, key) -> None:
    ActionChains(driver).send_keys(key).perform()


@manual("TC-081")
def test_tab_order_on_the_products_page_is_logical(driver, inventory):
    order = []
    for _ in range(5):
        press(driver, Keys.TAB)
        order.append(focused_key(driver))
    # menu, sort, then the first product: image link, name link, Add to cart button
    assert order == ["react-burger-menu-btn", "product-sort-container", "item-4-img-link", "item-4-title-link", "add-to-cart-sauce-labs-backpack"]


@manual("TC-082")
def test_add_to_cart_works_with_the_enter_key(inventory):
    inventory.find(inventory.dt("add-to-cart-sauce-labs-onesie")).send_keys(Keys.ENTER)
    assert inventory.appears(inventory.dt("remove-sauce-labs-onesie"))
    assert inventory.has_badge(1)


@manual("TC-083")
def test_escape_closes_the_side_menu(driver, inventory):
    inventory.open_menu()
    logout = inventory.dt("logout-sidebar-link")
    # The menu ignores Escape while it is still sliding open, so press again until it closes (a person would simply try again).
    deadline = time.monotonic() + 6
    closed = False
    while time.monotonic() < deadline and not closed:
        press(driver, Keys.ESCAPE)
        closed = inventory.becomes(lambda: any(e.is_displayed() for e in driver.find_elements(*logout)), False)
    assert closed, "the menu is still open after Escape"


@known
@manual("TC-086")
@pytest.mark.xfail(reason="BUG-020: the cart link cannot be reached or activated with the keyboard")
def test_the_cart_can_be_reached_with_tab_and_opened_with_enter(driver, base_url, inventory):
    reached = False
    for _ in range(40):
        press(driver, Keys.TAB)
        if focused_key(driver) == "shopping-cart-link":
            reached = True
            break
    assert reached, "Tab reaches the cart link"
    press(driver, Keys.ENTER)
    CartPage(driver, base_url).wait_until_loaded()


@known
@manual("TC-084")
@pytest.mark.parametrize("name, selector", [
    ("the menu button", "#react-burger-menu-btn"),
    ("the sort menu", '[data-test="product-sort-container"]'),
    ("an Add to cart button", '[data-test="add-to-cart-sauce-labs-backpack"]'),
    ("the cart link", ".shopping_cart_link"),
], ids=["menu-button", "sort-menu", "add-to-cart", "cart-link"])
@pytest.mark.xfail(reason="BUG-016: no outline, shadow or colour change when a control has keyboard focus")
def test_keyboard_focus_is_visible(driver, inventory, name, selector):
    driver.execute_script("arguments[0].focus()", driver.find_element(By.CSS_SELECTOR, selector))
    style = driver.execute_script("const s = getComputedStyle(document.activeElement); return { outlineStyle: s.outlineStyle, boxShadow: s.boxShadow }")
    assert style["outlineStyle"] != "none" or style["boxShadow"] != "none", f"no visible focus indicator on {name}"


@known
@manual("TC-087")
@pytest.mark.xfail(reason="BUG-020: the cart cannot be opened by keyboard, so the purchase cannot continue")
def test_a_whole_purchase_can_be_completed_without_a_mouse(driver, base_url, inventory):
    inventory.find(inventory.dt("add-to-cart-sauce-labs-backpack")).send_keys(Keys.ENTER)
    driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").send_keys(Keys.ENTER)
    CartPage(driver, base_url).wait_until_loaded()
    driver.find_element(By.CSS_SELECTOR, '[data-test="checkout"]').send_keys(Keys.ENTER)
    form = CheckoutPage(driver, base_url)
    form.wait_for_url_part("checkout-step-one")
    driver.find_element(*form.FIRST).send_keys("Ada" + Keys.TAB + "Lovelace" + Keys.TAB + "12345")
    driver.find_element(*form.CONTINUE).send_keys(Keys.ENTER)
    form.wait_for_url_part("checkout-step-two")
    driver.find_element(*form.FINISH).send_keys(Keys.ENTER)
    assert form.confirmation() == "Thank you for your order!"
