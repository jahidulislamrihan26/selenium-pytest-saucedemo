import re

import pytest

manual = pytest.mark.manual


@pytest.mark.smoke
@manual("TC-019")
def test_six_products_each_with_name_price_and_button(inventory):
    assert inventory.count() == 6
    assert all(n.strip() for n in inventory.names())
    assert len(inventory.prices()) == 6


@manual("TC-020")
def test_every_product_image_has_alternative_text(inventory):
    images = inventory.find_all(inventory.IMAGE)
    assert len(images) == 6
    assert all((img.get_attribute("alt") or "").strip() for img in images)


@manual("TC-024")
def test_default_sort_is_name_a_to_z(inventory):
    assert inventory.sort_value() == "az"
    names = inventory.names()
    assert names == sorted(names)


@manual("TC-026")
def test_price_sort_low_to_high(inventory):
    inventory.sort_by("lohi")
    prices = inventory.prices()
    assert prices == sorted(prices)


@manual("TC-027")
def test_price_sort_high_to_low(inventory):
    inventory.sort_by("hilo")
    prices = inventory.prices()
    assert prices == sorted(prices, reverse=True)


@manual("TC-025")
def test_name_sort_z_to_a(inventory):
    inventory.sort_by("za")
    names = inventory.names()
    assert names == sorted(names, reverse=True)


@manual("TC-030")
def test_adding_a_product_updates_the_cart_badge(inventory):
    inventory.add("sauce-labs-backpack")
    assert inventory.has_badge(1), f"badge shows {inventory.badge_count()}"


@manual("TC-031")
def test_badge_counts_every_product_and_falls_on_remove(inventory):
    inventory.add("sauce-labs-backpack", "sauce-labs-bike-light", "sauce-labs-onesie")
    assert inventory.has_badge(3), f"badge shows {inventory.badge_count()}"
    inventory.remove("sauce-labs-bike-light")
    assert inventory.has_badge(2), f"badge shows {inventory.badge_count()}"


@manual("TC-076")
def test_all_six_products_can_be_added(inventory):
    inventory.add_all()
    assert inventory.has_badge(6), f"badge shows {inventory.badge_count()}"


@manual("TC-078")
def test_double_click_on_add_to_cart_leaves_the_cart_consistent(driver, inventory):
    from selenium.webdriver import ActionChains
    button = inventory.find(inventory.dt("add-to-cart-sauce-labs-backpack"))
    ActionChains(driver).double_click(button).perform()

    # The first click adds the product and turns the button into Remove, so the second click may remove it again. Either end state is
    # fine; what matters is that the badge and the button agree.
    def consistent() -> bool:
        in_cart = inventory.is_present(inventory.dt("remove-sauce-labs-backpack"))
        return inventory.badge_count() == (1 if in_cart else 0)

    assert inventory.becomes(consistent, True), f"badge shows {inventory.badge_count()} but the button disagrees"


@manual("TC-033")
def test_reset_app_state_clears_the_cart_badge(inventory):
    inventory.add("sauce-labs-backpack")
    assert inventory.has_badge(1)
    inventory.reset_app_state()
    assert inventory.has_badge(0), f"badge shows {inventory.badge_count()}"


@manual("TC-021")
def test_product_detail_page_opens(driver, inventory):
    inventory.open_product(4)
    inventory.wait_for_url_part("inventory-item.html?id=4")
    assert re.search(r"Backpack", driver.page_source)


@manual("TC-079")
def test_adding_from_a_product_page_is_reflected_in_the_list(inventory):
    inventory.open_product(4)
    inventory.click(inventory.dt("add-to-cart"))
    inventory.click(inventory.dt("back-to-products"))
    inventory.wait_until_loaded()
    assert inventory.has_badge(1)
    assert inventory.has_button("remove-sauce-labs-backpack")
