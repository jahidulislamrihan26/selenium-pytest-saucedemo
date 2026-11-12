import pytest

from pages.inventory_page import InventoryPage

manual = pytest.mark.manual  # manual("TC-nnn"): the manual test case this test automates


@pytest.mark.smoke
@manual("TC-001")
def test_valid_user_reaches_the_product_list(driver, base_url, login_page):
    login_page.sign_in("standard_user", "secret_sauce")
    page = InventoryPage(driver, base_url)
    page.wait_until_loaded()
    assert page.count() == 6


@pytest.mark.parametrize(
    "username, password, message",
    [
        pytest.param("standard_user", "not_the_password", "Username and password do not match", marks=manual("TC-003"), id="wrong-password"),
        pytest.param("locked_out_user", "secret_sauce", "locked out", marks=manual("TC-002"), id="locked-out"),
        pytest.param("", "secret_sauce", "Username is required", marks=manual("TC-004"), id="empty-username"),
        pytest.param("standard_user", "", "Password is required", marks=manual("TC-005"), id="empty-password"),
        pytest.param("", "", "Username is required", marks=manual("TC-006"), id="both-empty"),
        pytest.param("STANDARD_USER", "secret_sauce", "Username and password do not match", marks=manual("TC-007"), id="case-sensitive"),
        pytest.param(" standard_user", "secret_sauce", "Username and password do not match", marks=manual("TC-008"), id="leading-space"),
        pytest.param("' OR '1'='1", "x", "Username and password do not match", marks=manual("TC-009"), id="sql-injection"),
        pytest.param("no_such_user", "secret_sauce", "Username and password do not match", id="unknown-user"),
    ],
)
def test_bad_logins_are_rejected_with_a_clear_message(login_page, username, password, message):
    login_page.sign_in(username, password)
    assert message in login_page.error_text()
    assert login_page.is_shown(), "still on the login page"


@manual("TC-010")
def test_password_is_masked_while_typing(login_page):
    assert login_page.password_is_masked()


@manual("TC-011")
def test_enter_key_submits_the_login_form(driver, base_url, login_page):
    from selenium.webdriver.common.keys import Keys
    login_page.type_into(login_page.USERNAME, "standard_user")
    login_page.type_into(login_page.PASSWORD, "secret_sauce" + Keys.ENTER)
    InventoryPage(driver, base_url).wait_until_loaded()


@manual("TC-012")
def test_error_banner_can_be_dismissed(login_page):
    login_page.sign_in("", "")
    login_page.error_text()
    login_page.click(login_page.dt("error-button"))
    login_page.wait_until_gone(login_page.ERROR)


@manual("TC-017")
def test_logout_returns_to_login_and_closes_the_session(driver, base_url, inventory, login_page):
    inventory.logout()
    login_page.wait_until_shown()
    driver.get(base_url + "/inventory.html")
    assert "when you are logged in" in login_page.error_text()


@manual("TC-018")
def test_cart_is_kept_after_logging_out_and_in_again(driver, base_url, inventory, login_page):
    inventory.add("sauce-labs-backpack")
    inventory.logout()
    login_page.wait_until_shown()
    login_page.sign_in("standard_user", "secret_sauce")
    page = InventoryPage(driver, base_url)
    page.wait_until_loaded()
    assert page.has_badge(1), f"badge shows {page.badge_count()}"
