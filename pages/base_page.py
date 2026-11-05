"""Base page object: explicit waits and the small actions every page shares. No fixed sleeps anywhere."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 10


class BasePage:
    path = "/"

    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, TIMEOUT)

    @staticmethod
    def dt(test_id: str) -> tuple[str, str]:
        """Locator for the site's data-test attribute, which stays stable when styling changes."""
        return (By.CSS_SELECTOR, f'[data-test="{test_id}"]')

    def open(self) -> None:
        self.driver.get(self.base_url + self.path)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_into(self, locator, text: str) -> None:
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator) -> str:
        return self.find(locator).text

    def wait_for_url_part(self, part: str) -> None:
        self.wait.until(EC.url_contains(part))

    def is_present(self, locator) -> bool:
        return len(self.find_all(locator)) > 0

    def wait_until_gone(self, locator) -> None:
        self.wait.until(lambda d: len(d.find_elements(*locator)) == 0)
