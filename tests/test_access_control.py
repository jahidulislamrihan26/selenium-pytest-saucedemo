"""Access-control checks. A defect that exists on the site today is written as the CORRECT behaviour and marked
xfail(strict=True): the suite stays green while the defect exists and turns red the day it is fixed, which is the signal
to remove the marker and close the defect (BUG-013 in the manual-testing-saucedemo repository)."""
import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.parametrize("path", ["/inventory.html", "/cart.html", "/checkout-step-one.html"])
def test_inner_pages_need_a_login(driver, base_url, path):
    driver.get(base_url + path)
    page = LoginPage(driver, base_url)
    assert "when you are logged in" in page.error_text()
    assert page.is_shown()


@pytest.mark.known_bug
@pytest.mark.xfail(reason="BUG-013: a cookie holding a valid user name opens the shop without the password")
def test_a_forged_session_cookie_is_rejected(driver, base_url):
    driver.get(base_url + "/")
    driver.add_cookie({"name": "session-username", "value": "standard_user"})
    driver.get(base_url + "/inventory.html")
    page = LoginPage(driver, base_url)
    assert page.is_shown_within(4), "correct behaviour: back at the login page"


def test_script_typed_into_the_login_form_is_not_executed(driver, login_page):
    login_page.sign_in('<img src=x onerror="window.__xss=1">', "x")
    assert driver.execute_script("return window.__xss") is None
