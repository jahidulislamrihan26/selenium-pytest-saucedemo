"""Automated accessibility scan with axe-core on the main pages. Rule: no violation of impact "critical". An automated scan finds only
part of the problems: keyboard use is tested directly in test_keyboard.py, and a screen-reader check is still manual work."""
import pytest

from pages import flows
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests import axe_helper

manual = pytest.mark.manual
pytestmark = pytest.mark.a11y


@manual("TC-060")
def test_login_page_has_no_critical_violations(driver, login_page):
    login_page.wait_until_shown()
    assert axe_helper.critical(driver) == []


@manual("TC-060")
def test_products_page_has_no_critical_violations(driver, inventory):
    assert axe_helper.critical(driver) == []


@manual("TC-060")
def test_product_detail_page_has_no_critical_violations(driver, base_url, inventory):
    driver.get(base_url + "/inventory-item.html?id=4")
    inventory.find(inventory.dt("inventory-item-name"))
    assert axe_helper.critical(driver) == []


@manual("TC-060")
def test_cart_page_has_no_critical_violations(driver, base_url, inventory):
    driver.get(base_url + "/cart.html")
    CartPage(driver, base_url).wait_until_loaded()
    assert axe_helper.critical(driver) == []


@manual("TC-060")
def test_checkout_form_has_no_critical_violations(driver, base_url, inventory):
    flows.to_checkout_form(driver, base_url, inventory, "sauce-labs-backpack")
    assert axe_helper.critical(driver) == []


@manual("TC-060")
def test_checkout_overview_has_no_critical_violations(driver, base_url, inventory):
    flows.to_overview(driver, base_url, inventory, "sauce-labs-backpack")
    assert axe_helper.critical(driver) == []


@manual("TC-060")
def test_order_confirmation_has_no_critical_violations(driver, base_url, inventory):
    flows.place_order(driver, base_url, inventory, "sauce-labs-backpack")
    assert axe_helper.critical(driver) == []


@manual("TC-059")
def test_pages_have_a_title_and_a_language(driver, base_url, inventory):
    from selenium.webdriver.common.by import By
    for path in ("/inventory.html", "/cart.html"):
        driver.get(base_url + path)
        inventory.find(inventory.dt("shopping-cart-link"))
        assert driver.title.strip()
        assert driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
