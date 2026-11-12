"""The site ships special users with built-in faults. Each test states the CORRECT behaviour and is marked xfail(strict=True): the
suite stays green while the defect exists and turns red the day it is fixed, which is the signal to remove the marker and close
the defect (BUG-nnn in the manual-testing-saucedemo repository)."""
import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages import flows
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage

manual = pytest.mark.manual
known = pytest.mark.known_bug
STANDARD_PRICES = [29.99, 9.99, 15.99, 49.99, 7.99, 15.99]  # in the default name order


@known
@manual("TC-022")
@pytest.mark.xfail(reason="BUG-004: all products show the same placeholder image")
def test_problem_user_every_product_shows_its_own_image(login_as):
    page = login_as("problem")
    assert len(set(page.image_sources())) == 6


@known
@manual("TC-028")
@pytest.mark.xfail(reason="BUG-005: sorting has no effect")
def test_problem_user_sort_z_to_a_reorders_the_list(login_as):
    page = login_as("problem")
    page.sort_by("za")
    names = page.names()
    assert names == sorted(names, reverse=True)


@known
@manual("TC-035")
@pytest.mark.xfail(reason="BUG-006: Add to cart does nothing for some products")
def test_problem_user_fleece_jacket_can_be_added(login_as):
    page = login_as("problem")
    page.add("sauce-labs-fleece-jacket")
    assert page.has_badge(1)


@known
@manual("TC-036")
@pytest.mark.xfail(reason="BUG-006: Remove does nothing for some products")
def test_problem_user_an_added_product_can_be_removed_again(login_as):
    page = login_as("problem")
    page.add("sauce-labs-backpack")
    page.remove("sauce-labs-backpack")
    assert page.appears(page.dt("add-to-cart-sauce-labs-backpack")), "the button is still Remove"


@known
@manual("TC-046")
@pytest.mark.xfail(reason="BUG-007: last name text is typed into the first name field")
def test_problem_user_last_name_can_be_entered_at_checkout(driver, base_url, login_as):
    page = login_as("problem")
    form = flows.to_checkout_form(driver, base_url, page, "sauce-labs-backpack")
    form.fill_info()
    form.wait_for_url_part("checkout-step-two")


@known
@manual("TC-029")
@pytest.mark.xfail(reason='BUG-008: sorting raises a "Sorting is broken!" alert')
def test_error_user_sorting_works_without_an_error_alert(driver, login_as):
    page = login_as("error")
    page.sort_by("za")
    try:
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
    except TimeoutException:
        return  # no alert: the correct behaviour
    text = alert.text
    alert.accept()
    pytest.fail(f"an alert was shown: {text}")


@known
@manual("TC-037")
@pytest.mark.xfail(reason="BUG-009: Add to cart does nothing for some products")
def test_error_user_bolt_t_shirt_can_be_added(login_as):
    page = login_as("error")
    page.add("sauce-labs-bolt-t-shirt")
    assert page.has_badge(1)


@known
@manual("TC-047")
@pytest.mark.xfail(reason="BUG-010: Finish does nothing, the order is not placed")
def test_error_user_an_order_can_be_finished(driver, base_url, login_as):
    page = login_as("error")
    flows.place_order(driver, base_url, page, "sauce-labs-backpack")


@known
@manual("TC-014")
@pytest.mark.xfail(reason="BUG-012: products take about 5 seconds to appear after login")
def test_performance_glitch_user_products_appear_within_3_seconds(driver, base_url, login_page):
    login_page.type_into(login_page.USERNAME, "performance_glitch_user")
    login_page.type_into(login_page.PASSWORD, "secret_sauce")
    start = time.monotonic()
    login_page.click(login_page.SUBMIT)
    InventoryPage(driver, base_url).wait_until_loaded()
    assert time.monotonic() - start < 3, "products took 3 seconds or more to appear"


@known
@manual("TC-023")
@pytest.mark.xfail(reason="BUG-011: prices differ from standard_user")
def test_visual_user_prices_match_the_standard_catalogue(login_as):
    page = login_as("visual")
    assert page.prices() == STANDARD_PRICES
