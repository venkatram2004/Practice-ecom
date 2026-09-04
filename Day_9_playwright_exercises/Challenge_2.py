import pytest
from playwright.sync_api import Page, expect
from user_login import user_auth

BASE_URL = "https://www.saucedemo.com"


def test_dom_relationships_and_relative_locators(page: Page):
    user_auth(page)

    expect(page).to_have_url(f"{BASE_URL}/inventory.html")

    target_name = "Sauce Labs Backpack"

    product_name_element = page.locator(
        ".inventory_item_name", has_text=target_name)

    card = page.locator(".inventory_item").filter(has=product_name_element)
    assert card.count() == 1, "Should resolve to exactly one product card"

    card_price = card.locator(".inventory_item_price")
    card_image = card.locator(".inventory_item_img img")
    card_add_button = card.locator("button.btn_inventory")

    expect(card_price).to_contain_text("$")
    expect(card_image).to_be_visible()
    expect(card_add_button).to_have_text("Add to cart")

    name_parent = product_name_element.locator("..")
    expect(name_parent).to_be_visible()

    card_children = card.locator("> div")
    print(
        f"\n[DOM Info] Card has {card_children.count()} direct container children.")

    pricebar_sibling = card.locator(".inventory_item_label ~ .pricebar")
    expect(pricebar_sibling).to_be_visible()

    nested_image = card.locator(".inventory_item_img >> a >> img")
    expect(nested_image).to_have_attribute("alt", target_name)

    card_add_button.click()
    expect(card_add_button).to_have_text("Remove")

    expect(page.locator(".shopping_cart_badge")).to_have_text("1")

    page.locator(".shopping_cart_link").click()
    expect(page.locator(".inventory_item_name")).to_have_text(target_name)


@pytest.mark.parametrize(
    "product_name",
    [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
    ],
)
def test_relative_product_card_addition_parameterized(page: Page, product_name: str):
    user_auth(page)

    card = page.locator(".inventory_item").filter(
        has=page.locator(".inventory_item_name", has_text=product_name)
    )

    add_btn = card.locator("button.btn_inventory")
    expect(add_btn).to_have_text("Add to cart")

    add_btn.click()
    expect(add_btn).to_have_text("Remove")

    page.locator(".shopping_cart_link").click()
    expect(page.locator(".inventory_item_name",
           has_text=product_name)).to_be_visible()
