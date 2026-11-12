"""Layouts at the screen sizes of the manual suite: desktop, tablet, phone and narrow screens.
The size is set with the browser's device emulation (Chrome only), because a desktop window cannot be made narrower than about
500 pixels."""
import pytest

manual = pytest.mark.manual
SIZES = [
    pytest.param(1366, 768, marks=manual("TC-056"), id="desktop-1366"),
    pytest.param(768, 1024, id="tablet-768"),
    pytest.param(375, 667, marks=manual("TC-057"), id="phone-375"),
    pytest.param(480, 640, marks=manual("TC-085"), id="small-phone-480"),
    pytest.param(320, 640, marks=manual("TC-085"), id="narrow-phone-320"),
]


@pytest.fixture
def at_size(driver, browser_name):
    if browser_name != "chrome":
        pytest.skip("device emulation is a Chrome feature")

    def _set(width: int, height: int) -> None:
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": width < 500})
    return _set


@pytest.mark.parametrize("width, height", SIZES)
def test_products_page_has_no_horizontal_scroll(driver, at_size, login_as, width, height):
    at_size(width, height)
    page = login_as("standard")
    assert page.count() == 6
    overflow = driver.execute_script("return document.documentElement.scrollWidth - window.innerWidth")
    assert overflow <= 0, f"the page is {overflow}px wider than the screen"


@pytest.mark.parametrize("width, height", SIZES)
def test_cart_and_menu_are_usable(driver, base_url, at_size, login_as, width, height):
    from pages.cart_page import CartPage
    at_size(width, height)
    page = login_as("standard")
    page.add("sauce-labs-backpack")
    page.open_cart()
    CartPage(driver, base_url).wait_until_loaded()
    page.open_menu()
    assert page.find(page.dt("inventory-sidebar-link")).is_displayed()
