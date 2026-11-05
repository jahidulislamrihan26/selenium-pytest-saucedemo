import re

import pytest


@pytest.mark.smoke
def test_six_products_each_with_name_price_and_button(inventory):
    assert inventory.count() == 6
    assert all(n.strip() for n in inventory.names())
    assert len(inventory.prices()) == 6


def test_price_sort_low_to_high(inventory):
    inventory.sort_by("lohi")
    prices = inventory.prices()
    assert prices == sorted(prices)


def test_price_sort_high_to_low(inventory):
    inventory.sort_by("hilo")
    prices = inventory.prices()
    assert prices == sorted(prices, reverse=True)


def test_name_sort_z_to_a(inventory):
    inventory.sort_by("za")
    names = inventory.names()
    assert names == sorted(names, reverse=True)


def test_adding_a_product_updates_the_cart_badge(inventory):
    inventory.add("sauce-labs-backpack")
    assert inventory.badge_count() == 1


def test_badge_counts_every_product_and_falls_on_remove(inventory):
    inventory.add("sauce-labs-backpack", "sauce-labs-bike-light", "sauce-labs-onesie")
    assert inventory.badge_count() == 3
    inventory.remove("sauce-labs-bike-light")
    assert inventory.badge_count() == 2


def test_product_detail_page_opens(driver, inventory):
    inventory.open_product(4)
    inventory.wait_for_url_part("inventory-item.html?id=4")
    assert re.search(r"Backpack", driver.page_source)
