"""Access-control, session and transport checks. A defect that exists on the site today is written as the CORRECT behaviour and marked
xfail(strict=True): the suite stays green while the defect exists and turns red the day it is fixed, which is the signal to remove
the marker and close the defect (BUG-013 and BUG-018 in the manual-testing-saucedemo repository)."""
import time
import urllib.error
import urllib.request

import pytest

from pages.login_page import LoginPage

manual = pytest.mark.manual
known = pytest.mark.known_bug


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # report the redirect itself instead of following it
        return None


def _fetch(url: str, follow: bool = True):
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(_NoRedirect)
    try:
        return opener.open(urllib.request.Request(url, headers={"User-Agent": "selenium-pytest-saucedemo"}), timeout=20)
    except urllib.error.HTTPError as err:  # a 3xx answer is raised as an error when redirects are off
        return err


@pytest.mark.smoke
@manual("TC-015")
@pytest.mark.parametrize("path", ["/inventory.html", "/cart.html", "/checkout-step-one.html"])
def test_inner_pages_need_a_login(driver, base_url, path):
    driver.get(base_url + path)
    page = LoginPage(driver, base_url)
    assert "when you are logged in" in page.error_text()
    assert page.is_shown()


@known
@manual("TC-065")
@pytest.mark.xfail(reason="BUG-013: a cookie holding a valid user name opens the shop without the password")
def test_a_forged_session_cookie_is_rejected(driver, base_url):
    driver.get(base_url + "/")
    driver.add_cookie({"name": "session-username", "value": "standard_user"})
    driver.get(base_url + "/inventory.html")
    assert LoginPage(driver, base_url).is_shown_within(4), "correct behaviour: back at the login page"


@known
@manual("TC-066")
@pytest.mark.xfail(reason="BUG-013: the session cookie is readable by script and not marked Secure")
def test_session_cookie_is_http_only_and_secure(driver, login_as):
    login_as("standard")
    cookie = driver.get_cookie("session-username")
    assert cookie and cookie.get("httpOnly") and cookie.get("secure")


@manual("TC-067")
def test_session_cookie_expires_after_a_limited_time(driver, login_as):
    login_as("standard")
    cookie = driver.get_cookie("session-username")
    assert cookie and "expiry" in cookie
    assert time.time() < cookie["expiry"] < time.time() + 3600


@manual("TC-068")
def test_plain_http_is_redirected_to_https():
    response = _fetch("http://www.saucedemo.com/", follow=False)
    assert response.status in (301, 308)
    assert response.headers["Location"].startswith("https://")


@known
@manual("TC-069")
@pytest.mark.xfail(reason="BUG-018: none of the standard security headers are sent")
def test_standard_security_headers_are_sent():
    headers = {k.lower() for k in _fetch("https://www.saucedemo.com/").headers.keys()}
    for name in ("strict-transport-security", "content-security-policy", "x-content-type-options", "referrer-policy"):
        assert name in headers, name


@manual("TC-070")
def test_script_text_in_a_product_address_is_not_executed(driver, base_url, inventory):
    driver.get(base_url + "/inventory-item.html?id=%3Cscript%3Ealert(1)%3C%2Fscript%3E")
    assert inventory.text_of(inventory.dt("inventory-item-name")) == "ITEM NOT FOUND"
    from selenium.common.exceptions import NoAlertPresentException
    with pytest.raises(NoAlertPresentException):
        driver.switch_to.alert


def test_script_typed_into_the_login_form_is_not_executed(driver, login_page):
    login_page.sign_in('<img src=x onerror="window.__xss=1">', "x")
    login_page.error_text()
    assert driver.execute_script("return window.__xss") is None
