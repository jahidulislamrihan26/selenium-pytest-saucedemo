"""Shared fixtures: the browser, the base URL, a logged-in session and screenshots of failures."""
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com")
SHOTS = Path("reports/screenshots")


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def driver():
    """A fresh browser for every test, so tests cannot affect each other. HEADLESS=0 shows the window."""
    options = Options()
    if os.environ.get("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # Chrome offers to save or check passwords after a login; switch those prompts off.
    options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False,
                                              "profile.password_manager_leak_detection": False})
    browser = webdriver.Chrome(options=options)  # Selenium Manager finds the matching driver
    yield browser
    browser.quit()


@pytest.fixture
def login_page(driver, base_url) -> LoginPage:
    page = LoginPage(driver, base_url)
    page.open()
    return page


@pytest.fixture
def inventory(driver, base_url, login_page) -> InventoryPage:
    """The product list, reached through a real login with the standard user."""
    login_page.sign_in("standard_user", "secret_sauce")
    page = InventoryPage(driver, base_url)
    page.wait_until_loaded()
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot when a test fails, so the failure can be seen and not just read."""
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("driver")
    if report.when == "call" and report.failed and driver:
        SHOTS.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(SHOTS / f"{item.name}.png"))
