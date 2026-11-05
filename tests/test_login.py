import pytest

from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_valid_user_reaches_the_product_list(driver, base_url, login_page):
    login_page.sign_in("standard_user", "secret_sauce")
    page = InventoryPage(driver, base_url)
    page.wait_until_loaded()
    assert page.count() == 6


@pytest.mark.parametrize(
    "username, password, message",
    [
        ("standard_user", "not_the_password", "Username and password do not match"),
        ("locked_out_user", "secret_sauce", "locked out"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("no_such_user", "secret_sauce", "Username and password do not match"),
    ],
    ids=["wrong-password", "locked-out", "empty-username", "empty-password", "unknown-user"],
)
def test_bad_logins_are_rejected_with_a_clear_message(login_page, username, password, message):
    login_page.sign_in(username, password)
    assert message in login_page.error_text()
    assert login_page.is_shown(), "still on the login page"


def test_password_is_masked_while_typing(login_page):
    assert login_page.password_is_masked()


def test_logout_returns_to_login_and_closes_the_session(driver, base_url, inventory, login_page):
    inventory.logout()
    login_page.wait_for_url_part("saucedemo.com")
    assert login_page.is_shown()
    driver.get(base_url + "/inventory.html")
    assert "when you are logged in" in login_page.error_text()
