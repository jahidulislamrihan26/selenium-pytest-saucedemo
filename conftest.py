"""Shared fixtures: the browser (Chrome or Firefox), the base URL, logged-in sessions and screenshots of failures."""
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com")
BROWSER = os.environ.get("BROWSER", "chrome").lower()  # chrome or firefox
SHOTS = Path("reports/screenshots")
PASSWORD = "secret_sauce"
USERS = {
    "standard": "standard_user", "locked": "locked_out_user", "problem": "problem_user",
    "error": "error_user", "visual": "visual_user", "glitch": "performance_glitch_user",
}


def pytest_configure(config):
    config.addinivalue_line("markers", "manual(id): the manual test case this test automates, for the traceability table")


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def browser_name() -> str:
    return BROWSER


def _make_driver():
    headless = os.environ.get("HEADLESS", "1") != "0"
    if BROWSER == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        options.add_argument("--width=1280")
        options.add_argument("--height=900")
        return webdriver.Firefox(options=options)
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # Chrome offers to save or check passwords after a login; switch those prompts off.
    options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False,
                                              "profile.password_manager_leak_detection": False})
    return webdriver.Chrome(options=options)  # Selenium Manager finds the matching driver


@pytest.fixture
def driver():
    """A fresh browser for every test, so tests cannot affect each other. HEADLESS=0 shows the window."""
    browser = _make_driver()
    yield browser
    browser.quit()


@pytest.fixture
def login_page(driver, base_url) -> LoginPage:
    page = LoginPage(driver, base_url)
    page.open()
    return page


@pytest.fixture
def login_as(driver, base_url, login_page):
    """Log in through the real login page as one of the site's test users (standard, problem, error, visual, ...)."""
    def _login(user: str = "standard") -> InventoryPage:
        login_page.sign_in(USERS[user], PASSWORD)
        page = InventoryPage(driver, base_url)
        page.wait_until_loaded()
        return page
    return _login


@pytest.fixture
def inventory(login_as) -> InventoryPage:
    """The product list, reached through a real login with the standard user."""
    return login_as("standard")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot when a test fails, so the failure can be seen and not just read."""
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("driver")
    if report.when == "call" and report.failed and driver:
        try:
            SHOTS.mkdir(parents=True, exist_ok=True)
            driver.save_screenshot(str(SHOTS / f"{BROWSER}-{item.name}.png".replace("/", "_").replace("[", "_").replace("]", "")))
        except Exception:  # an open alert or a closed window must not hide the real failure
            pass
