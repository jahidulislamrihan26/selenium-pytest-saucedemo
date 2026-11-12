"""What happens when a shopper types an address (manual-testing charter 5), and the links in the page."""
import re

import pytest
from selenium.webdriver.common.by import By

manual = pytest.mark.manual


@pytest.mark.parametrize("query", ["?id=999", "?id=abc", "?id=-1", ""], ids=["id-999", "id-abc", "id-minus-1", "no-id"])
@manual("TC-071")
def test_invalid_product_ids_show_a_not_found_state(driver, base_url, inventory, query):
    driver.get(f"{base_url}/inventory-item.html{query}")
    assert inventory.text_of(inventory.dt("inventory-item-name")) == "ITEM NOT FOUND"


@manual("TC-054")
def test_about_link_points_to_saucelabs(driver, inventory):
    href = driver.find_element(By.CSS_SELECTOR, "#about_sidebar_link").get_attribute("href")
    assert "saucelabs.com" in href


@manual("TC-055")
def test_footer_has_the_three_social_links(driver, inventory):
    links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "footer a")]
    assert len(links) == 3
    assert re.search(r"x\.com.*facebook\.com.*linkedin\.com", " ".join(links))
